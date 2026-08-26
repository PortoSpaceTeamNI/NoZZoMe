---
title: "NoZZoMe: An Open-Source Framework for MOC-Assisted Parametric Bell-Nozzle Optimization"
tags:
  - Python
  - rocket propulsion
  - method of characteristics
  - genetic algorithm
  - nozzle design
authors:
  - name: Rafael Lino
    affiliation: 1
  - name: Francisco Ferreira
    affiliation: 2
affiliations:
  - name: Porto Space Team, Porto, Portugal
    index: 1
  - name: Department of Mechanical Engineering, Faculty of Engineering, University of Porto, Porto, Portugal
    index: 2
date: 26 August 2026
bibliography: paper.bib
---

# Summary

A rocket nozzle converts the thermal and pressure energy of combustion gases into a
high-speed exhaust jet. Its contour affects thrust, efficiency, length, and the risk
of undesirable flow behaviour, but exploring alternative contours commonly requires
several disconnected tools. NoZZoMe is an open-source Python application for
generating, analysing, and optimizing axisymmetric single-bell rocket-nozzle
geometries. It combines thermochemical properties, parametric geometry,
reduced-order flow and loss models, a Method of Characteristics (MOC) analysis,
genetic optimization, interactive visualization, and machine-readable export in one
reproducible workflow.

NoZZoMe is intended for researchers, student rocketry teams, and preliminary-design
engineers who need to inspect the assumptions and intermediate results of a nozzle
study. Users can operate it through a desktop interface or a shared Python simulation
API. The software is deliberately positioned between ideal sizing calculations and
mesh-refined computational fluid dynamics (CFD): it supports rapid and transparent
design comparison but is not a qualification tool.

# Statement of need

Preliminary nozzle design involves more than drawing a divergent wall. An operating
point must be connected to thermochemical properties and an expansion ratio; a
geometrically continuous contour must then be evaluated for inviscid expansion,
multidimensional turning, boundary-layer displacement, wall friction, and performance
losses. These calculations are often split across thermochemical programs,
spreadsheets, contour utilities, optimization scripts, and CFD packages. This
fragmentation makes assumptions difficult to trace and encourages inconsistent
evaluation paths between manually generated and optimized designs.

NoZZoMe addresses this gap with an inspectable workflow in which the graphical
interface, examples, and optimizers use the same maintained simulation components.
It supports pressure-matched expansion sizing, continuous convergent-throat-bell
geometry, quasi-one-dimensional profiles, adiabatic thermal diagnostics,
BLIMP-inspired boundary-layer closures, prescribed-wall axisymmetric MOC analysis,
and genetic optimization. The resulting contours and physical fields can be exported
as CSV and JSON for independent analysis, CAD preparation, and reproducible research.
The validity limits of every reduced-order model are documented, and final designs
remain subject to CFD, structural and thermal assessment, manufacturing review, and
experimental validation.

# State of the field

NoZZoMe occupies a different level of scope and fidelity from established propulsion,
optimization, and CFD tools. Its closest relationships are summarized below.

| Software | Primary role | Relationship to NoZZoMe |
|:--|:--|:--|
| RPA [@rpa] | Broad preliminary chemical-rocket-engine analysis, including performance, chamber, nozzle, and thermal calculations | Broader engine-level scope; NoZZoMe concentrates on an inspectable Python workflow for single-bell contour generation and optimization |
| RocketCEA [@gordon1994; @rocketcea] | Python access to NASA CEA thermochemistry and ideal rocket performance | Used by NoZZoMe as a backend; NoZZoMe adds continuous geometry, prescribed-wall MOC, viscous corrections, and design search |
| OpenMDAO [@gray2019openmdao] | General multidisciplinary analysis and optimization architecture | A general orchestration framework rather than a nozzle-specific modelling application |
| SU2 [@economon2016su2] | Mesh-based multiphysics simulation and PDE-constrained design | A higher-fidelity and higher-cost downstream option for checking shortlisted NoZZoMe contours |

Table: Positioning of NoZZoMe relative to complementary engineering software.

Contributing the complete workflow to any one of these projects would mix a
specialized nozzle-design application with either a thermochemical backend, a general
workflow framework, or a mesh-based CFD suite. NoZZoMe instead composes established
packages where appropriate and contributes the nozzle-specific geometry, physical
closures, verification logic, interactive workflow, and exact-finalist optimization
strategy. It complements rather than replaces the cited tools.

# Software design

The overall analysis and optimization sequence is summarized in
\autoref{fig:workflow}.

## Shared physical evaluation path

