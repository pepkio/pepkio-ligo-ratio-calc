# pepkio-ligo-ratio-calc

Python client library and CLI for the Pepkio **ligo-ratio-calc** tool (Ligation Ratio Calculator).

## Installation

```bash
pip install pepkio-ligo-ratio-calc
```

Or with `uv`:

```bash
uv add pepkio-ligo-ratio-calc
```

## Environment Setup

Set your Pepkio API key:

```bash
export PEPKIO_API_KEY="your_api_key_here"
```

To target a local development server during testing:

```bash
export PEPKIO_API_BASE_URL="https://tools.localtest.me"
export LOCAL_PEPKIO_API_KEY="your_local_key_here"
```

## Python API Usage

```python
import os
from pepkio_ligo_ratio_calc import PepkioClient

api_key = os.getenv("PEPKIO_API_KEY")

with PepkioClient(api_key=api_key) as client:
    # 1. Fetch manifest
    manifest = client.get_manifest()

    # 2. Run calculation
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
    print("Status:", result.status)
    print("Result:", result.result)
```

## CLI Usage

```bash
# Print tool manifest
pepkio-ligo-ratio-calc manifest

# Run built-in manifest example
pepkio-ligo-ratio-calc run --example sticky_3kb_1kb

# Run with inline JSON input
pepkio-ligo-ratio-calc run --input-json '{"mode":"standard","cloning_preset":"sticky_end","vector_size":3000,"vector_size_unit":"bp","vector_concentration":50,"vector_conc_unit":"ng_uL","vector_mass_ng":50,"reaction_volume_ul":10,"buffer_volume_ul":1,"enzyme_volume_ul":1,"ratios":[1,3,5],"inserts":[{"id":"ins1","name":"Insert","size":1000,"size_unit":"bp","concentration":20,"conc_unit":"ng_uL"}]}'
```
