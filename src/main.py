from fps_calculator import FPSCalculator

def main():
    base_fps = 60.0
    fps_calculator = FPSCalculator(base_fps)

    # Add performance data for components
    performance_data = {
        'gpu': {1: 70.0, 2: 80.0, 3: 90.0},
        'cpu': {1: 65.0, 2: 75.0, 3: 85.0},
        'ram': {1: 62.0, 2: 72.0, 3: 82.0}
    }
    for component, data in performance_data.items():
        fps_calculator.add_component_performance_data(component, data)

    # Calculate FPS gains per dollar for each component
    costs = {'gpu': 100.0, 'cpu': 80.0, 'ram': 60.0}
    upgrade_level = 1
    sorted_components = fps_calculator.get_sorted_components_by_fps_gain_per_dollar(upgrade_level, costs)

    # Display the results
    print(f"Expected FPS gains per dollar for upgrade level {upgrade_level}:")
    for component in sorted_components:
        print(f"{component['component_name']}: {component['fps_gain_per_dollar']:.2f}")

if __name__ == '__main__':
    main()