import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

public class RoiService {
    private ConcurrentMap<String, RoiData> roiDataCache = new ConcurrentHashMap<>();

    public void updateRoiData(RoiData roiData) {
        roiDataCache.put(roiData.hashCode() + "", roiData);
    }

    public double getComponentRoi(String componentName) {
        for (RoiData roiData : roiDataCache.values()) {
            if (roiData.getComponentRoi(componentName) != 0) {
                return roiData.getComponentRoi(componentName);
            }
        }
        return 0;
    }
}