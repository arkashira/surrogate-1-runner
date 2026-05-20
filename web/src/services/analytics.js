const analytics = {
  config: {
    endpoint: '/api/analytics/track',
    batch: true,
    batchSize: 50,
    flushInterval: 10000,
    enabled: process.env.ANALYTICS_ENABLED !== 'false',
  },
  _events: [],
  _flushTimer: null,
  _batchSize: 0,

  init() {
    if (!this.config.enabled) return;
    this._flushTimer = setInterval(() => this._flush(), this.config.flushInterval);
  },

  track(event, data = {}) {
    if (!this.config.enabled) return;
    const payload = {
      event,
      timestamp: new Date().toISOString(),
      ...data,
    };
    this._events.push(payload);
    this._batchSize++;
    if (this._batchSize >= this.config.batchSize) {
      this._flush();
    }
  },

  _flush() {
    if (this._events.length === 0) return;
    const batch = this._events.splice(0, this.config.batchSize);
    fetch(this.config.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(batch),
    }).catch((err) => {
      console.error('Analytics flush failed:', err);
    });
  },

  // Correction-specific tracking events
  trackCorrectionSubmission(correction) {
    this.track('correction_submission', {
      correction_id: correction.id,
      invoice_id: correction.invoice_id,
      user_id: correction.user_id,
      correction_type: correction.type,
      field_name: correction.field_name,
      original_value: correction.original_value,
      corrected_value: correction.corrected_value,
      confidence_score: correction.confidence_score,
      source: correction.source,
    });
  },

  trackCorrectionFlag(flag) {
    this.track('correction_flag', {
      flag_id: flag.id,
      invoice_id: flag.invoice_id,
      user_id: flag.user_id,
      flag_type: flag.type,
      reason: flag.reason,
      timestamp: flag.timestamp,
    });
  },

  trackCorrectionReview(review) {
    this.track('correction_review', {
      review_id: review.id,
      correction_id: review.correction_id,
      invoice_id: review.invoice_id,
      user_id: review.user_id,
      review_score: review.score,
      review_notes: review.notes,
      timestamp: review.timestamp,
    });
  },

  trackCorrectionInterfaceInteraction(interaction) {
    this.track('correction_interface_interaction', {
      interaction_type: interaction.type,
      page: interaction.page,
      duration_ms: interaction.duration_ms,
      invoice_count: interaction.invoice_count,
      timestamp: interaction.timestamp,
    });
  },

  trackCorrectionQualityMetrics(metrics) {
    this.track('correction_quality_metrics', {
      total_corrections: metrics.total,
      accepted_rate: metrics.accepted_rate,
      rejected_rate: metrics.rejected_rate,
      avg_confidence: metrics.avg_confidence,
      time_to_submit_ms: metrics.time_to_submit_ms,
      timestamp: metrics.timestamp,
    });
  },

  trackCorrectionSession(session) {
    this.track('correction_session', {
      session_id: session.id,
      user_id: session.user_id,
      invoice_count: session.invoice_count,
      corrections_made: session.corrections_made,
      session_duration_ms: session.duration_ms,
      start_time: session.start_time,
      end_time: session.end_time,
    });
  },

  trackCorrectionError(error) {
    this.track('correction_error', {
      error_type: error.type,
      error_message: error.message,
      invoice_id: error.invoice_id,
      user_id: error.user_id,
      stack: error.stack,
      timestamp: error.timestamp,
    });
  },
};

// Export for module usage
export default analytics;