"""Refresh public ModelScope counters without credentials or dataset downloads.

Run with Python 3.9+: python scripts/refresh_metrics.py
Only replaces metrics.json after BOTH requested counters have been validated.
"""
import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_API = "https://modelscope.cn/api/v1/datasets/wyswyswys/TC-SAR-Coast"
DATASET_URL = "https://modelscope.cn/datasets/wyswyswys/TC-SAR-Coast"
STUDIO_URL = "https://modelscope.cn/studios/wyswyswys/TyphoonSAR-Copilot"


def get_text(url):
    # Both names are official public ModelScope endpoints. Overseas runners can
    # intermittently time out on one CDN route; retry only transient failures.
    alternate = url.replace("https://modelscope.cn/", "https://www.modelscope.cn/")
    for attempt, (target, timeout) in enumerate([(alternate, 25), (url, 25), (alternate, 40)]):
        request = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            if error.code not in {408, 429, 500, 502, 503, 504} or attempt == 2:
                raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == 2:
                raise
        time.sleep(2)


def counter(value, field):
    if type(value) is not int or value < 0:
        raise ValueError(f"Invalid or unavailable {field}: {value!r}")
    return value


def refresh_metrics():
    dataset_raw = get_text(DATASET_API)
    dataset_response = json.loads(dataset_raw)
    if dataset_response.get("Code") != 200:
        raise ValueError("ModelScope dataset API did not return success")
    dataset = dataset_response["Data"]
    if dataset.get("Namespace") != "wyswyswys" or dataset.get("Name") != "TC-SAR-Coast":
        raise ValueError("Unexpected dataset identity")

    studio_raw = get_text(STUDIO_URL)
    match = re.search(r'window\.__detail_data__\s*=\s*("(?:\\.|[^"\\])*")\s*;', studio_raw)
    if not match:
        raise ValueError("Studio embedded detail JSON was not found; keep the previous snapshot")
    studio = json.loads(json.loads(match.group(1)))
    if studio.get("Name") != "TyphoonSAR-Copilot" or studio.get("Path") != "wyswyswys":
        raise ValueError("Unexpected Studio identity")

    now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
    metrics = {
        "schema_version": 1,
        "observed_at": now,
        "timezone": "Asia/Shanghai",
        "display_note": "Platform counters as of the observation date; not unique users or verified full-dataset acquisitions.",
        "items": [
            {"id": "modelscope-dataset-downloads", "label": "ModelScope dataset downloads", "value": counter(dataset.get("Downloads"), "Downloads"), "unit": "platform-counted downloads", "url": DATASET_URL, "source_url": DATASET_API, "source_field": "Data.Downloads", "source_type": "public_api"},
            {"id": "modelscope-studio-visits", "label": "ModelScope Studio visits", "value": counter(studio.get("Visits"), "Visits"), "unit": "visits", "url": STUDIO_URL, "source_url": STUDIO_URL, "source_field": "window.__detail_data__.Visits", "source_type": "public_html_embedded_json"}
        ]
    }
    stamp = datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d-%H%M%S")
    evidence = ROOT / "work" / "metrics" / stamp
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "dataset-response.json").write_text(dataset_raw, encoding="utf-8")
    (evidence / "studio-page.html").write_text(studio_raw, encoding="utf-8")
    (evidence / "studio-detail.json").write_text(json.dumps(studio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "content").mkdir(exist_ok=True)
    destination = ROOT / "content" / "metrics.json"
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(destination)
    return metrics


def main():
    metrics = refresh_metrics()
    print(f"Saved {ROOT / 'content' / 'metrics.json'}")
    for item in metrics["items"]:
        print(f"{item['id']}: {item['value']:,}")
    print(f"Observed at: {metrics['observed_at']}")


if __name__ == "__main__":
    main()
