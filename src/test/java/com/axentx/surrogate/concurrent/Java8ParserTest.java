package com.axentx.surrogate.concurrent;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.List;

public class Java8ParserTest {
    @Test
    public void testParseDefaultMethods() {
        String sourceCode = "interface MyInterface {\n" +
                           "    default void myDefaultMethod() {\n" +
                           "        System.out.println(\"Default method\");\n" +
                           "    }\n" +
                           "}";

        Java8Parser parser = new Java8Parser();
        List<DefaultMethodInfo> defaultMethods = parser.parseDefaultMethods(sourceCode);

        assertEquals(1, defaultMethods.size());
        assertEquals("myDefaultMethod", defaultMethods.get(0).getMethodName());
    }
}