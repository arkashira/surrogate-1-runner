import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class java_formatter_test {

    @Test
    public void testSimpleClassFormatting() {
        String unformatted = "public class Foo{public void bar(){System.out.println(\"hi\");}}";
        String expected = """
                public class Foo{
                    public void bar(){
                        System.out.println("hi");
                    }
                }""";

        String actual = java_formatter.format(unformatted);
        assertEquals(expected, actual);
    }

    @Test
    public void testIndentationAndBlankLines() {
        String unformatted = """
                public class Sample{
                public static void main(String[] args){
                if(true){
                System.out.println("true");
                }
                }
                }""";

        String expected = """
                public class Sample{
                    public static void main(String[] args){
                        if(true){
                            System.out.println("true");
                        }
                    }
                }""";

        String actual = java_formatter.format(unformatted);
        assertEquals(expected, actual);
    }

    @Test
    public void testNullInputThrows() {
        assertThrows(IllegalArgumentException.class, () -> java_formatter.format(null));
    }
}