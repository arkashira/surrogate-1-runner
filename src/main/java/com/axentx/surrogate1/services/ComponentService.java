import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.data.domain.Sort.Order;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class ComponentService {

    public List<Map<String, String>> getComponentsByFilter(Map<String, String> filterSpecs) {
        // Implement filtering logic here
        // For now, just return a dummy list
        return List.of(
                Map.of("name", "Component 1", "price", "100"),
                Map.of("name", "Component 2", "price", "200")
        );
    }

    public List<Map<String, String>> getComponentsSortedBy(Sort sort) {
        // Implement sorting logic here
        // For now, just return a dummy list
        return List.of(
                Map.of("name", "Component 1", "price", "100"),
                Map.of("name", "Component 2", "price", "200")
        );
    }
}