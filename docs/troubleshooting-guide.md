# Troubleshooting Guide for CFD Simulations

## Purpose
This guide provides a concise, step‑by‑step process for diagnosing and resolving the most common errors encountered when running CFD simulations with the **surrogate‑1** framework. It is designed to help users of all experience levels quickly identify the root cause and apply the appropriate fix.

---

## Table of Contents
1. [Common CFD Errors](#common-cfd-errors)
2. [Step‑by‑Step Troubleshooting Process](#step-by-step-troubleshooting-process)
3. [Quick Reference Cheat‑Sheet](#quick-reference-cheat-sheet)
4. [Further Resources](#further-resources)

---

## 1. Common CFD Errors

| Error Category | Typical Symptoms | Likely Cause |
|----------------|------------------|--------------|
| **Mesh Issues** | Divergence, non‑physical pressure spikes | Poor mesh quality, too coarse, or inappropriate boundary conditions |
| **Solver Instabilities** | Solver fails to converge, oscillatory residuals | Incorrect time step, under‑resolved physics, or numerical scheme mismatch |
| **Physics Model Errors** | Negative densities, unrealistic temperatures | Wrong turbulence model, missing source terms, or incompatible material properties |
| **Boundary Condition Misconfigurations** | Unexpected flow patterns, stagnation points | Incorrect inlet/outlet settings, missing wall functions |
| **File/Path Errors** | Simulation aborts with “file not found” | Wrong file paths, missing input files, or permission issues |
| **Resource Constraints** | Out‑of‑memory, CPU throttling | Insufficient RAM/CPU, overly large domain, or inefficient solver settings |
| **Software Bugs** | Unexpected crashes, segmentation faults | Bugs in the CFD solver or in the surrogate‑1 wrapper |

> **Note:** The guide focuses on the top 80 % of these errors, which cover the majority of user issues.

---

## 2. Step‑by‑Step Troubleshooting Process

> **Step 0 – Preparation**  
> 1. Verify that the simulation input files are complete and correctly referenced.  
> 2. Ensure you are using the latest version of the surrogate‑1 runner (`git pull`).  
> 3. Check system resources (RAM, CPU, disk space).

> **Step 1 – Validate Mesh**  
> 1. Run the mesh checker (`meshcheck -i meshfile`).  
> 2. Inspect mesh quality metrics (skewness, orthogonality).  
> 3. If metrics exceed thresholds, refine the mesh or adjust element sizing.

> **Step 2 – Inspect Boundary Conditions**  
> 1. Open the boundary condition file (`boundary_conditions.yaml`).  
> 2. Confirm that all required boundaries are defined and that values are physically reasonable.  
> 3. For inlet/outlet, ensure velocity/pressure values are within expected ranges.

> **Step 3 – Verify Physics Models**  
> 1. Check the turbulence model selection (`turbulence.yaml`).  
> 2. Confirm that material properties (density, viscosity) are defined for all regions.  
> 3. If using multiphase, ensure phase fractions sum to 1.

> **Step 4 – Run a Short Test Simulation**  
> 1. Reduce the domain or use a coarser mesh.  
> 2. Execute the solver for a few time steps (`simulate -t 10`).  
> 3. Monitor residuals and check for divergence or oscillations.

> **Step 5 – Analyze Solver Output**  
> 1. Look at the log file (`solver.log`).  
> 2. Identify any “non‑convergent” warnings or “negative pressure” errors.  
> 3. Use the diagnostic script (`diagnose.js`) to automatically flag common issues.

> **Step 6 – Apply Fixes**  
> 1. If mesh quality is low, refine or remesh.  
> 2. If boundary conditions are wrong, correct the values.  
> 3. If physics models are incompatible, switch to a more suitable model.  
> 4. If resource limits are hit, increase RAM/CPU or reduce domain size.

> **Step 7 – Re‑run and Validate**  
> 1. Run the full simulation again.  
> 2. Verify that residuals converge and that output fields are physically plausible.  
> 3. Compare results against benchmark data if available.

> **Step 8 – Document the Issue**  
> 1. Record the error message, steps taken, and final solution in the project’s issue tracker.  
> 2. If the issue persists, open a new ticket with the logs and configuration files.

---

## 3. Quick Reference Cheat‑Sheet

| Symptom | Quick Fix |
|---------|-----------|
| **Solver diverges** | Reduce time step, increase relaxation factors |
| **Negative density** | Check material property tables |
| **High residuals** | Refine mesh, adjust solver tolerances |
| **File not found** | Verify file paths, check permissions |
| **Out‑of‑memory** | Reduce domain size, increase swap, or use a larger instance |

---

## 4. Further Resources

* **Surrogate‑1 Documentation** – https://github.com/axentx/surrogate-1  
* **CFD Solver Manual** – https://example.com/cfd-solver-manual  
* **Mesh Quality Guidelines** – https://example.com/mesh-quality  
* **Community Forum** – https://forum.axentx.com  

--- 

*Prepared by the Surrogate‑1 Support Team – 2026-05-13*