"""Unit tests for PepkioClient and CLI with mocked HTTP responses."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from click.testing import CliRunner

from pepkio_ligo_ratio_calc.cli import main
from pepkio_ligo_ratio_calc.client import PepkioClient
from pepkio_ligo_ratio_calc.config import DEFAULT_API_BASE_URL
from pepkio_ligo_ratio_calc.exceptions import PepkioAuthError, PepkioHTTPError, PepkioRunError

MOCK_MANIFEST: dict[str, Any] = {
    "tool_id": "ligo-ratio-calc",
    "title": "Ligation Ratio Calculator",
    "examples": [
        {
            "name": "sticky_3kb_1kb",
            "input": {
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
                        "conc_unit": "ng_uL",
                    }
                ],
            },
        }
    ],
}

MOCK_RUN_SUCCESS: dict[str, Any] = {
    "run_id": "test-run-123",
    "status": "completed",
    "result": {
        "mode": "standard",
        "columns": [{"ratio": 1, "feasible": True}],
    },
    "error": None,
    "result_url": "https://tools.pepkio.com/api/tools/v1/runs/test-run-123",
    "permalink": "https://tools.pepkio.com/r/test-run-123",
}

MOCK_RUN_ERROR: dict[str, Any] = {
    "run_id": "test-run-err",
    "status": "failed",
    "result": None,
    "error": {
        "code": "INVALID_INPUT",
        "message": "vector_size must be positive",
    },
}


def test_client_defaults() -> None:
    client = PepkioClient(api_key="test-key")
    assert client.base_url == DEFAULT_API_BASE_URL


def test_get_manifest() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tools/v1/tools/ligo-ratio-calc/manifest":
            return httpx.Response(200, json=MOCK_MANIFEST)
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    manifest = client.get_manifest()
    assert manifest["tool_id"] == "ligo-ratio-calc"
    assert client.list_examples() == ["sticky_3kb_1kb"]
    inp = client.get_example_input("sticky_3kb_1kb")
    assert inp["mode"] == "standard"


def test_run_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tools/v1/tools/ligo-ratio-calc/run":
            body = json.loads(request.content.decode())
            assert body["input"]["mode"] == "standard"
            return httpx.Response(200, json=MOCK_RUN_SUCCESS)
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    inp = MOCK_MANIFEST["examples"][0]["input"]
    res = client.run(inp, label="test-run")
    assert res.run_id == "test-run-123"
    assert res.status == "completed"
    assert res.result is not None


def test_get_run_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tools/v1/runs/test-run-123":
            return httpx.Response(200, json=MOCK_RUN_SUCCESS)
        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    res = client.get_run("test-run-123")
    assert res.run_id == "test-run-123"
    assert res.status == "completed"


def test_auth_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        err_body = {"error": {"code": "UNAUTHORIZED", "message": "Invalid token"}}
        return httpx.Response(401, json=err_body)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="invalid-key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    with pytest.raises(PepkioAuthError) as exc_info:
        client.get_manifest()
    assert exc_info.value.status_code == 401
    assert "Invalid token" in str(exc_info.value)


def test_http_500_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        err_body = {"error": {"code": "SERVER_ERROR", "message": "Internal Server Error"}}
        return httpx.Response(500, json=err_body)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    with pytest.raises(PepkioHTTPError) as exc_info:
        client.get_manifest()
    assert exc_info.value.status_code == 500


def test_run_error_body() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=MOCK_RUN_ERROR)

    transport = httpx.MockTransport(handler)
    client = PepkioClient(api_key="test-key", base_url="https://tools.pepkio.com")
    client._http = httpx.Client(base_url="https://tools.pepkio.com", transport=transport)

    with pytest.raises(PepkioRunError) as exc_info:
        client.run({"invalid": True})
    assert "vector_size must be positive" in str(exc_info.value)


def test_cli_manifest_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["manifest", "--help"])
    assert result.exit_code == 0
    assert "Fetch and print the tool manifest" in result.output
