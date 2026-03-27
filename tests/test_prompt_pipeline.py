from app.services.prompt_pipeline import MultiAgentPromptFixer, validate_instruction_following


def test_pipeline_builds_structured_prompt_and_consensus():
    fixer = MultiAgentPromptFixer()
    prompt, consensus, notes = fixer.run("Write a launch email for a new battery product")

    assert consensus is True
    assert "Role:" in prompt
    assert "Constraints:" in prompt
    assert "Fact-checking step:" in prompt
    assert set(notes.keys()) == {"writer", "editor", "proofreader", "fact_checker"}


def test_instruction_validator_flags_missing_markers():
    ok, notes = validate_instruction_following("unused", "Short answer only")
    assert ok is False
    assert "Missing markers" in notes


def test_instruction_validator_passes_structured_output():
    output = "Answer: done\nEvidence: source\nCaveats: uncertain"
    ok, notes = validate_instruction_following("unused", output)
    assert ok is True
    assert "appears to follow" in notes
