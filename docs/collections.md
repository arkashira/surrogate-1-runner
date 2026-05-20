import java.util.concurrent.ConcurrentHashMap;

public class Example {
    public static void main(String[] args) {
        // Using ConcurrentHashMap for thread-safe map operations
        ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();
        map.put("key", "value");
        System.out.println(map.get("key")); // prints "value"

        // Using ConcurrentHashMap for thread-safe set operations
        ConcurrentHashMap<String, String> set = new ConcurrentHashMap<>();
        set.put("element", "value");
        System.out.println(set.contains("element")); // prints "true"
    }
}