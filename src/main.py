# 1. Install required package
pip install schedule

# 2. Create necessary directories
mkdir -p /opt/axentx/surrogate-1/{data,logs}

# 3. Run the scheduler
python /opt/axentx/surrogate-1/src/cron_scheduler.py

# 4. (Optional) Set up as systemd service for production