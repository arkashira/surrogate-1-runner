import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name = "components")
public class Component {

    private String name;
    private String price;

    // Getters and setters
}