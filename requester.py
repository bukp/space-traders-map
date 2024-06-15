import requests
import json
import time

duration = time.time()
systems = []
total = 8498

while len(systems) < 8498:
    result = json.loads(requests.get("https://api.spacetraders.io/v2/systems", {"limit" : 20, "page" : len(systems)//20+1}).text)
    systems += result["data"]
    print(" "*200, end="\r")
    print(f" => requesting from {(len(systems)//20+1)*20-19} to {(len(systems)//20+1)*20}")
    print(f"[<{'=' * (len(systems) * 100 // 8498)}>{' ' * (100 - (len(systems) * 100 // 8498))}] {len(systems)}/{total}", end="\r")
print()

with open("systems.json", "w") as file:
    json.dump(systems, file, indent=3)

duration = time.time() - duration
print(f"Completed in {int(duration//60)} minutes and {int(duration%60//1)} secondes")