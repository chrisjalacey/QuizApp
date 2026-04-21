# JSON Schema Reference

## Overview

Quiz data is stored in `data/quizzes.json` as a JSON file with categories and questions. This file is loaded by the Flask app and used to populate quizzes.

## Root Structure

```json
{
  "categories": [...]
}
```

## Category Object

```json
{
  "name": "string (required) - Category name displayed in UI",
  "questions": [...]
}
```

**Example:**
```json
{
  "name": "Mathematics",
  "questions": [...]
}
```

## Question Object

```json
{
  "text": "string (required) - The question text",
  "options": ["string", "string", ...] (required) - Array of answer options",
  "correct": [integer, integer, ...] (required) - Array of indices of correct answers",
  "type": "string (required) - 'single' or 'multi'",
  "image": "string (optional) - Relative path to image file in img/ folder"
}
```

### Field Details

- **text**: Question phrasing. Support HTML entities for special characters.
- **options**: Array of possible answers. Each is rendered as a radio button (single) or checkbox (multi).
- **correct**: Array of 0-based indices into options array. For single-choice, usually length 1; for multi-choice, can be any length.
- **type**: "single" for single-choice (radio buttons), "multi" for multi-choice (checkboxes).
- **image**: Optional path relative to img/ folder (e.g., "math_primes.png" or "physics/forces.png"). If null or omitted, no image shown.

## Full Example

```json
{
  "categories": [
    {
      "name": "Mathematics",
      "questions": [
        {
          "text": "What is the square root of 144?",
          "options": ["10", "12", "14", "16"],
          "correct": [1],
          "type": "single",
          "image": null
        },
        {
          "text": "Which of the following are prime numbers?",
          "options": ["2", "4", "6", "7", "9"],
          "correct": [0, 3],
          "type": "multi",
          "image": "math/primes.png"
        }
      ]
    },
    {
      "name": "Science",
      "questions": [
        {
          "text": "Which of these are noble gases?",
          "options": ["Helium", "Oxygen", "Argon", "Nitrogen"],
          "correct": [0, 2],
          "type": "multi",
          "image": "science/periodic_table.png"
        }
      ]
    }
  ]
}
```

## Validation Rules

1. **Structure**: Must be valid JSON
2. **Categories**: At least one category required
3. **Questions per Category**: At least one question per category recommended
4. **Correct Indices**: Must be 0-based valid indices into options array
5. **Type**: Must be exactly "single" or "multi"
6. **Image Path**: Must be relative path or null; file must exist in img/ folder
7. **Text/Options**: Non-empty strings

## Image File Organization

Store images in the `img/` folder. Nested subfolders are supported:

```
img/
├── math_primes.png
├── physics/
│   ├── forces.png
│   └── motion.png
├── science/
│   └── elements.png
```

Reference in JSON:
```json
"image": "math_primes.png"              // Root img/ folder
"image": "physics/forces.png"          // Subfolder
"image": "science/elements.png"        // Nested subfolder
```

## Scoring Rules

### Single-Choice
- User selects one option (radio button)
- Marked correct if selected index matches `correct[0]`

### Multi-Choice
- User selects zero or more options (checkboxes)
- Marked correct if selected indices exactly match `correct` array (order-independent set comparison)
- Example: If `correct: [0, 2]`, user must select options 0 AND 2, no more, no less

## Recommendations

1. **Keep Options Concise**: 2-4 options per question for optimal UX
2. **Randomize Correct Position**: Avoid patterns like always "B is correct"
3. **Use Images Sparingly**: Only when they clarify the question (e.g., diagrams, charts)
4. **Validate Before Use**: Test JSON with a validator or by running the app
5. **Version Control**: Track changes to quizzes.json for question bank versioning

## Example for Adding New Question

1. Identify or create category in categories array
2. Add object to category's questions array:
   ```json
   {
     "text": "Your question here?",
     "options": ["Option A", "Option B", "Option C"],
     "correct": [0],
     "type": "single",
     "image": null
   }
   ```
3. Save and reload app