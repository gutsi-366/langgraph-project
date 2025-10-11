# src/lib/storage.py
from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

ROOT = Path(__file__).resolve().parents[2]  # .../langgraph_project
RUNS = ROOT / "outputs" / "runs"
CRAWLS = ROOT / "outputs" / "crawls"
RUNS.mkdir(parents=True, exist_ok=True)
CRAWLS.mkdir(parents=True, exist_ok=True)

# -------- Analysis runs --------
def save_run(results: Dict[str, Any]) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    p = RUNS / f"run-{ts}.json"
    p.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    return str(p)

def list_runs() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for p in sorted(RUNS.glob("run-*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        items.append({
            "id": p.stem,
            "path": str(p),
            "summary": data.get("key_metrics") or data.get("dataset_info") or {}
        })
    return list(reversed(items))

def load_run(run_id: str) -> Optional[Dict[str, Any]]:
    p = RUNS / f"{run_id}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

# -------- Crawls --------
def save_crawl(data: Dict[str, Any]) -> str:
    """Save a single crawl result as JSON and return its path."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    p = CRAWLS / f"crawl-{ts}.json"
    p.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return str(p)

def list_crawls() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for p in sorted(CRAWLS.glob("crawl-*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        items.append({
            "id": p.stem,
            "path": str(p),
            "title": data.get("title"),
            "url": data.get("url"),
            "link_count": data.get("link_count", 0),
        })
    return list(reversed(items))
