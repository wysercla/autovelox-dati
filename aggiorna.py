import json, urllib.request, urllib.parse, time

dati = {}
zone = [
    "36.5,12.2,38.4,15.8",
    "38.8,8.0,41.4,10.0",
    "37.8,15.3,42.3,18.6",
    "39.9,13.7,42.9,15.9",
    "41.1,11.4,43.5,14.2",
    "42.2,9.7,44.5,12.8",
    "43.5,9.2,45.1,14.0",
    "43.7,6.6,46.5,9.3",
    "44.6,8.5,46.6,11.5",
    "44.8,10.4,47.1,13.9"
]
srv1 = "https://" + "maps.mail.ru/osm/tools/overpass/api/interpreter"
srv2 = "https://" + "overpass-api.de/api/interpreter"
servers = [srv1, srv2]
zone_ok = 0

for b in zone:
    q = '[out:json][timeout:60];node["highway"="speed_camera"](' + b + ');out tags qt;'
    data = urllib.parse.urlencode({"data": q}).encode("utf-8")
    for t in range(4):
        try:
            req = urllib.request.Request(servers.__getitem__(t % 2), data=data, headers={"Accept": "application/json", "User-Agent": "Autovelox3008/1.0"})
            with urllib.request.urlopen(req, timeout=65) as r:
                for o in json.loads(r.read().decode("utf-8")).get("elements", []):
                    if "lat" in o and "lon" in o:
                        dati[o["id"]] = [o["id"], o["lat"], o["lon"], o.get("tags", {}).get("maxspeed", "N/D")]
                zone_ok += 1
                break
        except Exception:
            time.sleep(6)
    time.sleep(2)

if zone_ok >= 8 and len(dati) > 2500:
    with open("autovelox_italia.json", "w") as f:
        json.dump(list(dati.values()), f, separators=(",", ":"))
    print("AGGIORNAMENTO FISSI + TUTOR + SEMAFORI OK! Zone:", zone_ok, "Totale:", len(dati))
else:
    print("Server occupati (zone OK:", zone_ok, "), mantengo il file esistente.")
