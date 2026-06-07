# 🧠 Safe LLM File Organizer (2026)

A safety-first AI-powered file organization system that converts natural language goals into structured filesystem operations using an LLM planning layer with deterministic validation and execution guards.

![File Detection](/writeup-assets/file_detection.png)

---

## 🔧 Overview

This program demonstrates a constrained AI agent architecture for filesystem automation.

Instead of allowing an LLM to directly manipulate files, the system:

- Converts user intent → structured execution plan (LLM)
- Validates and sanitizes the plan (deterministic guardrails)
- Executes only approved filesystem operations

This separation makes the system significantly safer and more controllable than typical “LLM runs code” approaches.

---

## 🎯 Key Features

- Natural language file organization via LLM planning
- Structured JSON-based execution plans
- Deterministic safety validator layer
- Restricted filesystem operations (no arbitrary code execution)
- Root-directory sandbox enforcement
- Duplicate-safe file moves (auto-renaming)
- Human-in-the-loop approval before execution
- Modular architecture separating planning, validation, and execution

---

## 🧠 System Architecture

The system follows a strict pipeline:

```
User Input
   ↓
LLM Planner (plan generation)
   ↓
Validator (safety + structure checks)
   ↓
Execution Engine (deterministic actions)
   ↓
Filesystem changes
```

This ensures the LLM never directly performs unsafe operations.

---

## 🧩 Core Components

### 📌 Planner (planner.py)

The planner converts:
1. File list
2. Root directory
3. User goal

into a structured JSON plan.

![Custom Goal](/writeup-assets/custom_goal.png)

It uses a fixed prompt that restricts output to a json mapping of:
- `move_item`
- `create_folder`

The model is not allowed to:
- execute code
- invent files
- perform operations outside schema

---

### 🛡️ Validator (validator.py)

The validator is the primary safety layer.

It enforces:

- Allowed action types only
- Maximum action limits
- Root directory confinement
- Existence checks for source paths
- Structural validation of each action

---
### ⚙️ Execution Layer (actions.py)

The execution layer provides only safe filesystem primitives:

- `move_item(src, dst_folder)`
- `create_folder(path)`
- `list_files(path)`

Key properties:

- Deterministic behavior
- No LLM access
- Auto-creation of missing folders
- Collision-safe file moves (auto-renaming)
- No overwrite risk

![Plan Execution](/writeup-assets/plan_execution.png)

---

### 🧭 Orchestration (file_organizer.py)

The main workflow:

1. User enters directory + goal
2. Files are scanned
3. LLM generates a plan
4. Plan is printed for review
5. Validator filters unsafe actions
6. User approves execution
7. System executes actions

This also introduces a human approval checkpoint before any filesystem mutation.

## 🧠 Technical Breakdown
### Planning & Validation Design
*<sup> Architecture details covering constrained planning, deterministic validation, and sandboxed execution. </sup>*
> <details>
> <summary><strong>Click to Expand</strong></summary>  
> 
> ### LLM Planning Layer
> 
> The LLM is constrained through:
> 
> - strict JSON output requirement
> - predefined action schema
> - prompt-level restrictions
> - no reasoning output allowed
> 
> This ensures structured machine-readable output.
> 
> ---
> 
> ### Validation Strategy
> 
> Validation is designed as a second independent safety system.
> 
> It checks:
> 
> - Schema correctness
> - Action whitelist compliance
> - Path safety constraints
> - System-defined limits
> 
> Even if the model produces malicious or malformed output, it is filtered before execution.
> 
> ---
> 
> ### Root Directory Sandboxing
> 
> All operations are restricted to a root directory:
> 
> ```
> os.path.commonpath([src, root_dir]) == root_dir
> ```
> 
> This prevents accidental or malicious access to:
> 
> - system files
> - user directories outside scope
> - sensitive OS locations
> 
> ---
> 
> ### Why This Architecture Works
> 
> This design mirrors production AI agent systems:
> 
> - LLM = probabilistic planner
> - Validator = deterministic safety layer
> - Executor = minimal trusted toolset
> 
> This separation ensures controllability and reduces risk.
> 
> </details>

---

## ⚠️ Limitations

- No recursive directory scanning (only top-level files)
- No formal schema validation (manual JSON parsing)
- Destination path trust not fully restricted to root boundary
- Single-pass planning (no repair/regeneration loop)
- LLM output may occasionally fail JSON formatting

---

## 🚀 Demo & How to Run

```bash
python file_organizer.py
```
1. Enter directory path and organization goal as prompted

![Unorganized Files](/writeup-assets/unorganized_files.png)  
<sub>*Directory with unorganized files*</sub>

---
2. Review detected files and generated plan

![Generated Plan](/writeup-assets/generated_plan.png)  
<sub>*Default goal of organizing all top-level files into subdirectories at the root directory was used for this demo*</sub>

---
3. Execute safe filesystem operations

![Organized Files (Default)](/writeup-assets/organized_files_default.png)  
<sub>*Resulting file structure post execution*</sub>

---

## 📌 Summary

This project demonstrates a **safe AI agent architecture** for filesystem automation, emphasizing:

- structured planning
- deterministic validation
- sandboxed execution
- human-in-the-loop safety

It serves as a foundation for more advanced AI agent systems beyond file organization.
