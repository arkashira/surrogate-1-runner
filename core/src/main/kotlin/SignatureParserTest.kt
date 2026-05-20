import org.junit.Test
import kotlin.test.assertEquals

class SignatureParserTest {
    @Test
    fun testParseFunctionSignature() {
        val method = // create a PsiMethod instance
        val identifier = parseFunctionSignature(method)
        assertEquals("example-String-Int", generateOverloadIdentifier(method))
    }

    @Test
    fun testHandleTypeErasure() {
        val method = // create a PsiMethod instance
        val identifier = handleTypeErasure(method)
        assertEquals("example-String-Int", generateOverloadIdentifier(method))
    }

    @Test
    fun testHandleInlineClasses() {
        val method = // create a PsiMethod instance
        val identifier = handleInlineClasses(method)
        assertEquals("example-String-Int", generateOverloadIdentifier(method))
    }
}