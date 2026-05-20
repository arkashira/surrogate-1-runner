package com.axentx.surrogate1

import org.jetbrains.dokka.base.DokkaBase
import org.jetbrains.dokka.base.transformers.pages.comments.CommentTransformer
import org.jetbrains.dokka.model.DModule
import org.jetbrains.dokka.pages.ContentNode
import org.jetbrains.dokka.pages.PageNode
import org.jetbrains.dokka.plugability.DokkaContext
import org.jetbrains.dokka.plugability.plugin
import org.jetbrains.dokka.plugability.querySingle

class OverloadResolverDokkaPlugin : DokkaBase() {
    override fun doExecute(context: DokkaContext) {
        val transformer = context.plugin<OverloadResolverDokkaPlugin>().querySingle { overloadResolverTransformer }
        context.modules.forEach { module ->
            transformModule(module, transformer)
        }
    }

    private fun transformModule(module: DModule, transformer: CommentTransformer) {
        module.documentation.forEach { page ->
            page.content = transformer.transform(page.content)
        }
    }
}

val DokkaContext.overloadResolverTransformer: CommentTransformer
    get() = CommentTransformer { node ->
        when (node) {
            is ContentNode -> resolveOverloads(node)
            else -> node
        }
    }

private fun resolveOverloads(node: ContentNode): ContentNode {
    // Implement logic to resolve overloads within the documentation nodes
    return node
}