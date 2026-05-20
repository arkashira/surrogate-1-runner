import pandas as pd

def generate_weekly_report(resolutions):
    data = {
        'guide_id': [r.id for r in resolutions],
        'success_rate': [r.success_count / r.total_count for r in resolutions]
    }
    df = pd.DataFrame(data)
    return df