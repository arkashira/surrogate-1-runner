def fetch_benchmarks(source):
    """
    Mock function to simulate fetching benchmarks from a given source.
    In a real scenario, this would involve API calls or scraping.
    """
    mock_data = {
        'PassMark': {'component1': 850, 'component2': 920},
        'UserBenchmark': {'component1': 880, 'component3': 950},
        'Geekbench': {'component2': 900, 'component3': 970}
    }
    return mock_data.get(source, {})