package com.axentx.surrogate1.repositories

import com.axentx.surrogate1.models.Documentation
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface DocumentationRepository : JpaRepository<Documentation, Long> {
    fun findByContentContaining(query: String): List<Documentation>
}