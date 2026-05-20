public class GPU {
    private String name;
    private boolean configured;
    private double bandwidth;

    public GPU(String name) {
        this.name = name;
        this.configured = false;
        this.bandwidth = 0;
    }

    public void configure() {
        this.configured = true;
        this.bandwidth = 2000; // Bandwidth in MB/s
    }

    public boolean isConfigured() {
        return configured;
    }

    public double getBandwidth() {
        return bandwidth;
    }
}