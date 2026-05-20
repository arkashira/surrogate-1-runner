package com.axentx.surrogate1

import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class OverloadResolverTest {
    @Test
    fun `resolve function overloads`() {
        val resolver = OverloadResolver()
        val signature1 = FunctionSignature("Int", "foo", listOf("String", "Int"))
        val signature2 = FunctionSignature("Int", "foo", listOf("String", "String"))
        resolver.addFunctionSignature(signature1)
        resolver.addFunctionSignature(signature2)

        assertEquals("foo-0", resolver.getUniqueIdentifier(signature1))
        assertEquals("foo-1", resolver.getUniqueIdentifier(signature2))
    }
}