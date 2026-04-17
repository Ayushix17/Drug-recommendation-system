from __future__ import annotations

from ai.prompts import SYSTEM_PROMPT, recommendation_prompt


class LLMEngine:
    def __init__(self) -> None:
        self.system_prompt = SYSTEM_PROMPT

    def summarize_recommendation(self, payload: dict) -> str:
        _ = recommendation_prompt(payload)
        accepted = payload.get("accepted", [])
        rejected = payload.get("rejected", [])
        return (
            f"Summary: {len(accepted)} accepted options and {len(rejected)} rejected options. "
            "Review interaction and contraindication reasons before clinical use."
        )
