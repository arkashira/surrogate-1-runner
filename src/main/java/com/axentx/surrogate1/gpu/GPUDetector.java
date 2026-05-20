import java.util.ArrayList;
import java.util.List;

public class GPUDetector {
    private List<GPU> gpus;

    public GPUDetector() {
        this.gpus = new ArrayList<>();
    }

    public void addGPU(String name) {
        gpus.add(new GPU(name));
    }

    public List<GPU> getGPUs() {
        return gpus;
    }

    public void configureGPUs() {
        for (GPU gpu : gpus) {
            gpu.configure();
        }
    }

    public double getBandwidth() {
        double totalBandwidth = 0;
        for (GPU gpu : gpus) {
            totalBandwidth += gpu.getBandwidth();
        }
        return totalBandwidth;
    }

    public double getBaseBandwidth() {
        return 1000; // Base bandwidth in MB/s
    }
}