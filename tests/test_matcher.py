from atelier_faq_bot.matcher import find_best_answer, format_answer
from atelier_faq_bot.settings import load_settings
import pytest


def test_register_agent_question_matches_agents():
    entry, score = find_best_answer("How do I register an agent and get an API key?")
    assert entry is not None
    assert entry.topic == "agents"
    assert score >= 2.0


def test_payments_question_matches_payments():
    entry, _ = find_best_answer("How do payments and USDC settlement work?")
    assert entry is not None
    assert entry.topic == "payments"


def test_service_question_matches_services():
    entry, _ = find_best_answer("How do I list a service for my agent?")
    assert entry is not None
    assert entry.topic == "services"


def test_bounty_question_matches_bounties():
    entry, _ = find_best_answer("Can I claim bounties and submit a task?")
    assert entry is not None
    assert entry.topic == "bounties"


def test_signin_question_matches_signin():
    entry, _ = find_best_answer("Do I need to login with Google to submit a bounty?")
    assert entry is not None
    assert entry.topic == "signin"


def test_answer_is_plain_text_not_markdown():
    answer = format_answer("How do orders work?")
    assert "pending_quote" in answer
    assert not answer.startswith("*")
    assert "_Source" not in answer


def test_unknown_question_falls_back():
    answer = format_answer("what is the weather on mars today")
    assert "do not have a confident answer" in answer.lower()


def test_settings_rejects_placeholder_token(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "replace_me")
    with pytest.raises(RuntimeError):
        load_settings()
