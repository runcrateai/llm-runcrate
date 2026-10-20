"""LLM plugin for Runcrate's OpenAI-compatible inference API."""

import json
import time

import httpx
import llm
from llm.default_plugins.openai_models import AsyncChat, Chat

API_BASE = "https://api.runcrate.ai/v1"
CACHE_SECONDS = 24 * 60 * 60


class _RuncrateMixin:
    needs_key = "runcrate"
    key_env_var = "RUNCRATE_API_KEY"

    def __str__(self):
        return "Runcrate: {}".format(self.model_id)


class RuncrateChat(_RuncrateMixin, Chat):
    pass


class AsyncRuncrateChat(_RuncrateMixin, AsyncChat):
    pass


def _cache_path():
    return llm.user_dir() / "runcrate_models.json"


def fetch_models(force: bool = False) -> list:
    """Text models from GET /v1/models, cached for a day in the llm user dir."""
    path = _cache_path()
    if not force and path.exists() and time.time() - path.stat().st_mtime < CACHE_SECONDS:
        return json.loads(path.read_text())
    try:
        response = httpx.get(API_BASE + "/models", timeout=10, follow_redirects=True)
        response.raise_for_status()
        models = [
            m for m in response.json()["data"] if "text" in m.get("output_modalities", [])
        ]
    except (httpx.HTTPError, KeyError, ValueError):
        return json.loads(path.read_text()) if path.exists() else []
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(models))
    return models


def _kwargs(model: dict) -> dict:
    features = set(model.get("supported_features") or [])
    return dict(
        model_id="runcrate/" + model["id"],
        model_name=model["id"],
        api_base=API_BASE,
        vision="image" in (model.get("input_modalities") or []),
        supports_tools="tools" in features,
        supports_schema="structured_outputs" in features,
    )


@llm.hookimpl
def register_models(register):
    for model in fetch_models():
        if "text" not in (model.get("input_modalities") or []):
            continue  # speech-to-text models need audio input
        kwargs = _kwargs(model)
        register(RuncrateChat(**kwargs), AsyncRuncrateChat(**kwargs))


@llm.hookimpl
def register_commands(cli):
    @cli.group()
    def runcrate():
        "Commands for Runcrate models"

    @runcrate.command()
    def refresh():
        "Refresh the cached list of Runcrate models"
        models = fetch_models(force=True)
        print("{} Runcrate text models cached".format(len(models)))
