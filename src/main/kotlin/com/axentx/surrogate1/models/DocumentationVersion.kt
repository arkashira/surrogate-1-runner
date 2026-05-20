package com.axentx.surrogate1.models

import javax.persistence.*

@Entity
@Table(name = "documentation_version")
data class DocumentationVersion(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @ManyToOne
    @JoinColumn(name = "documentation_id", nullable = false)
    val documentation: Documentation,

    @Column(nullable = false)
    val version: String,

    @Column(nullable = false, columnDefinition = "TEXT")
    val content: String,

    @Column(nullable = false)
    val timestamp: Long
)