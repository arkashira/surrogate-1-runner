import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class ConcurrentCollectionTest {

    @Test
    public void testConcurrentHashMap() {
        ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();
        map.put("key", "value");
        assertEquals("value", map.get("key"));
    }

    @Test
    public void testConcurrentLinkedQueue() {
        ConcurrentLinkedQueue<String> queue = new ConcurrentLinkedQueue<>();
        queue.add("element");
        assertEquals("element", queue.peek());
    }

    @Test
    public void testCopyOnWriteArrayList() {
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        list.add("element");
        assertEquals("element", list.get(0));
    }
}