from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agent import make_brief

BASE = "Write a concise one-page brief with Snapshot, Bull case, Bear case and Open questions. Cite facts using the supplied source IDs. Use only these documents and do not browse the web."

EXPERIMENTS = [
    ("run_1_basic.md", BASE),
    ("run_2_source_priority.md", BASE + " Prioritize company releases and exchange filings over news articles. Clearly explain any conflicting numbers."),
    ("run_3_strict.md", (ROOT / "system_prompt.md").read_text(encoding="utf-8")),
]


def main():
    out = ROOT / "experiments"
    out.mkdir(exist_ok=True)
    for filename, prompt in EXPERIMENTS:
        print(f"Running {filename}...")
        brief = make_brief("SRVCABLE", prompt)
        (out / filename).write_text(brief, encoding="utf-8")
        print(f"Saved {out / filename}")
    print("Review the three outputs and write down what improved between runs.")


if __name__ == "__main__":
    main()
