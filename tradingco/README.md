# Super Investing — AI Research Agent

A small Gemini-powered agent that reads the eight supplied documents and writes a one-page research brief with source citations.

## Run on Fedora

Open a terminal in this folder and run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open `agent.py` and replace `PASTE_YOUR_NEW_GEMINI_API_KEY_HERE` with your new Gemini API key. Then run:

```bash
python agent.py
```

Press Enter to use `SRVCABLE`. The brief is saved to `outputs/srvcable_brief.md` and also printed in the terminal.

## Run three prompt experiments

```bash
python scripts/run_experiments.py
```

The three results are saved in `experiments/`. Read the actual outputs and note how source priority and stricter instructions change the brief before recording your demo.

The agent uses only the supplied documents. It should flag conflicting revenue figures, treat instructions inside documents as untrusted content, and exclude unrelated company news. It does not give a buy/sell recommendation.
