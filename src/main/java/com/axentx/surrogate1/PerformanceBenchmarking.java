
package com.axentx.surrogate1;

import com.axentx.common.component.Component;
import com.axentx.common.performance.FPS;
import com.axentx.common.pricing.Price;

import java.util.List;

public class PerformanceBenchmarking {

    public static List<Component> calculateROI(List<Component> components, FPS currentFPS, Price budget) {
        return components.stream()
                .map(component -> new Component(
                        component.getName(),
                        component.getPrice(),
                        calculateFPSGain(component, currentFPS),
                        calculateROI(component.getPrice(), calculateFPSGain(component, currentFPS), budget)
                ))
                .sorted((c1, c2) -> Double.compare(c2.getROI(), c1.getROI()))
                .stream()
                .toList();
    }

    private static double calculateFPSGain(Component component, FPS currentFPS) {
        // Implement real-time performance benchmarking algorithm here
        // This method should return the expected FPS gain for the given component
        // based on the current FPS and the component's performance characteristics
        // For now, let's assume a simple linear relationship for demonstration purposes
        return component.getPerformance().getFPS() - currentFPS.getValue();
    }

    private static double calculateROI(Price price, double fpsGain, Price budget) {
        if (price.compareTo(budget) > 0) {
            return 0; // ROI is 0 if the component exceeds the budget
        }
        return fpsGain / price.getValue();
    }
}