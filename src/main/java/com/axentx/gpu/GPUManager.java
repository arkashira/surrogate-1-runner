import java.util.ArrayList;
import java.util.List;

public class GPUManager {
    private final List<GPU> gpus;

    public GPUManager() {
        this.gpus = new ArrayList<>();
    }

    public void addGPU(GPU gpu) {
        gpus.add(gpu);
    }

    public void removeGPU(GPU gpu) {
        gpus.remove(gpu);
    }

    public int getNumGPUs() {
        return gpus.size();
    }
}

class GPU {
    private final int id;

    public GPU(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }
}