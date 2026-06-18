# JSON Schema Reference

## Overview

Quiz data is stored as individual JSON files in `data/quizzes/`. Files are auto-discovered — no registry needed. Simply add a `.json` file to the folder and restart the app.

## Quiz File Structure (data/quizzes/{quiz_id}.json)

```json
{
  "name": "string (required) - Display name shown in UI",
  "id": "string (optional) - Quiz identifier",
  "sections": [
    {
      "id": "string - Section identifier used in questions",
      "name": "string - Section display name",
      "description": "string - Brief section description"
    }
  ],
  "questions": [...]
}
```

## Question Object Format

```json
{
  "text": "string (required) - The question text",
  "options": ["string", ...],
  "correct": [integer, ...],
  "type": "single" or "multi",
  "image": "string or null (optional) - Relative path in img/ folder",
  "explanation": "string (optional) - Explanation shown in review",
  "section": "string (optional) - Section ID this question belongs to"
}
```

### Field Details

- **text**: Question phrasing
- **options**: Array of possible answers (rendered as radio buttons or checkboxes)
- **correct**: Array of 0-based indices into options array
  - Single-choice: length 1 (e.g., `[1]`)
  - Multi-choice: any length (e.g., `[0, 1, 3]`)
- **type**: `"single"` for radio buttons, `"multi"` for checkboxes
- **image**: Path relative to `img/` folder, or `null`
- **explanation**: Shown after quiz submission in the review
- **section**: Links question to a section defined in the top-level `sections` array

## Full Example

```json
{
  "name": "Google Associate Cloud Engineer",
  "id": "gce",
  "sections": [
    {"id": "setup", "name": "Setting up a cloud solution environment", "description": "Project creation, IAM, billing"},
    {"id": "deploy", "name": "Deploying a cloud solution", "description": "Deployment, configuration"}
  ],
  "questions": [
    {
      "text": "Which compute service provides serverless container execution?",
      "options": ["Compute Engine", "Cloud Run", "App Engine", "GKE"],
      "correct": [1],
      "type": "single",
      "image": null,
      "explanation": "Cloud Run is a fully managed serverless container platform.",
      "section": "deploy"
    },
    {
      "text": "Which are valid GCP instance metadata?",
      "options": ["Machine type", "Zone", "Project ID", "Service account email"],
      "correct": [0, 1, 2, 3],
      "type": "multi",
      "image": null,
      "explanation": "All of these are queryable via the metadata server.",
      "section": "setup"
    }
  ]
}
```

## Scoring Rules

### Single-Choice
- Correct if selected index matches `correct[0]`

### Multi-Choice
- Correct only if selected indices **exactly match** `correct` array (set comparison, order-independent)
- Must select all correct AND no incorrect answers

## How to Add a New Quiz

1. Create `data/quizzes/{quiz_id}.json` with the format above
2. Restart the app
3. Quiz appears automatically in the home page dropdown

## Image Organization

```
img/
├── math_primes.png
├── gcp/
│   └── architecture.png
```

Reference in JSON: `"image": "gcp/architecture.png"`

## Validation Rules

1. Must be valid JSON
2. Must have `name` and `questions` fields
3. `correct` indices must be valid indices into `options`
4. `type` must be `"single"` or `"multi"`
5. `section` (if used) should match a section `id` in the `sections` array
6. Image file must exist in `img/` if specified
