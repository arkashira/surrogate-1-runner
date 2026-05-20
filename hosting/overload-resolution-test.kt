package hosting

import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class VersionedOverloadResolutionTest {

    @Test
    fun testAddAndGetOverloads() {
        val resolution = VersionedOverloadResolution()
        resolution.addOverload("1.0", "foo", "foo(int)")
        resolution.addOverload("1.0", "foo", "foo(String)")
        resolution.addOverload("2.0", "foo", "foo(Double)")

        assertEquals(listOf("foo(int)", "foo(String)"), resolution.getOverloads("1.0", "foo"))
        assertEquals(listOf("foo(Double)"), resolution.getOverloads("2.0", "foo"))
    }
}