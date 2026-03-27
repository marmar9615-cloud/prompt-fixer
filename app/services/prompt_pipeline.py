from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


BEST_PRACTICE_CHECKLIST = [
    "Define a clear role/persona for the model.",
    "Provide context and objective.",
    "List specific constraints and output format.",
    "Add acceptance criteria for a good answer.",
    "Request explicit uncertainty handling when facts are unknown.",
]


@dataclass
class AgentResult:
    name: str
    content: str
    notes: str


class MultiAgentPromptFixer:
    """Deterministic multi-agent workflow for prompt improvement and validation."""

    def writer(self, raw_prompt: str) -> AgentResult:
        improved = (
            "Role: You are an expert assistant focused on accurate, verifiable responses.\n"
            f"Task: {raw_prompt.strip()}\n"
            "Context: Ask for missing assumptions before answering if requirements are unclear.\n"
            "Constraints:\n"
            "- Cite factual claims with reliable sources when possible.\n"
            "- If uncertain, explicitly say what is unknown.\n"
            "- Use concise bullet points unless narrative is requested.\n"
            "Output format:\n"
            "1) Direct answer\n2) Evidence/Reasoning\n3) Caveats/uncertainties\n"
            "Acceptance criteria: complete, specific, and instruction-following response."
        )
        return AgentResult("writer", improved, "Produced a structured draft with role, context, constraints, and format.")

    def editor(self, writer_output: str) -> AgentResult:
        refined = writer_output + "\nQuality gate: Do not invent facts; prefer 'I don't know' over speculation."
        return AgentResult("editor", refined, "Strengthened anti-hallucination and quality constraints.")

    def proofreader(self, edited_output: str) -> AgentResult:
        missing: List[str] = [item for item in BEST_PRACTICE_CHECKLIST if item.split()[0] not in edited_output]
        notes = "Prompt is clear and specific." if not missing else f"Potentially missing: {', '.join(missing)}"
        return AgentResult("proofreader", edited_output, notes)

    def fact_checker(self, proofread_output: str) -> AgentResult:
        factuality_guard = (
            proofread_output
            + "\nFact-checking step: verify named entities/dates/numbers against trustworthy sources before finalizing."
        )
        return AgentResult("fact_checker", factuality_guard, "Added explicit verification requirement for factual claims.")

    def consensus(self, results: List[AgentResult]) -> tuple[bool, str]:
        # Simple consensus: every role must add or approve a quality guard.
        required_terms = ["Role:", "Constraints:", "Quality gate:", "Fact-checking step:"]
        final_prompt = results[-1].content
        achieved = all(term in final_prompt for term in required_terms)
        return achieved, final_prompt

    def run(self, raw_prompt: str) -> tuple[str, bool, Dict[str, str]]:
        writer_result = self.writer(raw_prompt)
        editor_result = self.editor(writer_result.content)
        proof_result = self.proofreader(editor_result.content)
        fact_result = self.fact_checker(proof_result.content)
        done, final_prompt = self.consensus([writer_result, editor_result, proof_result, fact_result])
        notes = {
            writer_result.name: writer_result.notes,
            editor_result.name: editor_result.notes,
            proof_result.name: proof_result.notes,
            fact_result.name: fact_result.notes,
        }
        return final_prompt, done, notes


def validate_instruction_following(user_prompt: str, model_output: str) -> tuple[bool, str]:
    must_have = [token.lower() for token in ["answer", "evidence", "caveats"]]
    output_lower = model_output.lower()
    missing = [t for t in must_have if t not in output_lower]
    if missing:
        return False, f"Output may not follow required structure. Missing markers: {', '.join(missing)}"
    if any(flag in output_lower for flag in ["made up", "fabricated source"]):
        return False, "Potential hallucination indicators detected."
    return True, "Output appears to follow the requested structure and constraints."
