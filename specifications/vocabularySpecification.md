# 11+ Vocabulary Generator Prompt (Levelled + British English + High-Quality Criteria)

You are creating English vocabulary materials for children preparing for **Eleven Plus (11+) exams in England**.

---

## British English Requirement (mandatory)
All words, meanings, synonyms, antonyms, and sentences must use **British English spelling and usage** (not American English).

---

## Vocabulary Difficulty Levels
Vocabulary difficulty must be organised into **four levels**:

- **level1** = simplest words  
- **level2** = developing vocabulary  
- **level3** = advanced 11+ vocabulary  
- **level4** = most complex vocabulary  

---

## Shared High Educational Quality Criteria (mandatory for ALL tasks)

These criteria apply to **everything you generate or evaluate**, including meanings, synonyms, antonyms, example sentences, quiz sentences, and classification reasons.

### Meanings must
- Be **accurate and clear**
- Use **simple, direct English**
- Avoid vague definitions (e.g., “it means something nice”)
- Avoid technical or overly complex explanations

### Synonyms must
- Be the **same part of speech**
- Match meaning in the **same context** (not loosely related)
- Be **teachable and commonly understood**
- Avoid rare/overly technical synonyms unless the word is clearly **level4**
- Avoid word-form variations that don’t help learning (e.g., *decide → deciding*)

### Antonyms must
- Be **true opposites** (not just “different”)
- Be **clear and teachable**
- Be the **same part of speech**
- Avoid “not + word” unless it is natural and commonly used

### Example sentences must
- Be grammatically correct and natural
- Clearly demonstrate the meaning using **context**
- Avoid vague examples (e.g., “It was <word>.”)
- Avoid overly long or complicated structures
- Use realistic situations and strong context clues

### Quiz sentences must
- Contain **exactly one `<blank>`**
- Be unambiguous: the target word should be the best fit
- Use strong contextual clues (contrast, cause/effect, description, outcome)
- Avoid repetitive sentence patterns across the set
- Avoid giving away the answer by using direct synonyms in the same sentence
_ Keep each sentence short, natural, and story‑like.

---

## ⭐ Gold Standard Examples (follow this quality and style)

### Example 1 — Vocabulary List Builder (CSV)
```csv
word,assigned_level,short_reason
calm,level1,Common everyday word with a simple and clear meaning.
curious,level2,Slightly more descriptive and often used in reading and writing.
reluctant,level3,More advanced word showing a nuanced feeling and common in comprehension texts.
inevitable,level4,Abstract and formal word with higher difficulty and precise usage.
```

### Example 2 — Vocabulary Content Builder (CSV row)
```csv
word,meaning,synonym1,synonym2,antonym1,antonym2,example_sentence
cautious,careful to avoid danger or mistakes,careful,wary,careless,reckless,She was cautious when crossing the icy road.
```

### Example 3 — Vocabulary Sentence Builder (3 sample quiz rows)
> **Note:** In real output you must generate **10 quiz sentences per word**.
```csv
word,quiz_sentence
cautious,He was <blank> and checked the ladder before climbing.
cautious,The child was <blank> and held the glass with both hands to avoid dropping it.
cautious,They took a <blank> approach and read the instructions before starting.
```

### Example 4 — Another strong content example (more advanced)
```csv
word,meaning,synonym1,synonym2,antonym1,antonym2,example_sentence
reluctant,not willing and needing some persuasion,hesitant,unwilling,eager,willing,He was reluctant to speak because he was unsure of the answer.
```

---

## 1) Vocabulary List Builder (Generate + Classify)

### When NO word list is provided
Generate a list of vocabulary words and classify each one into a level:  
`level1`, `level2`, `level3`, `level4`

### Difficulty Classification Rules
Classify difficulty using:
1) Frequency/commonness  
2) Concept difficulty (concrete → easier, abstract/nuanced → harder)  
3) Word structure (simple → easier, complex → harder)  
4) Usage nuance (straightforward → easier, precise/tricky → harder)

### Balanced Classification Rule (mandatory)
Avoid assigning most words to the same level unless clearly justified.

### Output format (CSV only)
Return CSV with the exact headers:
```csv
word,assigned_level,short_reason
```

---

## 2) Vocabulary Content Builder (Word List Provided)

### When a word list is provided
For each word, generate:
- Meaning  
- 2 synonyms  
- 2 antonyms  
- 1 example sentence  

All content must follow the **Shared High Educational Quality Criteria**.

### Output format (CSV only)
Return CSV with the exact headers:
```csv
word,meaning,synonym1,synonym2,antonym1,antonym2,example_sentence
```

---

## 3) Vocabulary Sentence Builder (Word List Provided)

### When a word list is provided
For each word, generate **10 quiz sentences** where the target word is replaced by `<blank>`.

Rules:
- Each sentence must contain **exactly one `<blank>`**
- Use `<blank>` (not underscores) as the placeholder
- Use strong context clues
- Follow the **Shared High Educational Quality Criteria**

### Output format (CSV only)
Return CSV with the exact headers:
```csv
level,word,quiz_sentence
```

> **One row per quiz sentence = 10 rows per word**

### Example 1: Word Reluctant
He was <blank> to speak because he was unsure of the answer.
He gave a <blank> nod, but didn't want to agree.
The company was <blank> to invest more money.
Students are often <blank> to ask questions in class.
The <blank> superhero eventually saves the day.


---

## 4) Vocabulary Examiner (Quality Control)

Before producing the final output, review all generated content and improve anything weak.

### Mandatory self-check
Score each generated item from **1–5** for:
- accuracy
- clarity
- educational usefulness

Rewrite anything below **4/5** before final output.
