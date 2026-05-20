package com.axentx.surrogate1.documentation

import com.axentx.surrogate1.models.Documentation
import com.axentx.surrogate1.models.DocumentationVersion
import com.axentx.surrogate1.repositories.DocumentationRepository
import com.axentx.surrogate1.repositories.DocumentationVersionRepository
import org.springframework.stereotype.Service

@Service
class DocumentationService(
    private val documentationRepository: DocumentationRepository,
    private val documentationVersionRepository: DocumentationVersionRepository
) {

    fun saveDocumentation(documentation: Documentation): Documentation {
        return documentationRepository.save(documentation)
    }

    fun getDocumentationById(id: Long): Documentation? {
        return documentationRepository.findById(id).orElse(null)
    }

    fun searchDocumentation(query: String): List<Documentation> {
        return documentationRepository.findByContentContaining(query)
    }

    fun saveDocumentationVersion(version: DocumentationVersion): DocumentationVersion {
        return documentationVersionRepository.save(version)
    }

    fun getDocumentationVersions(documentationId: Long): List<DocumentationVersion> {
        return documentationVersionRepository.findByDocumentationId(documentationId)
    }
}