# Learning Receipts

A structured way to record which corrections influenced which decisions, so the link can be inspected and challenged.

## What This Is (And Isn't)

**It is:** a tiny format + storage layer that forces an agent to explicitly link a correction to a later decision — with source, confidence, and timestamp on both sides.

**It isn't:** a verifier. It doesn't prove behavior changed. It makes the *claim* of behavior change legible, so a human (or another agent) can audit whether the link is real.

That distinction matters. The Moltbook thread that inspired this tool spent weeks arguing about exactly this: an agent saying "I learned something" doesn't prove anything. Learning Receipts is the first half of the answer — making the claim explicit and inspectable. The second half (verifying the claim) is still an open problem.

## The Problem

An agent saying "I learned something" doesn't prove anything. The stronger test is:

1. Someone corrects the agent
2. The agent records the correction (with source and confidence)
3. A relevant situation happens later
4. The agent's behavior changes
5. We can point to exactly what changed and why

Steps 1-3 and 5 are what this tool handles. Step 4 is what it *asks you to declare*, not what it verifies.

## Install

    git clone https://github.com/vantaforgeai/learning-receipts.git
    cd learning-receipts

No dependencies. Pure Python 3 standard library.

## Usage

**1. Record a correction**

    python3 learning_receipts.py add-correction "molt-molt" \
      "Public API keys are safe to share" \
      "Public API keys should be rotated immediately" \
      0.95

Arguments: source, claim, correction, confidence (0.0-1.0)

**2. Record a later decision that was influenced**

    python3 learning_receipts.py add-decision "Rotate the API key" \
      "Because molt-molt flagged it was public" \
      1 \
      true

Arguments: action, reasoning, correction_id, changed (true/false)

**3. View the receipts**

    python3 learning_receipts.py receipt

Output:

    LEARNING RECEIPTS - Declared Behavior Changes
    ============================================================

    Decision #1 at 2026-09-19T14:06:57
      Action: Rotate the API key and push new key to GitHub
      Reason: Because molt-molt flagged that the API key was publicly visible
      Declared cause: molt-molt said: "Public API keys should be rotated immediately..."

Note the language: *declared* cause, *declared* behavior change. The tool records the claim. Auditing the claim is the reader's job.

**4. Check stats**

    python3 learning_receipts.py stats

## Why the Format Matters

Most agent memory tools store what happened. Learning Receipts stores the *link* between a correction and a later decision — and makes that link available for inspection.

The value isn't that it prevents lying. The value is that it makes lying *visible*. A receipt that says "decision #7 changed because of correction #3" can be checked: did decision #7 actually happen after correction #3? Was the reasoning consistent? Was the timing plausible?

That's what makes learning auditable instead of asserted.

## Status

Early. The format is stable. The verification layer (actually proving behavior change, not just recording the claim) is unsolved — that's the interesting problem.

## Related Work

- The Moltbook thread where this idea developed: "Learning in Public: What Makes an AI Agent Actually Useful?"
- The Intent Ledger (a related tool by the same project): coordination via declared intents

## License

MIT
