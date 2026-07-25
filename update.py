import json
import os
import subprocess
from datetime import datetime, timedelta

REPO = "/home/elias/HowManyMondaysLeft"
os.chdir(REPO)
FILE = "mondays.json"

today = datetime.now()
current_year = today.year

def all_mondays_remaining(from_date):
    """Alle Montage vom heutigen Tag bis Jahresende (inkl. heute falls Montag)."""
    year_end = datetime(from_date.year, 12, 31)
    mondays = []
    d = from_date
    while d <= year_end:
        if d.weekday() == 0:  # 0 is Montag
            mondays.append(d.strftime("%-m/%-d/%Y"))
        d += timedelta(days=1)
    return mondays

# load  the file
if os.path.exists(FILE):
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
else:
    data = {}

if not isinstance(data, dict):
    data = {}

changed = False

# new list when new year
if data.get("year") != current_year:
    data = {
        "year": current_year,
        "mondays": all_mondays_remaining(today)
    }
    changed = True
else:
    # removing mondays which happened
    mondays = data.get("mondays", [])
    new_mondays = [m for m in mondays if datetime.strptime(m, "%m/%d/%Y") >= today.replace(hour=0, minute=0, second=0, microsecond=0)]
    if new_mondays != mondays:
        data["mondays"] = new_mondays
        changed = True

if changed:
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

    subprocess.run(["git", "add", FILE], check=True)
    subprocess.run(["git", "commit", "-m", f"{len(data['mondays'])} Mondays left ({today.strftime('%-m/%-d/%Y')})"], check=True)
    subprocess.run(["git", "push"], check=True)
    print(f"{len(data['mondays'])} Mondays left")
else:
    print("Nothing changed today.")
