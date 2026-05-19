import pandas as pd
from upgrade_path_recommendation import UpgradePathRecommendation

def main():
    # Load game data
    game_data = pd.read_csv('data/games.csv')

    # Initialize recommender with a budget of 150
    recommender = UpgradePathRecommendation(game_data, 150)

    # Get recommended upgrade paths
    recommended_paths = recommender.recommend_upgrade_paths()
    print("Recommended Upgrade Paths:")
    for path in recommended_paths:
        print(path)

    # Filter and sort by genre and performance impact
    filters = {'genre': 'Action'}
    sorted_paths = recommender.filter_and_sort(filters, 'performance_impact')
    print("\nFiltered and Sorted Upgrade Paths:")
    for path in sorted_paths:
        print(path)

if __name__ == '__main__':
    main()