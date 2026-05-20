package dashboard;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Collection;

@Controller
@RequestMapping("/dashboard/validation")
public class ValidationDashboardController {

    private final ValidationEngineService validationService;

    public ValidationDashboardController(ValidationEngineService validationService) {
        this.validationService = validationService;
    }

    /**
     * Show the validation dashboard with all stored results.
     */
    @GetMapping
    public String dashboard(Model model) {
        Collection<ValidationResult> results = validationService.getAllResults();
        model.addAttribute("results", results);
        return "validation_dashboard";
    }

    /**
     * Trigger a validation scan for the supplied collection ID.
     */
    @PostMapping("/run")
    public String runValidation(@RequestParam("collectionId") String collectionId,
                                Model model) {
        ValidationResult result = validationService.runValidation(collectionId);
        model.addAttribute("results", validationService.getAllResults());
        model.addAttribute("message", "Validation completed for " + result.getCollectionId());
        return "validation_dashboard";
    }
}