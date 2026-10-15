# Lab L4 — Programmierbare Data Plane: P4 auf bmv2

**Advanced Computer Networks · HS Fulda · MMNet**
Ersetzt das frühere `5_p4_intro` (learn-sdn-hub-VM). Ziel: die P4-Toolchain **selbst** bedienen —
kompilieren, laden, Laufzeit-Tabellen manipulieren — statt per Weboberfläche deployen zu lassen.

---

## Lernziele

- P4-Programme mit `p4c` kompilieren (bmv2-Target, v1model-Architektur) und in `simple_switch` laden
- Laufzeit-Tabellen per `simple_switch_CLI` manipulieren (`table_add`, Multicast-Gruppen)
- Verstehen, wie Parser → Ingress → Egress → Deparser zusammenspielen
- Grenzen und Stärken der Software-Data-Plane einordnen (vgl. K6: Tofino-EOL, DPUs/IPUs)

## Voraussetzungen

- Linux mit **Docker** und `containerlab ≥ 0.56`; **Internet** für den ersten Image-Build
- Images: `alpine:3.20` (Hosts) + das Lab-Image, das Sie einmalig selbst bauen:
  ```bash
  cd Labs/L4_p4_intro
  docker build -t acn-l4-p4:2026.10 .
  ```
  Das Image kombiniert die offiziell gepflegten p4lang-Images `p4lang/p4c` (p4c 1.2.5.18) und
  `p4lang/behavioral-model` (bmv2 1.15.7, identische Ubuntu-24.04-Basis). Der frühere
  `prona/p4-container` (p4c 1.2.3.6, OVS-/learn-sdn-hub-Ballast) wird upstream nicht mehr gepflegt
  (letzter Commit 11/2022) und wird hier nicht mehr verwendet.

**Aufwand:** ca. 90–120 Minuten · Bearbeitung in Zweiergruppen empfohlen

---

## Topologie

```
 h1 ──────── switch (bmv2) ──────── h2
10.0.0.1/24   eth1→Port1, eth2→Port2   10.0.0.2/24
```

- **switch**: unser Image, startet `simple_switch` mit dem kompilierten P4-Programm
- **h1/h2**: Alpine-Hosts mit statischen IPs (gleiche L2-Domain, kein Gateway nötig)

```bash
cd Labs/L4_p4_intro
containerlab deploy  -t p4.clab.yml     # baut Beispiel 1 (Repeater) automatisch
containerlab inspect -t p4.clab.yml
containerlab destroy -t p4.clab.yml --cleanup
```

---

## Aufgabe 1 — Repeater: erster Kontakt mit der Pipeline

1. Deployen Sie die Topologie. `ping -c3 10.0.0.2` von `h1` — warum funktioniert das
   **ohne** Tabelleneinträge und ohne ARP-Konfiguration?
2. Lesen Sie `p4/repeater.p4` im Lab-Verzeichnis (bzw. `/p4/` im Container): Wo entscheidet
   sich, zu welchem Port ein Paket geht? Welche Pipeline-Phasen sieht man, und welche
   sind hier bewusst leer?
3. **Frage:** Was müsste sich ändern, damit der Repeater auch Pakete zwischen
   *drei* Hosts weiterleiten könnte — und warum stößt dieses Programm dort an seine Grenze?

## Aufgabe 2 — Minimalistischer L2-Switch: Tabellen und Multicast

Wechseln Sie im `switch`-Container auf Beispiel 2 (das Programm hat **keine**
voreingetragenen Regeln und droppt per Default):

```bash
# im switch-Container (docker exec -it clab-acn-l4-p4-switch sh):
pkill -x simple_switch                                   # alten Switch beenden
p4c --target bmv2 --arch v1model /p4/l2switch.p4 -o /tmp/build/l2switch
exit
# vom Host — detached starten, sonst stirbt simple_switch mit der exec-Sitzung:
docker exec -d clab-acn-l4-p4-switch sh -c \
  'simple_switch --thrift-port 9090 -i 1@eth1 -i 2@eth2 /tmp/build/l2switch/l2switch.json'
```

1. Bevor Sie irgendetwas eintragen: `ping` von `h1` — was passiert und warum?
   (Hinweis: ARP ist ein Broadcast an `ff:ff:ff:ff:ff:ff`.)
2. Befüllen Sie die Laufzeit-Tabellen. Lesen Sie zuerst die MACs der Hosts
   (`ip link show eth1` auf `h1`/`h2`), dann per `simple_switch_CLI`:
   ```text
   mc_mgrp_create 1                                        # Multicast-Gruppe
   mc_node_create 0 1 2                                    # Node: Ports 1 und 2 (dezimal!)
   mc_node_associate 1 0
   table_add forwarding broadcast ff:ff:ff:ff:ff:ff =>     # Broadcast → Gruppe
   table_add forwarding forward <mac-h1> => 1
   table_add forwarding forward <mac-h2> => 2
   ```
   Kontrollieren Sie mit `table_dump` und `mc_dump`. Danach: `ping` von `h1` —
   RTT vergleichen mit Aufgabe 1.
