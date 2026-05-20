import com.axentx.surrogate1.services.MarginService;
import com.axentx.surrogate1.api.Margins;

public class MarginController {
    private final MarginService marginService;

    public MarginController(MarginService marginService) {
        this.marginService = marginService;
    }

    public Margins getMargins() {
        return marginService.getMargins();
    }
}