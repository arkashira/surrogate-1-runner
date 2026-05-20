package com.axentx.surrogate1

import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class FunctionSignatureParserTest {
    @Test
    fun `parse function signature`() {
        val parser = FunctionSignatureParser()
        val signature = parser.parse("Int foo(String, Int)")
        assertEquals("Int", signature.returnType)
        assertEquals("foo", signature.name)
        assertEquals(listOf("String", "Int"), signature.parameters)
    }
}