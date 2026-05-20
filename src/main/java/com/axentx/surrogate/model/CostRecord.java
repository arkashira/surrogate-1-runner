package com.axentx.surrogate.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "cost_record")
public class CostRecord {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false) private String vmType;
    @Column(nullable = false) private String region;
    @Column(nullable = false) private int instanceCount;
    @Column(nullable = false) private BigDecimal totalCost;
    @Column(nullable = false) private LocalDate date;

    // Constructors, getters, setters omitted for brevity
}