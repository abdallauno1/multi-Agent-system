from __future__ import annotations

import json
import os
import urllib.request
from abc import ABC, abstractmethod
from typing import Any, Dict


class LLMClient(ABC):
    provider_name: str = "base"

    @abstractmethod
    def complete_json(self, *, system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    provider_name = "mock"

    def complete_json(self, *, system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
        task = user_payload.get("task")
        goal = user_payload.get("goal", "")
        context = user_payload.get("context", {})
        attempt = int(user_payload.get("attempt", 1))

        if task == "plan":
            steps = [
                "Clarify the goal and constraints",
                "Collect relevant context and signals",
                "Execute the safest operational action",
                "Validate the result and decide whether to retry",
            ]
            if context.get("service"):
                steps.insert(2, f"Focus analysis on service: {context['service']}")
            return {
                "steps": steps,
                "reasoning": "Mock LLM generated a safe operational plan from the goal and context.",
            }

        if task == "validate":
            confidence = float(user_payload.get("confidence", 0.0))
            passed = confidence >= 0.70 and bool(user_payload.get("summary")) and bool(user_payload.get("next_action"))
            if attempt == 1 and confidence < 0.70:
                passed = False
            return {
                "passed": passed,
                "reason": "LLM validation accepted the result." if passed else "LLM validation requested a retry due to weak confidence or missing action.",
            }

        return {
            "summary": f"LLM-assisted execution for goal: {goal}",
            "next_action": "Inspect telemetry, logs, and recent changes before applying mitigation",
            "confidence": 0.82 if attempt > 1 else 0.66,
            "details": {"mode": "mock-llm", "attempt": attempt},
        }


class OpenAICompatibleClient(LLMClient):
    provider_name = "openai"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")

    def complete_json(self, *, system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")

        body = {
            "model": self.model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_payload)},
            ],
        }
        request = urllib.request.Request(
            self.base_url,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)


class OllamaClient(LLMClient):
    provider_name = "ollama"

    def __init__(self) -> None:
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1")
        self.url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    def complete_json(self, *, system_prompt: str, user_payload: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"{system_prompt}\n\nReturn only valid JSON.\nInput:\n{json.dumps(user_payload)}"
        body = {"model": self.model, "prompt": prompt, "format": "json", "stream": False}
        request = urllib.request.Request(
            self.url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        return json.loads(data["response"])


def get_llm_client() -> LLMClient:
    provider = os.getenv("LLM_PROVIDER", "mock").lower().strip()
    if provider == "openai":
        return OpenAICompatibleClient()
    if provider == "ollama":
        return OllamaClient()
    return MockLLMClient()
