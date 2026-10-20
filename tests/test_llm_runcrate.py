import json

import llm

import llm_runcrate

MODELS = [
    {
        "id": "deepseek-ai/DeepSeek-V3.2",
        "input_modalities": ["text"],
        "output_modalities": ["text"],
        "supported_features": ["tools", "json_mode", "structured_outputs"],
    },
    {
        "id": "Qwen/Qwen3-VL-8B-Instruct",
        "input_modalities": ["text", "image"],
        "output_modalities": ["text"],
        "supported_features": [],
    },
    {
        "id": "openai/whisper-large-v3",
        "input_modalities": ["audio"],
        "output_modalities": ["text"],
        "supported_features": [],
    },
]


def test_registers_text_models(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_USER_PATH", str(tmp_path))
    (tmp_path / "runcrate_models.json").write_text(json.dumps(MODELS))
    ids = {m.model_id: m for m in llm.get_models()}
    chat = ids["runcrate/deepseek-ai/DeepSeek-V3.2"]
    assert chat.api_base == "https://api.runcrate.ai/v1"
    assert chat.model_name == "deepseek-ai/DeepSeek-V3.2"
    assert chat.supports_tools and chat.supports_schema
    assert chat.needs_key == "runcrate" and chat.key_env_var == "RUNCRATE_API_KEY"
    assert ids["runcrate/Qwen/Qwen3-VL-8B-Instruct"].attachment_types
    assert "runcrate/openai/whisper-large-v3" not in ids
