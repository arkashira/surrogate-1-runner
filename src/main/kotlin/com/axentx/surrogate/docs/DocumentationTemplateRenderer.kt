package com.axentx.surrogate.docs

import com.axentx.surrogate.model.FunctionOverload
import com.axentx.surrogate.utils.LinkGenerator
import com.github.mustachejava.DefaultMustacheFactory
import com.github.mustachejava.MustacheFactory
import java.io.StringWriter

class DocumentationTemplateRenderer(
    private val mustacheFactory: MustacheFactory = DefaultMustacheFactory()
) {

    /**
     * Renders documentation for the supplied list of function overloads.
     *
     * @param overloads List of FunctionOverload objects to document.
     * @return Rendered documentation as an HTML string.
     */
    fun render(overloads: List<FunctionOverload>): String {
        // 1. Load the Mustache template
        val template = mustacheFactory.compile("templates/documentation.mustache")

        // 2. Build the model map for the template
        // We transform our Domain Models into a Map structure compatible with Mustache
        val model = mapOf(
            "functions" to overloads.map { overload ->
                val paramTypes = overload.signature.parameterTypes
                
                mapOf(
                    "name" to overload.functionName,
                    "signature" to overload.signature.toString(),
                    // Generate the unique anchor link using our robust utility
                    "overloadLink" to LinkGenerator.generateUniqueLink(overload.functionName, paramTypes),
                    "parameters" to paramTypes.map { type ->
                        mapOf("type" to type)
                    }
                )
            }
        )

        // 3. Execute template
        val writer = StringWriter()
        template.execute(writer, model).flush()
        return writer.toString()
    }
}