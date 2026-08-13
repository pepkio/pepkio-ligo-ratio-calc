# pepkio-ligo-ratio-calc

Python client library and CLI for the Pepkio **ligo-ratio-calc** tool (Ligation Ratio Calculator).

## Installation

```bash
pip install pepkio-ligo-ratio-calc
```

## Quick Start

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
                "name": "Insert",
                "size": 1000,
                "size_unit": "bp",
                "concentration": 20,
                "conc_unit": "ng_uL"
            }
        ]
    })
    print(result.result)
```
