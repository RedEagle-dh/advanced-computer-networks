# Lab L3 — SDN & OpenFlow mit Mininet

**Advanced Computer Networks · HS Fulda · MMNet**
Ersetzt die früheren Labs `4_mininet_intro`(+part2) und `5_openflow_intro` (learn-sdn-hub-VM).
Ziel: Mininet, Open vSwitch und einen OpenFlow-Controller **selbst** betreiben — und verstehen,
warum ein Switch ohne Control Plane nichts weiterleitet.

---

## Lernziele

- Mininet-Topologien per CLI und Python-API bauen (`mn`, `pingall`, `iperf`, `dump`/`links`)
- Open vSwitch mit `ovs-vsctl`/`ovs-ofctl` inspizieren (Ports, Flow-Tabellen, OpenFlow-Versionen)
- Einen OpenFlow-Controller (os-ken, die gepflegte Ryu-Gabelung) mit einer eigenen App betreiben
- Verstehen: Data Plane ohne Flow-Einträge = Schwarzes Loch; Control Plane programmiert die Flows

## Voraussetzungen

- Linux mit Docker und `containerlab ≥ 0.56`; **Internet** für den ersten Image-Build
- Lab-Image einmalig selbst bauen (Ubuntu 24.04 + Mininet 2.3.0 + OVS 3.3.9 + os-ken 4.2.2):
  ```bash
  cd Labs/L3_sdn_mininet
  docker build -t acn-l3-mininet:2026.10 .
  ```
  Ryu selbst ist seit 04/2024 ohne Commits und baut auf Python 3.12 nicht mehr — os-ken
  (OpenStack-Gabelung) ist der Ersatz. **Stolperfalle:** die os-ken-Wheels enthalten weder
  `os_ken/cmd` (Manager) noch `app/wsgi` — beides liegt hier als portierter Patch bei
  (`osken_patch/`), inkl. `osken-manager` als Ersatz für `ryu-manager`.

**Aufwand:** ca. 90–120 Minuten · Bearbeitung in Zweiergruppen

---

## Umgebung

```bash
cd Labs/L3_sdn_mininet
containerlab deploy  -t sdn.clab.yml     # startet den Knoten, OVS-Daemon inklusive
docker exec -it clab-acn-l3-mininet-mininet bash
containerlab destroy -t sdn.clab.yml --cleanup
```

Alles Weitere passiert **im Knoten** (Sie sind dort root): zuerst `cd /lab` — dort liegen die
Lab-Dateien (`OpenFlowTopo.py`, `OpenFlowApp.py`, …). Das Mininet-Netz besteht aus
Netzwerk-Namespaces *im Container* — es braucht keinen Controller-Container extra; der
os-ken-Controller läuft im selben Knoten und verbindet sich über `127.0.0.1:6633`.

---

## Aufgabe 1 — Mininet-Basics

1. Standard-Topologie mit Default-Controller (L2-Learning, wie im Bachelor):
   ```bash
   mn --test pingall
   mn -c   # falls eine alte Topologie noch läuft
   ```
2. Interaktiv: `mn` starten und die CLI erkunden:
   ```text
   mininet> help          mininet> nodes / net / links / ports
   mininet> dump          mininet> h1 ping -c3 h2
   mininet> iperf h1 h2   mininet> h1 ifconfig   (alt: ip addr)
   mininet> exit
   ```
3. **Frage:** Welche Komponenten erzeugt `dump`? Wer ist hier der Controller und was macht
   er (`ovs-ofctl dump-flows s1` während `mn` läuft, zweites Terminal)?

## Aufgabe 2 — OpenFlow-Switch ohne Controller

1. Starten Sie die bereitgestellte Topologie mit **entferntem** Controller
   (`OpenFlowTopo.py` verbindet sich auf `127.0.0.1:6633`, auf dem noch niemand lauscht):
   ```bash
   printf "pingall\nexit\n" | python3 OpenFlowTopo.py
   ```
   Alternativ interaktiv: `python3 OpenFlowTopo.py` und im `mininet>`-Prompt arbeiten.
2. **Frage:** Warum schlägt `pingall` fehl? Was hat der OVS-Switch im vorherigen Abschnitt
   bei `h1 ping h2` gemacht? (Hinweis: `fail_mode: secure` — `ovs-vsctl show`.)
3. Inspizieren Sie den Switch (in einem zweiten Terminal, während `OpenFlowTopo.py` läuft):
   ```bash
   ovs-vsctl show
   ovs-ofctl show ofp-sw1              # welche OpenFlow-Version verhandelt OVS?
   ovs-ofctl dump-flows ofp-sw1        # wie viele Flows stehen in der Tabelle?
   ```

## Aufgabe 3 — OpenFlow-Controller (os-ken)

1. Lesen Sie `OpenFlowApp.py`: Die App holt sich den Datapath per `dpset`, programmiert
   Flows per `OFPFlowMod` — mit **Platzhalter-Werten** (in_port=0, MACs `aa:bb:…`, IPs
   `1.2.3.4`). Überlegen Sie zuerst: Welche Flows braucht ICMP-Kommunikation zwischen
   h1 und h2? Welche Match-Felder und Actions? (Tipp: `dl_type` 0x0800 = IPv4, 0x0806 = ARP.)
