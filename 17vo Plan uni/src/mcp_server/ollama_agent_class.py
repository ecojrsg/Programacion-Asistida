#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Developer: Miguel Jara Maldonado.
Creation Date: 2025-04-10.
Description: Interface for all system agents to ensure consistent structure.
"""

import logging

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

MCP_SERVER_URL = "http://localhost:4000/mcp"
logger = logging.getLogger(__name__)


class OllamaAgent:

    def __init__(self, model_name: str, base_url: str):
        self.model = OllamaModel(
            model_name=model_name,
            provider=OllamaProvider(base_url=base_url),
        )

        self.mcp_server = MCPToolset(MCP_SERVER_URL)

        self.agent = Agent(
            self.model,
            toolsets=[self.mcp_server],
            system_prompt=(
                "You are chat bot assistant."
                "You can use available tools to help users when required."
                "Start all your responses with '[Answer ahead]:'."
            ),
        )

    def run(self, prompt: str):
        logger.info(f"Running AI for: {prompt}.")

        result = self.agent.run_sync(prompt)
        return result
