package com.axentx.surrogate1.models

import javax.persistence.*

@Entity
@Table(name = "documentation")
data class Documentation(
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    val id: Long = 0,

    @Column(nullable = false)
    val title: String,

    @Column(nullable = false, columnDefinition = "TEXT")
    val content: String,

    @Column(nullable = false)
    val version: String
)