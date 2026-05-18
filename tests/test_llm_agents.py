from app.agents.executor import ExecutorAgent
from app.agents.planner import PlannerAgent
from app.agents.validator import ValidatorAgent
from app.llm.client import MockLLMClient


def test_planner_uses_llm_provider_metadata():
    planner = PlannerAgent(llm=MockLLMClient())

    result = planner.run({"goal": "Investigate latency", "context": {"service": "checkout-api"}})

    assert result["llm_provider"] == "mock"
    assert result["steps"]
    assert any("checkout-api" in step for step in result["steps"])


def test_executor_returns_llm_enriched_details():
    executor = ExecutorAgent(llm=MockLLMClient())

    result = executor.run({"goal": "Fix incident", "context": {"service": "orders-api"}, "attempt": 2})

    assert result["details"]["llm_provider"] == "mock"
    assert result["confidence"] >= 0.70


def test_validator_can_request_retry_then_pass():
    validator = ValidatorAgent(llm=MockLLMClient())

    first = validator.run({"summary": "ok", "next_action": "check logs", "confidence": 0.66, "attempt": 1})
    second = validator.run({"summary": "ok", "next_action": "check logs", "confidence": 0.82, "attempt": 2})

    assert first["passed"] is False
    assert second["passed"] is True
