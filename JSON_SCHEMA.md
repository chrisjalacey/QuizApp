# JSON Schema Reference

## Overview

Quiz data is organized into separate JSON files by topic. A registry file (`quizzes_registry.json`) indexes all available quizzes. This modular approach enables easy addition of new quizzes without modifying existing files.

## Quizzes Registry (data/quizzes_registry.json)

Central index of all available quizzes.

```json
{
  "quizzes": [
    {
      "id": "string (required) - Unique quiz identifier",
      "name": "string (required) - Display name for UI",
      "file": "string (required) - Relative path to quiz JSON file"
    }
  ]
}
```

**Example:**
```json
{
  "quizzes": [
    {
      "id": "math",
      "name": "Mathematics",
      "file": "data/math.json"
    },
    {
      "id": "science",
      "name": "Science",
      "file": "data/science.json"
    },
    {
      "id": "gce",
      "name": "Google Associate Cloud Engineer",
      "file": "data/gce.json"
    }
  ]
}
```

## Individual Quiz File Structure (data/{quiz_id}.json)

Each quiz file contains only the questions (no wrapper).

```json
{
  "questions": [...]
}
```

**Example: data/math.json**
```json
{
  "questions": [
    {
      "text": "What is 2 + 2?",
      "options": ["3", "4", "5"],
      "correct": [1],
      "type": "single",
      "image": null
    },
    {
      "text": "Which are prime numbers?",
      "options": ["2", "3", "4", "5"],
      "correct": [0, 1, 3],
      "type": "multi",
      "image": null
    }
  ]
}
```

## Question Object Format

```json
{
  "text": "string (required) - The question text",
  "options": ["string", "string", ...] (required) - Array of answer options",
  "correct": [integer, integer, ...] (required) - Array of indices of correct answers",
  "type": "string (required) - 'single' or 'multi'",
  "image": "string (optional) - Relative path to image in img/ folder"
}
```

### Field Details

- **text**: Question phrasing. Support HTML entities for special characters.
- **options**: Array of possible answers. Each is rendered as a radio button (single) or checkbox (multi).
- **correct**: Array of 0-based indices into options array.
  - For single-choice: length 1 (e.g., `[1]`)
  - For multi-choice: any length (e.g., `[0, 1, 3]` for 3 correct answers)
- **type**: "single" for single-choice (radio buttons), "multi" for multi-choice (checkboxes).
- **image**: Optional path relative to img/ folder (e.g., "math_primes.png" or "physics/forces.png"). If null or omitted, no image shown.

## Full Example (data/gce.json)

```json
{
  "questions": [
    {
      "text": "Which compute service provides serverless container execution?",
      "options": ["Compute Engine", "Cloud Run", "App Engine", "GKE"],
      "correct": [1],
      "type": "single",
      "image": null
    },
    {
      "text": "Which of these are valid GCP metadata? (Select all that apply)",
      "options": ["Machine type", "Zone", "Project ID", "Service account email"],
      "correct": [0, 1, 2, 3],
      "type": "multi",
      "image": null
    },
    {
      "text": "What is the difference between Standard and Nearline storage?",
      "options": ["Nearline has higher latency and lower cost", "Standard is slower", "They are identical"],
      "correct": [0],
      "type": "single",
      "image": "gcp/storage_tiers.png"
    }
  ]
}
```

## Validation Rules

1. **Structure**: Must be valid JSON
2. **Registry**: Must contain at least one quiz
3. **Quiz File**: Must have `questions` array (can be empty, but not recommended)
4. **Correct Indices**: Must be 0-based valid indices into options array
5. **Type**: Must be exactly "single" or "multi"
6. **Image Path**: Must be relative path or null; file must exist in img/ folder if specified
7. **Text/Options**: Non-empty strings recommended

## Image File Organization

Store images in the `img/` folder. Nested subfolders are supported:

```
img/
├── math_primes.png
├── physics/
│   ├── forces.png
│   └── motion.png
├── gcp/
│   └── architecture.png
```

Reference in JSON:
```json
"image": "math_primes.png"              // Root img/ folder
"image": "physics/forces.png"          // Subfolder
"image": "gcp/architecture.png"        // Nested subfolder
```

## Scoring Rules

### Single-Choice
- User selects one option (radio button)
- Marked correct if selected index matches `correct[0]`
- Example: `correct: [1]` → only option index 1 is correct

### Multi-Choice
- User selects zero or more options (checkboxes)
- Marked correct if selected indices **exactly match** `correct` array (order-independent set comparison)
- User must select all correct answers AND no incorrect answers
- Example: If `correct: [0, 2]`, user must select **both** option 0 AND option 2, no more, no less
- Selecting only 0, or 0 & 1, or 0 & 2 & 3 would all be marked incorrect

## How to Add a New Quiz

### Step 1: Create Quiz JSON File
Create `data/{quiz_id}.json` with questions:
```json
{
  "questions": [
    {"text": "...", "options": [...], "correct": [...], "type": "single", "image": null},
    ...
  ]
}
```

### Step 2: Add to Registry
Edit `data/quizzes_registry.json` and append:
```json
{
  "id": "{quiz_id}",
  "name": "Display Name",
  "file": "data/{quiz_id}.json"
}
```

### Step 3: Test
- Restart Flask app
- Verify quiz appears in home page dropdown
- Take quiz to verify questions load correctly

**Example: Adding a Python quiz**
1. Create `data/python.json` with Python questions
2. Add to registry: `{"id": "python", "name": "Python Programming", "file": "data/python.json"}`
3. Restart app → Python quiz now available in dropdown

## Recommendations

1. **Keep Options Concise**: 2-4 options per question for optimal UX
2. **Randomize Correct Position**: Avoid patterns like always "B is correct"
3. **Use Images Sparingly**: Only when they clarify the question (e.g., diagrams, charts)
4. **Validate JSON**: Use online JSON validator or Python: `python -c "import json; json.load(open('data/math.json'))"`
5. **Version Control**: Commit quiz changes to git for history tracking
6. **Naming**: Use lowercase, hyphen-separated IDs (e.g., `aws-ec2`, `kubernetes-basics`)

## Multi-Choice Display Hint

In quiz.html, questions with `type: "multi"` display:
```
(Select X correct answers)
```

This count is calculated from `len(question.correct)` automatically.
     "type": "single",
     "image": null
   }
   ```
3. Save and reload app