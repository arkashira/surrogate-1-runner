import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.data.domain.Sort.Order;
import org.springframework.data.repository.CrudRepository;

import java.util.List;
import java.util.Map;

public interface ComponentRepository extends CrudRepository<Component, Long> {

    List<Component> findByFilter(Map<String, String> filterSpecs);

    List<Component> findBySort(Sort sort);
}