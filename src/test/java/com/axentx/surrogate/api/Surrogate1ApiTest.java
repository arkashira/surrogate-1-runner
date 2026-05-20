import org.junit.Test;

public class Surrogate1ApiTest {
    @Test
    public void testSurrogate1Api() {
        GamingGpuResource gamingGpuResource = new GamingGpuResource("gpu-1", "Gaming GPU", "Utilize for graphics processing");
        Surrogate1Api surrogate1Api = new Surrogate1ApiImpl();
        assert surrogate1Api.getGamingGpuResource().getId().equals("gpu-1");
    }
}