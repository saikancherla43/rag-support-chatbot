"""Demo CLI: ask a question, print the extractive answer + cited sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from answer import answer
from embed import Index


def main() -> None:
    parser = argparse.ArgumentParser(description="Acme Cloud support chatbot (RAG demo)")
    parser.add_argument("question", nargs="*", help="question to ask")
    args = parser.parse_args()

    question = " ".join(args.question) or input("Ask a question: ").strip()
    if not question:
        print("No question given.")
        return

    result = answer(question, Index.load(), k=3)
    print(f"\nQ: {result['query']}\n")
    print(f"A: {result['summary']}\n")
    print("Sources:")
    for i, s in enumerate(result["sources"], 1):
        print(f"  [{i}] {s['title']} > {s['section']}  (score={s['score']}, {s['id']})")


if __name__ == "__main__":
    main()
