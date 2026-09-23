import argparse
import csv
import logging
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("analyser")


def parse_args():
    parser = argparse.ArgumentParser(description="Summarise sensor readings.")
    parser.add_argument("--input", default="/data/readings.csv")
    parser.add_argument("--output", default="/data/summary.txt")
    return parser.parse_args()


def load_readings(path):
    readings = {}
    skipped = 0
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            sensor = (row.get("sensor") or "").strip()
            raw = (row.get("value") or "").strip()
            if not sensor or not raw:
                skipped += 1
                continue
            try:
                readings.setdefault(sensor, []).append(float(raw))
            except ValueError:
                skipped += 1
    return readings, skipped


def build_report(readings, source):
    lines = [
        "SWE40006 Task 4.4 sensor summary",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"Source: {source}",
        "",
        f"{'Sensor':<16}{'Count':>8}{'Min':>12}{'Max':>12}{'Mean':>12}{'Median':>12}",
        "-" * 72,
    ]
    for sensor in sorted(readings):
        values = readings[sensor]
        lines.append(
            f"{sensor:<16}{len(values):>8}{min(values):>12.2f}{max(values):>12.2f}"
            f"{statistics.mean(values):>12.2f}{statistics.median(values):>12.2f}"
        )
    return "\n".join(lines) + "\n"


def main():
    args = parse_args()
    log.info("Analyser starting")
    log.info("Reading %s", args.input)

    source = Path(args.input)
    if not source.exists():
        log.error("Input file not found: %s", source)
        return 1

    readings, skipped = load_readings(source)
    if not readings:
        log.error("No usable rows found in %s", source)
        return 1

    total = sum(len(v) for v in readings.values())
    log.info("Loaded %d readings across %d sensors", total, len(readings))
    if skipped:
        log.warning("Skipped %d malformed rows", skipped)

    report = build_report(readings, source.name)
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(report, encoding="utf-8")

    log.info("Report written to %s", destination)
    log.info("Analyser finished successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
