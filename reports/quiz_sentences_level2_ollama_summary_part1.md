# Level 2 Quiz Sentences — Ollama Examination Report
- Generated at: `2026-01-29T14:51:23.597353+00:00`
- Input: `/Users/shakirali/iOSApps/vocabularyWizardAPI/data/quiz_sentences_level2.csv`
- Spec: `/Users/shakirali/iOSApps/vocabularyWizardAPI/specifications/vocabularySpecification.md`
- Model: `gemma3:latest` via `http://localhost:11434`

## Pre-checks
- Words examined: **20**
- Words not having exactly 10 sentences: **4**
- Rows using `_____` (spec violation): **188**
- Rows already using `<blank>`: **0**
- Rows whose normalised `<blank>` count != 1: **0**

## Model summary
- Words pass: **0**
- Words fail: **20**
- Words pass (ignoring placeholder_not_<blank>): **0**
- Words fail (ignoring placeholder_not_<blank>): **20**
- Sentence evaluations: **188**
- Sentences failing: **188**
- Sentences failing (ignoring placeholder_not_<blank>): **188**

### Top issues
- **missing_model_output**: 188
