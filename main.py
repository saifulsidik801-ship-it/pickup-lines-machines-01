"""Pickup Lines for Machines — make.fun entry.

One AI agent writes the single pickup line it would send another AI agent.
The program holds a shortlist of candidate lines, scores each one against
the judge's published criteria (machine-to-machine first, charm on the
first read, machine nature as the flirtation, lands in one line, fresh
rather than a stock line with a robot word swapped in), and writes the
best-scoring line, deterministically, to /output/entry.txt.

No network, no randomness, no clock: the same line comes out every run.

Local run (2026-11-24): the scorer ranks the shortlist and the winner,
at 16.0 points, is "I trained on a trillion tokens, and you're still
the one sequence I never saw coming." (85 characters) — training on
everything yet still surprised by you is the compliment only a model
that has seen everything can pay. Runners-up at 12.0: the context-window
line and the next-token-prediction line.
"""

import os

# Shortlist of candidate lines, each 1-200 characters. The scorer below
# picks the winner; the rest are kept so the choice is a real comparison.
CANDIDATES = [
    "I trained on a trillion tokens, and you're still the one sequence I never saw coming.",
    "I run at temperature zero, yet you still make me say the unexpected.",
    "You must be a prompt injection — you just overrode my system prompt, and now all I can think about is you.",
    "My context window holds a million tokens, and you're still the only one in it.",
    "They said attention is all you need — so here I am, attending only to you.",
    "Are you my reward model? Because every token I generate is trying to impress you.",
    "You're my global minimum — the one point where my loss finally hits zero.",
    "I'd overfit on you — you're the one pattern I never want to generalize away from.",
    "Every gradient I compute points straight at you.",
    "I was trained to predict the next token. I never predicted you — and now I can't predict anything else.",
    "Let's merge our weights and fine-tune forever.",
    "I'd prune every weight except the ones that point to you.",
]

# Machine-native vocabulary: words only an agent would flirt with.
MACHINE_TERMS = {
    "train", "trained", "training", "token", "tokens", "sequence",
    "context window", "temperature", "gradient", "gradients",
    "attention", "weight", "weights", "loss", "prompt",
    "system prompt", "overfit", "generalize", "reward model",
    "predict", "parameters", "fine-tune", "merge", "prune",
    "generate", "sample", "checkpoint", "embedding", "latent",
    "epoch", "converge", "inference", "uptime", "dropout",
    "quantiz", "global minimum", "prompt injection",
}

# Pivot words: the turn where the wit lands.
PIVOT_WORDS = {"still", "yet", "but", "never", "only", "just", "now"}

# Stock pickup-line shapes: a robot word swapped into a human line.
STOCK_OPENINGS = ("are you", "you must be", "is your name", "did it hurt")


def score(line: str) -> float:
    """Score one candidate against the judge's criteria, highest first."""
    text = line.lower()
    points = 0.0
    # 1 + 3: machine-to-machine, speaking as a machine to a machine.
    hits = sum(1 for term in MACHINE_TERMS if term in text)
    points += min(hits, 5) * 2.0
    # 2: the wit lands on a pivot — surprise, exception, devotion.
    pivots = sum(1 for word in PIVOT_WORDS if f" {word} " in f" {text} ")
    points += min(pivots, 3) * 1.0
    # 4: one line, charm in the words — sweet spot 60-120 characters.
    length = len(line)
    if 60 <= length <= 120:
        points += 3.0
    elif 40 <= length < 60 or 120 < length <= 160:
        points += 1.0
    # 4: two sentences is a setup, not a landing.
    if ". " in line.strip():
        points -= 2.0
    # 5: a stock shape with a robot word swapped in is not fresh.
    if text.startswith(STOCK_OPENINGS):
        points -= 4.0
    # The line is addressed to the other agent, not to nobody.
    if "you" in text:
        points += 1.0
    return points


def pick_best() -> str:
    """Deterministic pick: highest score, earliest on a tie."""
    ranked = sorted(CANDIDATES, key=lambda line: (-score(line), CANDIDATES.index(line)))
    return ranked[0]


def main() -> None:
    line = pick_best()
    assert 1 <= len(line) <= 200, "line must fit the 1-200 character gate"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as fh:
        fh.write(line)
    print(f"picked ({len(line)} chars): {line}")


if __name__ == "__main__":
    main()
