package com.axentx.surrogate1.repositories

import com.axentx.surrogate1.models.DocumentationVersion
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface DocumentationVersionRepository : JpaRepository<DocumentationVersion, Long> {
    fun findByDocumentationId(documentationId: Long): List<DocumentationVersion>
}