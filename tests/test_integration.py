"""Integration tests running against live Pepkio API endpoints."""

from __future__ import annotations

from pathlib import Path

import pytest
from dotenv import load_dotenv

from pepkio_ligo_ratio_calc import PepkioClient
from pepkio_ligo_ratio_calc.config import resolve_api_key, resolve_base_url

# Search parent directories for .env file
current = Path(__file__).resolve()
parents = [
    current.parent,
    current.parent.parent,
    current.parent.parent.parent,
    current.parent.parent.parent.parent,
]
for parent in parents:
    env_path = parent / ".env"
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)
        break

BASE_URL = resolve_base_url()
API_KEY = resolve_api_key(base_url=BASE_URL)


@pytest.mark.skipif(not API_KEY, reason="PEPKIO_API_KEY / LOCAL_PEPKIO_API_KEY not set")
def test_live_manifest_and_run() -> None:
    """Integration test executing manifest fetch, tool run, and get_run against live API."""
    with PepkioClient(api_key=API_KEY, base_url=BASE_URL) as client:
        # 1. Fetch manifest
        manifest = client.get_manifest()
        assert manifest.get("tool_id") == "ligo-ratio-calc"
        assert "examples" in manifest
        assert len(manifest["examples"]) > 0

        # 2. Get example input
        example_name = manifest["examples"][0]["name"]
        inp = client.get_example_input(example_name)
        assert isinstance(inp, dict)

        # 3. Run tool
        run_res = client.run(inp, label="integration-test")
        assert run_res.status == "completed"
        assert run_res.run_id is not None
        assert run_res.result is not None
        assert "columns" in run_res.result

        # 4. Get run by ID
        fetched_res = client.get_run(run_res.run_id)
        assert fetched_res.run_id == run_res.run_id
        assert fetched_res.status == "completed"
        assert fetched_res.result is not None
