# pepkio-ligo-ratio-calc

Calculate exact insert-to-vector molar stoichiometry, required DNA masses, and reaction pipetting volumes for molecular cloning protocols.

# What It Does

`pepkio-ligo-ratio-calc` simplifies DNA ligation reaction planning by determining the required insert mass (in nanograms) and stock solution volumes (in microliters) needed for target insert-to-vector molar ratios (e.g., 1:1, 3:1, 5:1, 10:1). It performs automated length-to-mass conversions, handles single or multi-insert assemblies, and validates whether required DNA volumes fit within total reaction limits.

# Features

* **Multi-Ratio Calculations**: Computes required insert mass and pipetting volumes across multiple target molar ratios simultaneously.
* **Volumetric Feasibility Validation**: Checks reaction volume budgets (vector, insert, buffer, enzyme, water) and alerts when stock concentrations are insufficient.
* **Flexible Unit Parsing**: Accepts vector and insert lengths in base pairs (bp) or kilobases (kb), and DNA concentrations in ng/µL or µg/mL.
* **Multi-Insert & Assembly Support**: Accommodates cohesive-end, blunt-end, TA cloning, and multi-fragment assembly workflows.
* **Python API & CLI**: Provides a typed Python SDK (`PepkioClient`) and a command-line interface (`pepkio-ligo-ratio-calc`).

# Installation

```bash
pip install pepkio-ligo-ratio-calc
```

# Quick Example

```python
import os
from pepkio_ligo_ratio_calc import PepkioClient

api_key = os.getenv("PEPKIO_API_KEY")

with PepkioClient(api_key=api_key) as client:
    result = client.run({
        "mode": "standard",
        "cloning_preset": "sticky_end",
        "vector_size": 3000,
        "vector_size_unit": "bp",
        "vector_concentration": 50,
        "vector_conc_unit": "ng_uL",
        "vector_mass_ng": 50,
        "reaction_volume_ul": 10,
        "buffer_volume_ul": 1,
        "enzyme_volume_ul": 1,
        "ratios": [1, 3, 5],
        "inserts": [
            {
                "id": "ins1",
                "name": "Target Gene Insert",
                "size": 1000,
                "size_unit": "bp",
                "concentration": 20,
                "conc_unit": "ng_uL"
            }
        ]
    })
    
    print("Run Status:", result.status)
    print("Pipetting Plan:", result.result)
```

# Typical Use Cases

* **Cohesive-End (Sticky-End) Subcloning**: Determine insert mass for 3:1 or 5:1 molar ratios when ligating restriction digest products into linearized vectors.
* **Blunt-End PCR Fragment Ligation**: Scale insert stoichiometry (5:1 to 10:1) to optimize bimolecular collision rates for blunt-ended fragments.
* **Multi-Fragment & Modular Assembly**: Calculate balanced fragment masses for dual-insert ligations, Gibson Assembly, or Golden Gate cloning.
* **Volume Constraint Validation**: Verify if low-concentration DNA preparations can fit into standard 10 µL or 20 µL T4 ligase reactions without exceeding volume budgets.

# Scientific Background

DNA ligation kinetics depend on relative molar end concentrations rather than raw mass concentrations. Molar amounts of double-stranded DNA are calculated from mass and fragment length using the average dsDNA molecular weight (~650 Da/bp):

$$\text{pmol dsDNA} = \frac{\text{Mass (ng)} \times 1000}{\text{Length (bp)} \times 650}$$

To achieve a target insert-to-vector molar ratio ($R$), the required insert mass is determined by:

$$\text{Insert Mass (ng)} = \text{Vector Mass (ng)} \times \left( \frac{\text{Insert Size (bp)}}{\text{Vector Size (bp)}} \right) \times R$$

Pipetting volume is calculated as $\text{Insert Mass (ng)} / \text{Insert Concentration (ng/\mu L)}$. Total volume is completed with nuclease-free water after accounting for fixed buffer, enzyme, and vector volumes.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/ligo-ratio-calc

The web interface features real-time volume budget visualization, cloning preset selection, shareable permalinks, and printable benchtop worksheets.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-ligo-ratio-calc

Web Application: https://www.pepkio.com/tools/ligo-ratio-calc

Source code and issue tracking are available on GitHub.

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro). See https://www.pepkio.com for additional tools and services.

# Keywords

* ligation ratio calculator
* DNA ligation calculator
* insert to vector ratio
* molar ratio calculator
* molecular cloning calculator
* restriction subcloning
* T4 DNA ligase volume
* insert mass calculation
* sticky end ligation
* blunt end ligation
* TA cloning ratio
* Gibson assembly ratio
* Golden Gate cloning
* dsDNA mass to pmol
* ligation reaction volume
* vector insert stoichiometry
* DNA pipetting scheme
* ligation volume budget
* cloning reaction setup
* plasmid vector backbones
* PCR product ligation
* recombinant DNA cloning
* T4 ligase reaction buffer
* DNA concentration ng/uL
* vector self-ligation
* molecular biology calculator
* wet lab protocol calculator

* calculate insert to vector molar ratio
* how to calculate DNA ligation volumes
* insert mass formula base pairs to nanograms
* sticky end ligation molar ratio 3 to 1
* blunt end ligation insert vector ratio 5 to 1
* calculate ligation mix for 10 uL total volume
* how to convert ng to pmol for dsDNA
* multi fragment Gibson assembly molar ratio
* volumetric feasibility check for DNA ligation
* calculating T4 DNA ligase and buffer volumes
* troubleshooting low transformation efficiency after ligation
* how to prevent vector self ligation background