2. Überprüfen Sie die MACs der Hosts (`OpenFlowTopo.py` setzt sie fix:
   `ba:de:af:fe:00:01` / `ba:de:af:fe:00:02`).
3. Starten Sie die bereitgestellte **Lazy**-Lösung (flootet unbekannte Ziele an alle Ports).
   **Reihenfolge wie im alten VM-Lab — zwei Terminals:** erst Mininet, dann der Controller
   (die App installiert ihre Flows erst **10 Sekunden** nach Controller-Start, Timer im
   Quellcode — ist zu dem Zeitpunkt keine Topologie verbunden, gehen die Flows ins Leere):
   ```bash
   # Terminal 1 (MININET):
   python3 OpenFlowTopo.py            # → mininet> Prompt offen halten
   # Terminal 2 (CONTROLLER):
   nohup osken-manager OpenFlowAppLazySolution.py >/tmp/osken.log 2>&1 &
   ```
   ~10 s warten, dann im `mininet>`-Prompt: `pingall`.
   Beobachten Sie den Übergang von **100 % Verlust** (vor den Flows) zu **0 %** (danach)
   — genau der Lehrmoment dieser Aufgabe.
4. Prüfen Sie die installierten Flows (während der Topologie läuft):
   `ovs-ofctl dump-flows ofp-sw1` — und löschen Sie sie wieder:
   `ovs-ofctl del-flows ofp-sw1`. Was passiert mit laufenden Pings?
5. **Vertiefung (optional):** Schreiben Sie die **Smart**-Variante: exakte L2-Matches
   (`dl_src`/`dl_dst` + `in_port`) statt Flood — Lösungsidee in `OpenFlowAppSmartSolution.py`
   (in der alten Materialablage). Wie unterscheidet sich das Verhalten bei Broadcast?

## Aufgabe 4 — Reflexion

1. **Wozu SDN?** Vorteile (zentrale Gesamtsicht, programmierbare Netzlogik) vs. Nachteile
   (Single Point of Failure, Skalierung, Kosten) — vgl. K4 (Google B4, ONOS).
2. **Frage:** OpenFlow wird in der Praxis großflächig durch proprietäre SDN-Lösungen abgelöst —
   was bleibt vom Prinzip erhalten? (K4: Trennung Control/Data Plane, northbound APIs.)
3. **Ausblick:** In L4 programmieren Sie die Data Plane selbst in P4 — was unterscheidet
   einen per OpenFlow programmierbaren Switch von einem P4-Switch?

---

## Verifikation (erwartete Ergebnisse)

| Prüfschritt | Erwartung |
|---|---|
| `mn --test pingall` | 2/2 empfangen, 0 % Verlust (Default-Controller, L2-Learning) |
| `OpenFlowTopo.py` ohne laufenden Controller | `pingall` **100 % Verlust**, Flow-Tabelle leer |
| `ovs-vsctl show` | Bridge `ofp-sw1`, `is_connected: true` sobald os-ken läuft |
| os-ken-Lazy-App + 10 s Timer | Log `add flows: [dp=0000000000000001]` |
| `pingall` **nach** Flow-Installation | **0 % Verlust** (2/2) |
| `ovs-ofctl del-flows ofp-sw1` | laufender Ping bricht ab (nächste Pakete gedroppt) |

## Troubleshooting

- **`mn --test pingall` bricht mit "Error connecting to ovs-db" ab:** der OVS-Daemon läuft
  noch nicht — im clab-Deploy startet ihn ein `exec` automatisch; manuell:
  `/usr/share/openvswitch/scripts/ovs-ctl start`.
- **`osken-manager: not found`** (außerhalb des Lab-Images): der Manager kommt aus dem
  Patch (`osken_patch/`), nicht aus dem os-ken-Wheel — Lab-Image verwenden.
- **`AttributeError: ... no attribute 'RyuApp'`:** os-ken heißt die Basisklasse `OSKenApp`
  — die beigelegten Dateien sind bereits angepasst; beim Übernehmen eigener alter Apps
  entsprechend ändern.
- **Ping bleibt bei 100 %, obwohl der Controller läuft:** die Lazy-App braucht **10 s**
  bis zur Flow-Installation (`threading.Timer`) — erneut pingen; und es darf nur **eine**
  os-ken-Instanz laufen (`pgrep -af osken`, sonst streiten zwei um Port 6633).
- **`py …`-Befehle mit Semikolon in der mininet-CLI funktionieren nicht zuverlässig** —
  zum Halten der Sitzung besser `h1 ping -cN` verwenden.
- **Alles hängt:** `containerlab destroy -t sdn.clab.yml --cleanup` und neu deployen.

## Bezug zur Vorlesung

- Kapitel 4 (SDN): Control/Data-Plane-Trennung, OpenFlow als southbound-Protokoll,
  Google B4/Orion (zentrale Control mit Edge-Verteilung)
- Kapitel 1/2: L2-Learning (Flood & Filter) als Vergleichspunkt zum programmierbaren Switch
- Kapitel 6 (P4): Abgrenzung OpenFlow (vorgefertigte Actions) vs. P4 (eigene Pipeline)
