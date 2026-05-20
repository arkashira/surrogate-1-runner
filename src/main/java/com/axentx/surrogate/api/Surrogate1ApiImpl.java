public class Surrogate1ApiImpl implements Surrogate1Api {
    @Override
    public GamingGpuResource getGamingGpuResource() {
        return new GamingGpuResource("gpu-1", "Gaming GPU", "Utilize for graphics processing");
    }

    @Override
    public void setGamingGpuResource(GamingGpuResource gamingGpuResource) {
        // Not implemented
    }
}