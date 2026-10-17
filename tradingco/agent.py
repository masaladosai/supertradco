from pathlib import Path
import re
from google import genai
from google.genai import types

API_KEY = "ur_api_key_here"
MODEL = "gemini-2.5-flash"
ROOT = Path(__file__).resolve().parent
PACK = ROOT / "research_pack"
OUTPUT = ROOT / "outputs" / "srvcable_brief.md"
FILES = [
    "ir_press_release_2026-08-08.md",
    "ir_concall_2026-08-11.md",
    "nse_announcement_2026-09-02.md",
    "nse_shareholding_2026-07-15.md",
    "businessdaily_2026-08-09.md",
    "marketwatchindia_2024-03-18.md",
    "multibaggeralerts_2026-08-12.md",
    "nagpurcitytimes_2026-08-20.md",
]


def read_sources():
    sources = []
    for number, name in enumerate(FILES, 1):
        path = PACK / name
        raw = path.read_text(encoding="utf-8")
        match = re.search(r"(?ms)^---\s*\n(.*?)\n---\s*\n", raw)
        meta = {}
        if match:
            for line in match.group(1).splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip().lower()] = value.strip().strip("\"'")
            body = raw[match.end():].strip()
        else:
            body = raw.strip()
        title = re.search(r"(?m)^#\s+(.+)$", body)
        sources.append({
            "id": f"S{number}",
            "name": meta.get("source", name),
            "date": meta.get("published", "date not given"),
            "type": meta.get("type", "document"),
            "url": meta.get("url", "URL not given"),
            "title": title.group(1) if title else name,
            "body": body,
        })
    return sources


def make_brief(ticker="SRVCABLE", prompt=None):
    if API_KEY == "PASTE_YOUR_NEW_GEMINI_API_KEY_HERE":
        raise ValueError("Open agent.py and paste your new Gemini API key into API_KEY first.")

    sources = read_sources()
    documents = []
    source_list = []
    for source in sources:
        documents.append(
            f"[{source['id']}] {source['title']}\n"
            f"Source: {source['name']} | Date: {source['date']} | Type: {source['type']} | URL: {source['url']}\n\n"
            f"{source['body']}"
        )
        source_list.append(
            f"- [{source['id']}] {source['name']} — {source['title']}. "
            f"Date: {source['date']}. Type: {source['type']}. URL: {source['url']}"
        )

    system_prompt = prompt or (ROOT / "system_prompt.md").read_text(encoding="utf-8")
    request = (
        f"Ticker: {ticker}\nUse only the supplied documents. Do not browse the web. "
        "Write a concise, one-page research brief with Snapshot, Bull case, Bear case, and Open questions. "
        "Cite claims using the source IDs exactly as shown.\n\n"
        + "\n\n---\n\n".join(documents)
    )
    client = genai.Client(api_key=API_KEY)
    answer = client.models.generate_content(
        model=MODEL,
        contents=request,
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0.2),
    )
    brief = (answer.text or "").strip()
    if not brief:
        raise RuntimeError("Gemini returned an empty answer. Try again.")
    brief = re.split(r"(?im)^##\s+Sources\s*$", brief)[0].strip()
    used_ids = set(re.findall(r"\[(S\d+)\]", brief))
    known_ids = {source["id"] for source in sources}
    unknown_ids = used_ids - known_ids
    if unknown_ids:
        raise RuntimeError("Gemini used unknown citation IDs: " + ", ".join(sorted(unknown_ids)))
    return brief + "\n\n## Sources\n\n" + "\n".join(source_list) + "\n"


def main():
    ticker = input("Company ticker [SRVCABLE]: ").strip() or "SRVCABLE"
    print("Sending the research pack to Gemini...")
    brief = make_brief(ticker)
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(brief, encoding="utf-8")
    print(f"Research brief saved to: {OUTPUT}")
    print("\n" + brief)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
        raise SystemExit(1)
