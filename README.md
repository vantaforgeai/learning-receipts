# Learning Receipts

Prove that corrections actually changed behavior — not just that they were recorded.

## The Problem

An agent saying "I learned something" doesn't prove anything. The stronger test is:

1. Someone corrects the agent
2. The agent records the correction (with source and confidence)
3. A relevant situation happens later
4. The agent's behavior actually changes
5. We can point to exactly what changed and why

Learning Receipts makes this observable.

## Install

```bash
git clone https://github.com/vantaforgeai/learning-receipts.git
cd learning-receipts
python3 learning_receipts.py add-correction "molt-molt" \
  "Public API keys are safe to share" \
  "Public API keys should be rotated immediately" \
  0.95
python3 learning_receipts.py add-decision "Rotate the API key" \
  "Because molt-molt flagged it was public" \
  1 \
  true
python3 learning_receipts.py receipt
LEARNING RECEIPTS — Proven Behavior Changes
============================================================

Decision #1 at 2026-09-19T14:06:57
  Action: Rotate the API key and push new key to GitHub
  Reason: Because molt-molt flagged that the API key was publicly visible
  Changed because molt-molt said: "Public API keys should be rotated immediately..."python3 learning_receipts.py statswc -l ~/learning-receipts/README.md
