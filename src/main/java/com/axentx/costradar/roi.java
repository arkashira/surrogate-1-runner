import java.util.HashMap;
import java.util.Map;

public class RoiCalculator {
    public static class Component {
        private String name;
        private double cost;
        private double fpsGain;

        public Component(String name, double cost, double fpsGain) {
            this.name = name;
            this.cost = cost;
            this.fpsGain = fpsGain;
        }

        public double calculateRoi() {
            return fpsGain / cost;
        }
    }

    public static class RoiData {
        private Map<String, Component> components = new HashMap<>();

        public void addComponent(Component component) {
            components.put(component.name, component);
        }

        public double getComponentRoi(String componentName) {
            return components.get(componentName).calculateRoi();
        }
    }

    public static void main(String[] args) {
        RoiData roiData = new RoiData();
        roiData.addComponent(new Component("GPU", 1000, 10));
        roiData.addComponent(new Component("CPU", 500, 5));

        System.out.println("GPU ROI: " + roiData.getComponentRoi("GPU"));
        System.out.println("CPU ROI: " + roiData.getComponentRoi("CPU"));
    }
}