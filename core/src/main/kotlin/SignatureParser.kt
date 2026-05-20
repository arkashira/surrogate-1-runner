import com.intellij.psi.PsiMethod
import com.intellij.psi.PsiParameter
import com.intellij.psi.PsiType

data class OverloadIdentifier(val name: String, val parameters: List<String>)

fun parseFunctionSignature(method: PsiMethod): OverloadIdentifier {
    val name = method.name
    val parameters = method.parameters.map { parameter ->
        val type = parameter.type
        val typeName = type.text
        typeName
    }
    return OverloadIdentifier(name, parameters)
}

fun generateOverloadIdentifier(method: PsiMethod): String {
    val identifier = parseFunctionSignature(method)
    return "${identifier.name}-${identifier.parameters.joinToString("-")}"
}

fun handleTypeErasure(method: PsiMethod): OverloadIdentifier {
    // For simplicity, assume type erasure is handled by ignoring the type
    return parseFunctionSignature(method)
}

fun handleInlineClasses(method: PsiMethod): OverloadIdentifier {
    // For simplicity, assume inline classes are handled by ignoring the class
    return parseFunctionSignature(method)
}