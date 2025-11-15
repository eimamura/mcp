"""Command-line demo marrying LangChain prompts with core MCP concepts."""

from __future__ import annotations

import asyncio
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from mcp.server.fastmcp import FastMCP


MCP_SERVER = FastMCP("toolkit-demo")


@MCP_SERVER.tool()
def spotlight(name: str) -> str:
    """Friendly greeter so new users see basic tool wiring."""

    return f"MCP spotlight -> Hello, {name}!"


@MCP_SERVER.tool()
def summarize(text: str) -> str:
    """Return a lightweight summary without external dependencies."""

    sentences = text.strip().split(".")
    first_sentence = sentences[0].strip()
    if not first_sentence:
        return "No content to summarize."
    return f"Summary: {first_sentence}."


@MCP_SERVER.tool()
def word_count(text: str) -> dict[str, int]:
    """Count words so toolchains can inspect payload sizes."""

    words = [chunk for chunk in text.split() if chunk]
    return {"words": len(words)}


@MCP_SERVER.resource(
    "resource://mcp/primer",
    title="Core MCP Concepts",
    description="Explains resources, tools, and prompts at a glance",
)
def mcp_primer_resource() -> str:
    """Textual primer describing the three MCP capability types."""

    return (
        "Resources: file-like data surfaces exposed via URIs so agents can read "
        "context such as docs or API output.\n"
        "Tools: callable functions (with human approval) that let an LLM trigger "
        "side effects or computations.\n"
        "Prompts: curated templates that standardize multi-step instructions for "
        "common workflows."
    )


@MCP_SERVER.resource(
    "resource://mcp/resources/{capability}",
    title="Capability Deep Dive",
    description="Explains how to use a specific MCP capability",
)
def capability_resource(capability: str) -> str:
    """Template resource returning details for a named capability."""

    sections = {
        "resources": "Stream large context or structured payloads via URIs.",
        "tools": "Wrap business logic so an LLM can request actions on demand.",
        "prompts": "Share proven instructions so users are productive instantly.",
    }
    return sections.get(capability.lower(), "Unknown capability.")


@MCP_SERVER.prompt(
    title="MCP Orientation Prompt",
    description="Guides an LLM through verifying MCP resources/tools/prompts",
)
def orientation_prompt(project: str) -> list[dict[str, str]]:
    """Sample prompt definition used to orient new MCP projects."""

    return [
        {
            "role": "system",
            "content": "You are an MCP onboarding assistant who references "
            "registered resources before calling tools.",
        },
        {
            "role": "user",
            "content": (
                f"Project: {project}.\n"
                "1. Read resource://mcp/primer.\n"
                "2. Ask the `spotlight` tool for a greeting.\n"
                "3. Summarize findings for the operator."
            ),
        },
    ]


def _render_prompt(name: str) -> str:
    """Build a short scripted conversation highlighting LangChain v1."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You introduce the Model Context Protocol to new users."),
            ("human", "Greet {name} and mention MCP."),
        ]
    )
    messages = prompt.format_messages(name=name)
    lines = [f"{message.type.title()}: {message.content}" for message in messages]
    return "\n".join(lines)


def _sample_mcp_tool_output(target: str) -> str:
    """Call the in-process FastMCP tools to show what they return."""

    outputs = [
        ("spotlight", spotlight(target)),
        (
            "summarize",
            summarize(
                "LangChain orchestrates prompts while MCP standardizes tooling.",
            ),
        ),
        (
            "word_count",
            word_count(
                "FastMCP keeps rapid prototyping inside a single process",
            ),
        ),
    ]

    formatted = []
    for name, result in outputs:
        formatted.append(f"{name}: {result}")
    return "\n".join(formatted)


async def _read_resource(uri: str) -> str:
    """Read a resource via the FastMCP server and stringify its contents."""

    contents = await MCP_SERVER.read_resource(uri)
    lines: list[str] = []
    for chunk in contents:
        payload: Any = chunk.content
        if isinstance(payload, bytes):
            lines.append(payload.decode("utf-8", "replace"))
        else:
            lines.append(str(payload))
    return "\n".join(lines)


def _sample_mcp_resources() -> str:
    """Synchronously fetch two resources for CLI display."""

    async def runner() -> tuple[str, str]:
        primer = await _read_resource("resource://mcp/primer")
        deep_dive = await _read_resource("resource://mcp/resources/tools")
        return primer, deep_dive

    primer_text, deep_dive_text = asyncio.run(runner())
    return (
        "Primer -> "
        + primer_text
        + "\nDeep dive (tools) -> "
        + deep_dive_text
    )


def _sample_mcp_prompt() -> str:
    """Render the orientation prompt so humans can see the template."""

    messages = orientation_prompt("Demo Workspace")
    lines = [f"{msg['role'].title()}: {msg['content']}" for msg in messages]
    return "\n".join(lines)


def main() -> None:
    print("Hello from the MCP demo!")
    print("\n--- LangChain scripted chat ---")
    print(_render_prompt("LangChain + MCP explorer"))
    print("\n--- MCP resources ---")
    print(_sample_mcp_resources())
    print("\n--- MCP prompts ---")
    print(_sample_mcp_prompt())
    print("\n--- FastMCP tool results ---")
    print(_sample_mcp_tool_output("LangChain + MCP explorer"))
