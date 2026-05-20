import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.data.domain.Sort.Order;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
public class ComponentComparisonController {

    @GetMapping("/components/comparison")
    public Map<String, List<Map<String, String>>> getComparisonTable(
            @RequestParam List<String> selectedComponents,
            @RequestParam Map<String, String> filterSpecs,
            @RequestParam(defaultValue = "price") String sortBy) {
        // Implement filtering and sorting logic here
        // For now, just return a dummy response
        return Map.of("components", List.of(
                Map.of("name", "Component 1", "price", "100"),
                Map.of("name", "Component 2", "price", "200")
        ));
    }
}