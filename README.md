# Advanced Computer Networks — Foliensatz

Foliensatz und Ablaufplan der Lehrveranstaltung **Advanced Computer Networks** im Master AI an der
Hochschule Fulda, Prof. Sebastian Rieger · MMNet.

Die Veranstaltung behandelt die Netzinfrastruktur moderner Rechenzentren und Cloud-Umgebungen:
Anforderungen und Performance, Data Center Networking, Netzvirtualisierung, SDN, NFV und
cloud-native Networking, programmierbare Data Planes (P4), moderner Transport (QUIC/TAPS) und
Netze für KI-Cluster. Theorie und Praktikum laufen parallel: containerlab (FRR) und Mininet
ersetzen die frühere GNS3-Umgebung.

## Semesterstand

- `main` ist der aktuelle Stand; der Tag **`wise2026`** markiert den Stand zu Semesterbeginn
  (erste Vorlesungswoche).
- Änderungen im Semester laufen als normale Commits — die Historie ersetzt die frühere Praxis,
  pro Semester einen eigenen Ordner zu führen.

## Inhalt

| Datei(en) | Inhalt |
|---|---|
| `0-AdvCompNet-Gliederung.md` | Organisation, Kapitelübersicht, Leistungsnachweis |
| `1-AdvCompNet-Anforderungen.md` | Anforderungen & Performance, Skalierbarkeit & Design-Prinzipien (7E Kap. 1) |
| `2-AdvCompNet-DataCenterNetworking.md` | Rechenzentren: Aufbau/Evolution, Clos/Leaf-Spine, Fehlertoleranz |
| `3-AdvCompNet-Netzvirtualisierung.md` | VLAN, VXLAN/EVPN, Overlays, VPN/Zero Trust, Microsegmentation |
| `4-AdvCompNet-SDN.md` | SDN-Paradigma, Data/Control Plane, Controller, Google B4/Jupiter, Telemetrie |
| `5-AdvCompNet-NFV.md` | ETSI-NFV, vSwitch/DPDK, Cloud-native Networking (CNI/eBPF), SD-WAN |
| `6-AdvCompNet-P4-ProgrammableDataPlane.md` (+ `…-Detail.md`) | Programmierbare Data Plane: PISA, P4, P4Runtime, „nach Tofino", DPUs |
| `7-AdvCompNet-NetworkApplicationPerformance.md` (+ `…-Detail.md`) | HTTP/3/QUIC, Congestion Control, TAPS, RPC/RDMA |
| `8-AdvCompNet-NetworksForAI.md` | Netze für KI-Cluster: Rail-optimized Clos, AllReduce, RoCE/UEC, DCQCN |
| `Labs/` | Praktikum L0–L6 (containerlab + Mininet), Konventionen und Stolperfallen in `Labs/README.md` |
| `PLAN.md` | Ablauf der Veranstaltung (Terminplan, Lab-Übersicht, Zuordnung) |
| `figures/` | Abbildungen je Kapitel |

Referenzliteratur: Peterson/Davie, *Computer Networks: A Systems Approach*, 7. Auflage
(<https://7e.systemsapproach.org>) und das SDN-Buch (<https://sdn.systemsapproach.org>); je Folie als
Fußzeile referenziert (`*7E §4.5 …*`).

## Erzeugen und Präsentieren

Die Umgebung kommt aus [devenv](https://devenv.sh) (marp-cli, Chromium, Node):

```sh
direnv allow          # einmalig
devenv shell          # Shell mit allen Werkzeugen

# in der Shell:
pdfs                  # alle Decks als PDF rendern
slidev-convert        # Slidev-Fassung aus den Marp-Decks erzeugen
slidev-watch 4-AdvCompNet-SDN.md   # Live-Vorschau im Browser (http://localhost:3030)
slidev 4-AdvCompNet-SDN.md         # Presenter-Modus
slidev-build          # statische Slidev-Fassung nach slidev/dist/ bauen
```

**Marp ist die Quelle**; die Slidev-Fassung wird per `slidev-convert` erzeugt und nicht versioniert.

## PDFs

Die PDFs werden **nicht** im Repository abgelegt, sondern bei jeder Änderung automatisch
gebaut und über GitHub Pages veröffentlicht:

- Übersicht: **https://srieger1.github.io/advanced-computer-networks/**
- einzelne Decks: `https://srieger1.github.io/advanced-computer-networks/4-AdvCompNet-SDN.pdf` (usw.)

Damit lässt sich aus Moodle direkt auf die jeweils aktuelle Fassung verlinken — die Links
bleiben stabil, auch wenn sich die Folien im Semester ändern.

Lokal dasselbe Ergebnis (`public/index.html` + `public/*.pdf`, copyright-Bilder wie in der CI ausgeblendet):

```sh
devenv shell -- pages     # bauen wie die CI
devenv shell -- pdfs      # nur die PDFs neben die Decks legen
```

## Prüfen

```sh
devenv shell -- check        # Folien-Dichte, Marker-Konventionen, Links (Exit ≠ 0 bei Verstoß)
devenv shell -- slidevcheck  # Überlauf in der gerenderten Slidev-Fassung (0 erwartet)
```

Die Regeln dahinter stehen in `tools/slidecheck.mjs` bzw. `tools/linkcheck.mjs`.

## Lizenz

- **Folien und Abbildungen** (`*.md`, `figures/`, `PLAN.md`): [Creative Commons Namensnennung
  4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) — siehe `LICENSE`.
- **Werkzeuge und Skripte** (`tools/`, `devenv.nix`): MIT — siehe `LICENSE-MIT`.

Bei Nachnutzung bitte nennen: *Sebastian Rieger, MMNet, Hochschule Fulda — LVA Advanced Computer Networks*.

## Hinweise

- Eigene Grafiken und Fotos werden durch Abbildungen aus der 7. Auflage von *Computer Networks:
  A Systems Approach* ergänzt (CC BY 4.0, mit Quellenangabe auf der Folie).
- Material, das nicht weiterverbreitet werden darf (Screenshots fremder Präsentationen, Hersteller-Marketing),
  ist bewusst **nicht Teil des Repos**.
- Externe Inhalte sind verlinkt, nicht übernommen; kurze Zitate sind mit Quelle gekennzeichnet.
- Nicht Teil des Repos: Altmaterial früherer Semester (u. a. die GNS3-Labs in `Labs/!old/`),
  Arbeitsdokumente und Prüfungs- bzw. Teilnehmendendaten (siehe `.gitignore`).
