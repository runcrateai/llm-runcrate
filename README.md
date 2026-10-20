# llm-runcrate

[LLM](https://llm.datasette.io/) plugin for [Runcrate](https://www.runcrate.ai/?utm_source=github-llm-runcrate&utm_medium=directory&utm_campaign=gpu_pricing): 200+ open models (DeepSeek, Qwen, Llama, Kimi, gpt-oss and more) behind one OpenAI-compatible API, billed per token from one prepaid balance.

## Install

```bash
llm install git+https://github.com/aeonmindai/llm-runcrate
```

## Configure

Create an API key ([docs](https://www.runcrate.ai/docs/account/api-keys?utm_source=github-llm-runcrate&utm_medium=directory&utm_campaign=gpu_pricing)), then:

```bash
llm keys set runcrate
# or: export RUNCRATE_API_KEY=...
```

## Use

```bash
llm models list | grep runcrate/
llm -m runcrate/deepseek-ai/DeepSeek-V3.2 "Explain LoRA fine-tuning in one sentence"
llm -m runcrate/Qwen/Qwen3-VL-8B-Instruct "Describe this" -a photo.jpg
llm chat -m runcrate/moonshotai/Kimi-K2.6
```

Models that support tools and JSON schemas work with `--tool`/`-T` and `--schema`. The model list comes from `https://api.runcrate.ai/v1/models` and is cached for a day; refresh it with `llm runcrate refresh`.

Python:

```python
import llm

model = llm.get_model("runcrate/deepseek-ai/DeepSeek-V3.2")
print(model.prompt("Name three uses for an H100").text())
```

Models and per-token prices: [runcrate.ai/inference/pricing](https://www.runcrate.ai/inference/pricing?utm_source=github-llm-runcrate&utm_medium=directory&utm_campaign=gpu_pricing). The same account rents GPUs by the hour, and the remote MCP server `https://mcp.runcrate.ai/mcp` (OAuth sign-in, no key) lets agents launch them ([setup](https://www.runcrate.ai/docs/mcp/setup?utm_source=github-llm-runcrate&utm_medium=directory&utm_campaign=mcp)).

## Development

```bash
uv run --group test pytest
```

## License

MIT, Aeonmind LLC.
