let improvedPrompt = "";
let latestOutput = "";

const rawPrompt = document.getElementById("rawPrompt");
const improveBtn = document.getElementById("improveBtn");
const improvedPreview = document.getElementById("improvedPreview");
const consensus = document.getElementById("consensus");
const modelName = document.getElementById("modelName");
const testBtn = document.getElementById("testBtn");
const modelOutput = document.getElementById("modelOutput");
const validation = document.getElementById("validation");
const saveFeedbackBtn = document.getElementById("saveFeedbackBtn");
const rating = document.getElementById("rating");
const rank = document.getElementById("rank");
const saveStatus = document.getElementById("saveStatus");

improveBtn.addEventListener("click", async () => {
  const response = await fetch("/api/improve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: rawPrompt.value })
  });
  const data = await response.json();
  improvedPrompt = data.improved_prompt;
  improvedPreview.textContent = improvedPrompt;
  consensus.textContent = data.consensus_reached ? "Consensus reached" : "Consensus failed";
});

testBtn.addEventListener("click", async () => {
  const response = await fetch("/api/test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ improved_prompt: improvedPrompt, model: modelName.value })
  });
  const data = await response.json();
  latestOutput = data.output;
  modelOutput.textContent = latestOutput;
  validation.textContent = `${data.instruction_followed ? "Pass" : "Fail"}: ${data.validation_notes}`;
});

saveFeedbackBtn.addEventListener("click", async () => {
  const response = await fetch("/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      original_prompt: rawPrompt.value,
      improved_prompt: improvedPrompt,
      model_name: modelName.value,
      model_output: latestOutput,
      rating: Number(rating.value),
      rank: Number(rank.value)
    })
  });

  const data = await response.json();
  saveStatus.textContent = response.ok ? `Saved feedback #${data.id}` : "Failed to save feedback";
});
