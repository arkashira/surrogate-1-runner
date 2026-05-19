/var/log/axentx/surrogate-1/audit.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 axentx axentx
    sharedscripts
    postrotate
        systemctl reload axentx-surrogate-1 >/dev/null 2>&1 || true
    endscript
}