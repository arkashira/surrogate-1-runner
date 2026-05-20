import org.junit.Test;

public class GamingGpuResourceTest {
    @Test
    public void testGamingGpuResource() {
        GamingGpuResource gamingGpuResource = new GamingGpuResource("gpu-1", "Gaming GPU", "Utilize for graphics processing");
        assert gamingGpuResource.getId().equals("gpu-1");
        assert gamingGpuResource.getName().equals("Gaming GPU");
        assert gamingGpuResource.getDescription().equals("Utilize for graphics processing");
    }
}