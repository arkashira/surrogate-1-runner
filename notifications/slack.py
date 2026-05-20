class SlackDispatcher:
    def __init__(
        self,
        webhook_url: Optional[str] = None,
        db_path: str = "/opt/axentx/surrogate-1/data/alerts.db",
        deduplication_window_hours: int = 24,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.webhook_url = webhook_url or os.environ.get(
            "SLACK_WEBHOOK_URL",
            "<slack-webhook>"
        )
        self.db_path = db_path
        self.deduplication_window = timedelta(hours=deduplication_window_hours)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._init_database()

    def _post_to_slack(self, payload: Dict[str, Any]) -> Optional[str]:
        """Post a message to the Slack webhook with retry logic."""
        for attempt in range(self.max_retries):
            try:
                data = json.dumps(payload).encode("utf-8")
                req = Request(
                    self.webhook_url,
                    data=data,
                    headers={"Content-Type": "application/json"}
                )
                with urlopen(req, timeout=10) as response:
                    response_data = json.loads(response.read().decode("utf-8"))
                    return response_data.get("ts")  # Return message timestamp
            except URLError as e:
                logger.warning(f"Slack API attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error("Max retries reached for Slack API call")
                    raise
        return None

    def _update_slack_message(self, message_ts: str, payload: Dict[str, Any]) -> bool:
        """Update an existing Slack message."""
        # Slack doesn't support direct message updates via webhook
        # This would require using Slack API with OAuth tokens
        # Implementation would go here
        return False

    def _get_existing_alert(self, alert: Alert) -> Optional[Alert]:
        """Get existing alert from database."""
        dedup_key = self._generate_dedup_key(alert.metric_name)
        cutoff_time = datetime.utcnow() - self.deduplication_window

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM alerts
                WHERE deduplication_key = ?
                AND timestamp > ?
                ORDER BY timestamp DESC
                LIMIT 1
            """, (dedup_key, cutoff_time.isoformat()))
            row = cursor.fetchone()

            if row:
                return Alert(
                    id=row[0],
                    metric_name=row[1],
                    current_value=row[2],
                    moving_average=row[3],
                    standard_deviation=row[4],
                    severity=row[5],
                    timestamp=row[6],
                    raw_data_link=row[7],
                    slack_message_id=row[8],
                    deduplication_key=row[9]
                )
        return None

    def dispatch(self, alert: Alert) -> bool:
        """Main dispatch method that handles the alert lifecycle."""
        # Check for existing alert
        existing_alert = self._get_existing_alert(alert)

        if existing_alert and existing_alert.slack_message_id:
            logger.info(f"Duplicate alert detected for {alert.metric_name}, skipping")
            return False

        # Format and post new alert
        payload = self._format_slack_message(alert)
        message_ts = self._post_to_slack(payload)

        if message_ts:
            # Update database with message timestamp
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    INSERT INTO alerts (
                        metric_name, current_value, moving_average,
                        standard_deviation, severity, timestamp,
                        raw_data_link, deduplication_key, slack_message_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert.metric_name, alert.current_value,
                    alert.moving_average, alert.standard_deviation,
                    alert.severity, alert.timestamp,
                    alert.raw_data_link, alert.deduplication_key, message_ts
                ))
                conn.commit()
            return True
        return False