3. **Frage:** Warum braucht der Broadcast einen eigenen Tabelleneintrag, obwohl die
   Multicast-Gruppe bereits existiert? Was passiert mit einem Paket, dessen
   Ingress-Port in der Multicast-Gruppe liegt? (Prüfen Sie die Doku in `l2switch.p4`.)
4. **Frage:** Löschen Sie per `table_delete forwarding <handle>` den Eintrag von `h2`
   und pingen Sie erneut. Warum schlägt der Ping jetzt fehl, obwohl `h1` die MAC von
   `h2` längst im ARP-Cache hat? (Nicht vergessen: Eintrag wiederherstellen.)

## Aufgabe 3 — Direkte Tool-Nutzung

1. `p4c --help` — welche Targets und Architekturen kennt der Compiler? Wofür ist
   `--p4runtime-files` gedacht (Ausblick: P4Runtime-gesteuerte Switches)?
2. Sehen Sie sich `/tmp/simple_switch.log` und `mc_dump` an: Wie "sieht" die Software-Data-Plane
   die Ports? Wo ist der Unterschied zu physischen Switch-ASICs?
3. **Frage:** In `l2switch.p4` steht `default_action = drop()`. Warum ist das für eine
   Sicherheitsbetrachtung die richtige Voreinstellung — und was spricht in einem echten
   Netz dagegen, UNbekannte MACs einfach zu droppen? (Stichwort: MAC-Learning, `ageing`)

## Aufgabe 4 — Reflexion

1. Vergleichen Sie mit dem alten Weg (learn-sdn-hub-VM): Was ist einfacher, was fehlt?
2. **Ausblick:** Die Software-Data-Plane (bmv2) schafft je nach Rechner wenige hundert Kbit/s
   bis wenige Mbit/s — warum ist sie trotzdem das richtige Werkzeug, um P4 zu *lehren*?
   Wo liegt der Stand der Hardware (Tofino EOL, DPUs/IPUs, quelloffene Toolchain — K6)?

---

## Verifikation (erwartete Ergebnisse)

| Prüfschritt | Erwartung |
|---|---|
| `containerlab inspect` | 3 Knoten `running` |
| `ping` h1 → h2 (Beispiel 1, Repeater) | 0 % Verlust, RTT < 2 ms — ohne Tabelleneinträge |
| `p4c`-Kompilat | `/tmp/build/<name>/<name>.json` (p4c 1.2.5 schreibt ein **Verzeichnis**) |
| `ping` h1 → h2 (Beispiel 2, **vor** Einträgen) | 100 % Verlust (Default-Drop, auch ARP) |
| `table_dump` nach Befüllung | 3 Einträge: broadcast + 2 × forward |
| `mc_dump` | `mgrp(1) → (rid=0) → ports=[1, 2]` |
| `ping` h1 → h2 (Beispiel 2, **nach** Einträgen) | 0 % Verlust, RTT < 2 ms |

## Troubleshooting

- **`pkill -f simple_switch` tötet Ihre eigene Shell:** der Filter matcht auch die
  `sh -c`-Kommandozeile des exec-Aufrufs. Immer `pkill -x simple_switch` verwenden.
- **`simple_switch` stirbt, sobald Ihr `docker exec` endet:** Hintergrundstart mit
  `docker exec -d` (detached), nicht mit `&` in einer normalen exec-Sitzung.
- **`table_delete forwarding 0x2` → "Bad format for entry handle":** `table_dump` zeigt Handles
  mit `0x`-Präfix, das Löschen erwartet sie **dezimal ohne Präfix** (`table_delete forwarding 2`).
- **`mc_node_create 0 0x6` → "not a valid port number":** die CLI erwartet **dezimale
  Port-Nummern als Einzelargumente** (`mc_node_create 0 1 2`), keine Hex-Bitmaps.
- **`table_add` mit parameterloser Aktion:** das abschließende `=>` ist Pflicht
  (`table_add forwarding broadcast ff:ff:ff:ff:ff:ff =>`).
- **`mc_node_associate` meldet nichts, aber `mc_dump` zeigt keinen Node:** die
  Reihenfolge ist create → associate; ein Associate vor erfolgreichem Create geht verloren.
- **Kein Internet im Container (`apk`/Image-Pull hängt):** die Topologie setzt das
  Mgmt-Netz auf IPv4-only (`ipv6-subnet: ""`, Stolperfalle 9); hinter VPN ggf. im
  Container `echo "nameserver 9.9.9.9" > /etc/resolv.conf`.
- **Alles hängt:** `containerlab destroy -t p4.clab.yml --cleanup` und neu deployen.

## Bezug zur Vorlesung

- Kapitel 6 (Programmierbare Data Plane): PISA-Modell, Parser/Match-Action/Deparser, v1model
- Kapitel 4/6: Control-Plane/Data-Plane-Trennung — hier läuft die Control-Plane als CLI
  anstelle eines Controllers (Beispiel 3 im alten Lab, Learning-Switch mit P4Runtime-Controller,
  ist als Ausbaustufe möglich: `simple_switch_grpc` + `p4runtime-shell` sind im Image enthalten)
- Kapitel 6 („Was nach Tofino kommt"): Software-Modell vs. Hardware-Reality
