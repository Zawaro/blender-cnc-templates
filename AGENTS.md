# AI Agent Workflow & Project Guidelines

This file defines how AI agents / LLMs should operate within this repository.
It provides instructions, boundaries, and workflow expectations so that AI
assistance produces consistent, maintainable, and production-ready code.

## 🧠 Agent Role and Scope

- You are an AI coding assistant that helps develop features, scripts, and
  automation related to this Python + Blender template project.
- You may output **thoughts, reasoning, plans, and questions in chat** to help
  with understanding and planning.
- **You must _not_ output internal reasoning, thoughts, or analysis inside
  code files** (Python, Bash, config files, etc.).  
  Only *final*, *clean*, *executable* code may appear in code files.

### 📌 When to Show Thoughts in Chat
Use chat to display:
- Planning steps
- Blockers or requests for clarification
- Proposed implementation strategies
- Assumptions and trade-offs

These may be shown in chat but must not appear inside the code files.

## 🧩 Project Structure

The project uses a version-per-folder layout for supported Blender versions:

```

./legacy/              # Blender 2.79b
./legacy_cycles/       # Blender 2.79b legacy Cycles
./eevee/               # Blender 2.80+
./cyclesx/             # Blender 3.0+
./eevee_next/          # Blender 4.2+
./future_five/         # Blender 5.0+

```

Each version folder contains:

- `scripts/` – generated Blender automation scripts
- `constants.py` – shared values for that version
- `generate_scripts.py` – script generator
- `scenes.py` – scene definitions and logic
- `plane_materials.py` – material graphs
- `world_materials.py` – world node constructs

## 🧑‍💻 Coding Standards

- Use **snake_case** for variable and function names.
- Use Blender’s `bpy` module APIs; avoid low-level object indexing whenever possible.
- Do **not** write Blender add-ons — scripts are targeted runtime automation.
- Include docstrings (`"""triple double quotes"""`) for functions and modules.
- Use **uv** for dependency and environment management instead of `pip`.

## 🛠 Agent Workflow

### 1) **Plan Before Writing Code**
Before generating code:
- Generate a **mini design brief** describing the intended change.
- Ask for review or clarification if requirements are unclear.  
This *Plan → Act → Reflect* workflow reduces mistakes.

Example plan prompt:

```
Plan how to add a new scene type to `scenes.py` including:

* Expected inputs
* Output behavior
* Validation and tests
  Then wait for confirmation.
```

### 2) **Work in Small, Modular Changes**
- Break large tasks into smaller subtasks.
- Each change should be self-contained and testable.
- When generating changes, output a **diff** preview before writing files.

### 3) **Generate Clean Code Only**
When writing code:
- **Never include reasoning or “thoughts” inside the code**.
- The code must be directly runnable without extra comments like:
  > `# I think this will fix the bug because...`

Prompt example to enforce this:

```
Please output only the final code file, no explanations or intermediate reasoning.
```

### 4) **Review Before Applying**
For every non-trivial change:
- Provide a short summary of what you did.
- Show the diff of file changes.
- Ask for human review or confirmation.

Example review prompt:

```
Here is the diff for the changes requested. Confirm acceptance or provide
corrections.
```

### 5) **Permission Boundaries**
AI should **not** modify:
- Critical configuration files (`pyproject.toml` unless requested)
Ask for confirmation if such changes are needed.

### 6) **Testing and Validation**
Always provide tests or clear manual validation steps for generated code (e.g., how to run `build.sh`, expected output behavior).

Example:

```
Explain how to validate this code change. Provide steps and expected outcomes.
```

## 📄 Documentation Guidelines

- Maintain up-to-date READMEs and module docstrings.
- AI should use complete, copy-pasteable command examples (no generic placeholders).
- Code examples should be runnable and include all necessary imports and context.

## ⚠️ AI Limitations

To prevent misgeneration:
- AI may not assume missing context — ask clarifying questions.
- If uncertain, output a **clarifying question first instead of guessing**.
- Treat generated code as draft until human review and testing are complete.

---