The central architectural decision is to keep one physical evaluation path across
interactive simulation and optimization. Operating conditions, engine pre-sizing
quantities, fixed contour inputs, and genetic variables are represented separately so
that the optimizer cannot silently change quantities that should remain fixed. The
maintained Python packages separate geometry, RocketCEA access, flow reconstruction,
thermal diagnostics, boundary-layer integration, performance, MOC, optimization, and
export, while a shared simulation entry point coordinates the common reduced-order
analysis.

![NoZZoMe analysis and optimization workflow. Reduced-order and axisymmetric models
support the genetic search, while shortlisted designs undergo exact finalist
verification before visualization and export.](joss2.png){#fig:workflow width="100%"}


## Modelling and analysis capabilities

| Capability | Technical implementation | Principal output |
|:--|:--|:--|
| Thermochemistry and sizing | RocketCEA properties with pressure-matched expansion sizing | Throat and exit conditions, expansion ratio, ideal performance |
| Parametric geometry | Continuous convergent, throat, and single-bell contour construction | Wall coordinates and geometric design variables |
| Reduced-order analysis | Quasi-one-dimensional flow, adiabatic thermal diagnostics, wall friction, and integral boundary-layer models | Axial profiles, displacement effects, and loss estimates |
| Axisymmetric MOC | Prescribed-wall characteristic marching with characteristic-field visualization | Mach, pressure, flow-angle, and mass-conservation diagnostics |
| Design optimization | Genetic search with Quick, BLIMP-lite, or MOC-assisted evaluation | Ranked feasible geometries and an exactly verified finalist |
| Reproducibility | Shared API, desktop interface, automated tests, and CSV/JSON export | Repeatable studies and machine-readable results |

Table: Main technical capabilities exposed by the common NoZZoMe workflow.

## Multi-fidelity optimization and verification

Three optimization fidelities balance computational cost and physical detail. Quick
uses an integral boundary-layer closure, BLIMP-lite uses a resolved compressible
profile marcher, and MOC-assisted mode includes multidimensional turning. Because
refined MOC is too costly for every genetic candidate, a bounded piecewise-linear
surrogate is constructed from exact MOC evaluations. Shortlisted candidates are then
recomputed with exact coarse MOC, finalists on Fast or Precise meshes, and only an
exactly verified design is returned.

Verification prevents surrogate acceleration from concealing physical error. MOC
solutions are checked against the RocketCEA choking reference and for mass
conservation. Invalid geometry, non-finite states, predicted separation, or excessive
residuals are rejected. Numerical studies, retained CSV results, automated tests, and
continuous integration provide reproducible checks beyond the graphical interface.

## Interactive inspection

Representative outputs are shown in \autoref{fig:geometry} and
\autoref{fig:moc}. They expose the generated nozzle geometry and the
axisymmetric characteristic-field diagnostics.

![Parametric single-bell nozzle geometry: two-dimensional contour construction
and interactive three-dimensional surface visualization.](joss1.png){#fig:geometry width="95%"}

![Axisymmetric MOC diagnostics: Mach-number and static-pressure fields, exit
radial profiles, and mass-conservation verification.](joss3.png){#fig:moc width="95%"}

# Research impact statement

NoZZoMe originated in the Porto Space Team workflow for preliminary analysis of the
paraffin/nitrous-oxide hybrid propulsion system developed in the context of the
European Rocketry Challenge. Its evolution is publicly documented in a repository
with development activity since June 2025 and contributions from several team
members. Release v0.2.0 provides the first formal research-software snapshot
[@nozzomerelease2026].

The accompanying technical report documents the underlying geometric formulation,
physical models, verification procedures, and MOC-assisted optimization study
[@lino2026technicalreport]. Reproducible scripts in the repository regenerate the
principal model comparisons and convergence studies. In the reported reference case,
the Fast and Precise finalist meshes selected the same geometry, while the refined
study quantified the remaining performance difference and enforced independent
mass-flow thresholds. These materials demonstrate present research use by the
developers and provide auditable benchmarks for reuse, extension, and comparison by
other propulsion researchers. The public API, contribution guidelines, issue tracker,
GPL-3.0 license, tests, and machine-readable outputs are intended to support such use
beyond the original team.

# AI usage disclosure

OpenAI Codex, using GPT-5-family models available in August 2026, assisted with code
refactoring, test scaffolding, documentation organization, editorial review, and
drafting and copy-editing portions of this paper and the related technical report.
The human authors defined the research problem, selected the physical and numerical
models, made the architectural and scientific decisions, reviewed and edited all
AI-assisted material, and validated software behaviour and reported numerical results
against the documented equations, convergence studies, automated tests, and retained
outputs. The authors remain responsible for the accuracy, originality, licensing, and
scientific claims of the software and publications.

# Acknowledgements

The authors acknowledge the Porto Space Team and the Faculty of Engineering of the
University of Porto for the engineering context in which this work developed. The
authors received no specific external financial support for this work and declare no
competing interests.

# References
