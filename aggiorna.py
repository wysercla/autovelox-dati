import json, urllib.request, urllib.parse, time

with open("autovelox_italia.json") as f:
    dati = {}
    for row in json.load(f):
        dati[row.__getitem__(0)] = row

zone = [
    "35.4,6.6,42.5,18.6",
    "42.5,6.6,45.0,18.6",
    "45.0,6.6,45.7,14.0",
    "45.7,6.6,47.1,10.5",
    "45.7,10.5,47.1,13.9"
]
srv1 = "https://" + "maps.mail.ru/osm/tools/overpass/api/interpreter"
srv2 = "https://" + "overpass-api.de/api/interpreter"
servers = [srv1, srv2]

for b in zone:
    p1 = 'node["highway"="speed_camera"](' + b + ');'
    p2 = 'node["man_made"="enforcement"](' + b + ');'
    q = '[out:json][timeout:45];(' + p1 + p2 + ');out tags qt;'
    data = urllib.parse.urlencode({"data": q}).encode("utf-8")
    for t in range(4):
        try:
            req = urllib.request.Request(servers.__getitem__(t % 2), data=data, headers={"Accept": "application/json", "User-Agent": "Autovelox3008/1.0"})
            with urllib.request.urlopen(req, timeout=50) as r:
                for o in json.loads(r.read().decode("utf-8")).get("elements", []):
                    if "lat" in o and "lon" in o:
                        dati[o["id"]] = [o["id"], o["lat"], o["lon"], o.get("tags", {}).get("maxspeed", "N/D")]
                break
        except Exception:
            time.sleep(5)
    time.sleep(2)

with open("autovelox_italia.json", "w") as f:
    json.dump(list(dati.values()), f, separators=(",", ":"))
print("AGGIORNAMENTO COMPLETATO! Totale punti:", len(dati))
