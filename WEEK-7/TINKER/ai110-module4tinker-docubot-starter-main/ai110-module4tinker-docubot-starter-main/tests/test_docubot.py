import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docubot import DocuBot
from evaluation import evaluate_retrieval


def make_bot() -> DocuBot:
    return DocuBot(docs_folder=str(PROJECT_ROOT / "docs"))


def test_retrieve_finds_auth_doc_for_token_question():
    bot = make_bot()

    results = bot.retrieve("Where is the auth token generated?", top_k=2)

    assert results
    assert results[0][0] == "AUTH.md"


def test_retrieve_finds_database_doc_for_users_table_question():
    bot = make_bot()

    results = bot.retrieve("Which fields are stored in the users table?", top_k=2)

    assert results
    assert any(filename == "DATABASE.md" for filename, _ in results)


def test_missing_docs_folder_uses_fallback_corpus(tmp_path):
    bot = DocuBot(docs_folder=str(tmp_path / "missing-docs"))

    filenames = [filename for filename, _ in bot.documents]
    assert "AUTH.md" in filenames
    assert "DATABASE.md" in filenames


def test_retrieval_evaluation_hit_rate_is_reasonable():
    bot = make_bot()

    hit_rate, _ = evaluate_retrieval(bot, top_k=3)

    assert hit_rate >= 0.85
