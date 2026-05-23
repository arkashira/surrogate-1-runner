import json
from cost_alerts import CostAlert

def main():
    cost_alert = CostAlert()

    # Example usage
    cost_alert.set_threshold("service3", 300.0)

    current_costs = {
        "service1": 150.0,
        "service2": 250.0,
        "service3": 350.0
    }

    alerts = cost_alert.check_costs(current_costs)
    print("Alerts:", alerts)

    recent_alerts = cost_alert.get_alerts(hours=1)
    print("Recent Alerts:", recent_alerts)

if __name__ == "__main__":
    main()