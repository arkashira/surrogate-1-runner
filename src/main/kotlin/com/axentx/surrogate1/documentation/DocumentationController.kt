package com.axentx.surrogate1.documentation

import com.axentx.surrogate1.models.Documentation
import com.axentx.surrogate1.models.DocumentationVersion
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/documentation")
class DocumentationController(
    private val documentationService: DocumentationService
) {

    @PostMapping
    fun saveDocumentation(@RequestBody documentation: Documentation): Documentation {
        return documentationService.saveDocumentation(documentation)
    }

    @GetMapping("/{id}")
    fun getDocumentationById(@PathVariable id: Long): Documentation? {
        return documentationService.getDocumentationById(id)
    }

    @GetMapping("/search")
    fun searchDocumentation(@RequestParam query: String): List<Documentation> {
        return documentationService.searchDocumentation(query)
    }

    @PostMapping("/version")
    fun saveDocumentationVersion(@RequestBody version: DocumentationVersion): DocumentationVersion {
        return documentationService.saveDocumentationVersion(version)
    }

    @GetMapping("/versions/{documentationId}")
    fun getDocumentationVersions(@PathVariable documentationId: Long): List<DocumentationVersion> {
        return documentationService.getDocumentationVersions(documentationId)
    }
}