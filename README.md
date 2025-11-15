## mcp

Minimal uv-managed Python CLI that now showcases both LangChain v1 prompting
and the Model Context Protocol (MCP) FastMCP helper.

### Requirements

- Python 3.12 (see `.python-version`)
- [uv](https://docs.astral.sh/uv/latest/) for dependency and virtualenv management
- Network access the first time you run `uv sync` so LangChain + MCP packages can
  be downloaded

### Setup

```bash
git clone <repo-url>
cd mcp
UV_CACHE_DIR=$PWD/.uv-cache uv sync
```

`uv sync` creates the local `.venv` using the locked dependencies in `uv.lock`.

### Run the CLI demo

```bash
UV_CACHE_DIR=$PWD/.uv-cache uv run mcp
```

The script prints four sections:

1. A LangChain-formatted chat transcript that shows how templated prompts work.
2. Sample MCP *resources* (a primer plus a templated deep dive).
3. Sample MCP *prompts* (the `orientation_prompt` onboarding helper).
4. Outputs from three sample FastMCP *tools*:
   - `spotlight` (friendly greeter)
   - `summarize` (first-sentence TL;DR)
   - `word_count` (quick payload sizing helper)

Use the sample as a base for building a real MCP server by replacing or expanding
the toy tools with your own handlers.
