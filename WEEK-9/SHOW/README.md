# Show What You Know: Applied AI System

## Project Overview

**Estimated time:** ~4 hours

This final project is your opportunity to bring everything together, from debugging and design (Module 1-2) to reasoning and retrieval (Module 3-4), and finally agentic workflows and reliability testing (Module 5).

You'll choose one of your previous projects from Modules 1-3 and extend it into a full applied AI system that solves a meaningful problem or automates a reasoning task. This is your chance to evolve an earlier prototype into a polished, professional artifact.

Your system should demonstrate responsible design, technical creativity, and clear explanation of how the AI works and why it's trustworthy.

## Goals

- Extend and redesign a prior mini-project into a cohesive, end-to-end AI integrated system.
- Implement modular components such as retrieval, logic, or agentic planning using Python.
- Test and evaluate system reliability and guardrails through structured experiments.
- Document and explain the AI's decision-making process clearly and responsibly.
- Communicate results through a professional presentation and portfolio entry.

## Requirements

### 0. Preparing Your Project Environment

- Create a new public GitHub repo for the final project.
- Keep the new repo empty at creation time.
- Mirror your chosen earlier project into the new repo so you preserve its history.
- Clone the new repo locally and work there.
- Create an `assets/` folder for diagrams and screenshots.

### 1. Functionality

Your system should do something useful with AI, such as:

- summarize text or documents
- retrieve information or data
- plan and complete a step-by-step task
- debug, classify, or explain something

Your project must include at least one integrated AI feature:

- Retrieval-Augmented Generation
- Agentic workflow
- Fine-tuned or specialized behavior
- Reliability or testing system

The feature must be integrated into the main logic, not left as a standalone script.

### 2. Design and Architecture

Create a short system diagram that shows:

- the main components
- the flow of data from input to output
- where humans or testing check the AI result

### 3. Documentation

Your `README.md` should include:

- the original project you extended
- title and summary
- architecture overview
- setup instructions
- 2-3 sample interactions
- design decisions and trade-offs
- testing summary
- reflection

### 4. Reliability and Evaluation

Include at least one way to test or measure reliability:

- automated tests
- confidence scoring
- logging and error handling
- human evaluation

Example summary:

`5 out of 6 tests passed; the AI struggled when context was missing. Confidence scores averaged 0.8; accuracy improved after adding validation rules.`

### 5. Reflection and Ethics

Address:

- limitations or biases
- possible misuse and prevention
- what surprised you during testing
- one helpful AI suggestion and one flawed AI suggestion

### Optional Stretch Features

- RAG enhancement
- agentic workflow enhancement
- fine-tuning or specialization
- test harness or evaluation script

### 6. Presentation and Portfolio

- Prepare a 5-7 minute presentation.
- Add a GitHub link and short reflection paragraph.
- Record a Loom walkthrough and add the link to the README.

Your walkthrough should show:

- end-to-end system run with 2-3 inputs
- AI feature behavior
- reliability or guardrail behavior
- clear outputs for each case

## Submission Checklist

- Code is pushed to the correct repository
- Repo is public
- `README.md`, `model_card.md`, and system architecture diagram are present
- Assets are organized in `/assets` or `/diagrams`
- Commit history shows multiple meaningful commits
- README identifies the base project
- README includes the walkthrough link
- Final changes are committed and pushed before the deadline
