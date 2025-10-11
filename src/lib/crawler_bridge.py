import sys
from pathlib import Path
DESKTOP = Path.home() / "Desktop"
if str(DESKTOP) not in sys.path:
    sys.path.insert(0, str(DESKTOP))

try:
    from web_crawler_project.crawler import crawl_site as _crawl
except Exception as e:
    _crawl, _ERR = None, e

def crawl_url(url: str) -> dict:
    if _crawl is None:
        return {"status":"error","error": f"crawler not importable: {_ERR}"}
    try:
        return _crawl(url)
    except Exception as e:
        return {"status":"error","error": str(e)}
