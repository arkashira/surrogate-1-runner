import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RoiController {
    private RoiService roiService;

    public RoiController(RoiService roiService) {
        this.roiService = roiService;
    }

    @GetMapping("/roi")
    public double getComponentRoi() {
        return roiService.getComponentRoi("GPU");
    }
}