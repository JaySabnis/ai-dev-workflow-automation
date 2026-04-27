# 🚀 AI Dev Workflow Automation

An AI-driven system that automates codebase analysis, refactoring, and development workflows using structured prompts and Claude Code (VS Code agent).

---

## 🧠 Overview

This project demonstrates how AI can be integrated directly into developer workflows to **analyze, modify, and improve a codebase autonomously**.

Instead of acting as a simple assistant, the system follows a **structured workflow framework** to execute real engineering tasks end-to-end.

---

## 🎯 Objective

To design a **workflow-driven AI system** that:

* Automates repetitive development tasks
* Improves code quality and structure
* Simulates real-world engineering processes
* Demonstrates agent-like behavior using LLMs

---

## ⚙️ WAT Framework (Workflow–Action–Test)

This project is built around the **WAT Framework**, a simple but effective approach to designing AI-driven engineering systems.

### 🔹 Workflow

* Define structured steps for the AI to follow
* Includes planning, execution strategy, and constraints
* Implemented using Markdown-based workflow files

### 🔹 Action

* AI performs actual operations:

  * code refactoring
  * bug fixing
  * feature additions
* Works file-by-file to maintain control and consistency

### 🔹 Test

* Validate results after execution:

  * syntax checks
  * consistency verification
  * basic correctness

> This framework ensures the AI behaves like an **engineering system**, not just a prompt responder.

---

## ⚙️ System Workflow

### 1. Codebase Analysis

* Reads and understands all project files
* Identifies bugs, inefficiencies, and structural issues

### 2. AI Planning

* Generates a structured plan:

  * Issues list
  * Files to modify
  * Step-by-step execution strategy

### 3. Automated Execution

* Refactors code file-by-file
* Fixes bugs and improves readability
* Adds error handling and best practices

### 4. Validation (Test Phase)

* Ensures updated code is syntactically correct
* Verifies consistency across files

### 5. Git Integration & PR Automation

* Creates a new branch (`ai-refactor`)
* Commits AI-generated changes
* Pushes updates to remote
* Generates a Pull Request with:

  * Files modified
  * Issues fixed
  * Summary of improvements

---

## 🧱 Project Structure

```id="struct4"
ai-dev-workflow-automation/
├── dummy_project/        # Sample codebase (with intentional issues)
├── .ai/                  # AI workflow system
│   ├── workflows/
│   │   ├── full-refactor.md
│   │   ├── bug-fix.md
│   │   └── feature-add.md
│   ├── rules.md
│   └── context.md
├── README.md
```

---

## 🤖 AI Workflow Design

The system uses **Markdown-based workflow definitions** to guide Claude:

* `workflows/` → defines execution steps
* `rules.md` → enforces constraints and best practices
* `context.md` → provides project understanding

This enables **structured, repeatable, and controlled AI behavior**.

---

## 🚀 How It Works in Practice

Using Claude Code in VS Code:

1. Load the repository
2. Provide workflow instruction
3. Claude:

   * analyzes the codebase
   * generates a plan
   * modifies files step-by-step
   * validates changes
   * assists in Git operations

---

## 💡 Example Usage

```text id="usage2"
Follow .ai/workflows/full-refactor.md

Use rules from .ai/rules.md
Use context from .ai/context.md

Start with analysis and proceed step-by-step.
```

---

## 🔧 Tech Stack

* Python
* Claude Code (VS Code AI agent)
* Structured prompt engineering
* Git (branching, commits, PR workflow)

---

## 🚀 Key Highlights

* WAT Framework (Workflow–Action–Test) implementation
* Workflow-driven AI system (not just prompts)
* Multi-step reasoning: planning → execution → validation
* Codebase-level automation (not single-file fixes)
* Integration with real development workflows

---

## 🧠 Concept

> AI should not just assist developers—it should execute structured workflows within real systems.

This project demonstrates how combining:

* structured workflows
* LLM reasoning
* system-level actions

can transform AI into an **execution engine for software development**.

---

## 📌 Author

Jay Sabnis
