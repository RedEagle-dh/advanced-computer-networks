# Praktikum Advanced Computer Networks — Laborübungen

Dieser Ordner enthält die **neue, containerbasierte Lab-Reihe (L0–L6)** sowie die historischen
GNS3-/Mininet-Labs in ihren jeweiligen Unterordnern.

## Neue Lab-Reihe (Zielbild WiSe 2026/27)

| Lab | Ordner | Thema | Stack | Status |
|---|---|---|---|---|
| L0 | `L0_setup_tools/` | Setup, Werkzeuge, Netz-Diagnose | containerlab, Alpine, FRR | ✅ gebaut & verifiziert |
| L1 | `L1_dcn_l2_lag/` | Layer 2 im RZ: STP vs. Link Aggregation (LACP) | containerlab, Linux-Bridges/Bonds, FRR | ✅ gebaut & verifiziert (STP 30 s Ausfall vs. LACP 0 %) |
| L2 | `L2_dcn_bgp_fabric/` | Leaf-Spine-Fabric mit BGP + Fehlertoleranz/BFD | containerlab, FRR | ✅ gebaut & verifiziert (Konvergenz ~60 s, ECMP, BFD-Failover) |
| L3 | `L3_sdn_mininet/` | SDN mit Mininet/OpenFlow, eigene Topologien | Mininet, Controller (`os-ken`/ONOS) | ⏳ Portierung von `4_mininet_intro*` |
| L4 | `L4_p4_programmable_data_plane/` | Programmable Data Plane mit P4 | Mininet/bmv2, `prona/p4-container` (Image aktualisieren!) | ⏳ Portierung von `5_p4_intro` |
| L5 | `L5_multipath_quic_taps/` | Multipath QUIC & Transport Services (TAPS) | containerlab (2 Pfade, `netem`), QUIC-Stack nach Didaktik-Kriterium, PyTAPS | ⏳ neu zu bauen |
| L6 | `L6_networking_for_ai/` | Incast, Tail-Latency, ECN/PFC, ECMP vs. Packet Spraying | containerlab, FRR, `iperf3` | ⏳ neu zu bauen |

**Grundsatzentscheidungen (S. Rieger, 2026-09-24):**

- **FRR zuerst** (leichtgewichtig, kein Account, BYOD-fähig). **SR Linux** nur, wo FRR Funktionen fehlen
  (z. B. gNMI/Streaming-Telemetrie). **cEOS entfällt** — Registrierung und Image-Import erschweren BYOD.
- **Mininet bleibt** für SDN und P4 (schneller, leichtgewichtiger), containerlab für Routing/Switching
  und Data Center Networking.
- **GNS3 wird abgelöst.** Später zu prüfen: `netlab` (Ivan Pepelnjak) und `nixnet`.

## Konventionen für die neuen Labs

Jedes Lab ist so aufgebaut, dass es **ohne Vorwissen reproduzierbar** ist:

```
Lx_<thema>/
├── <lab>.clab.yml      # Topologie (name: acn-lx-…)
├── configs/            # frr.conf je Knoten, daemons
└── labsheet.md         # Lernziele · Aufgaben · erwartete Ergebnisse · Troubleshooting
```

- **Adressierung gehört ins Topology-File (`exec`), nicht in die `frr.conf`.** Grund: Zebra liest die
  `frr.conf`, *bevor* containerlab die Links anlegt — enthält sie `ip address`-Zeilen, werden diese
  nicht angewendet. FRR konfiguriert nur Routing-Protokolle (BGP/OSPF) und Peering-Eigenschaften.
- **Start/Abbau** immer über `containerlab deploy/destroy -t <datei> --cleanup`.
- **Link-Manipulation** über `containerlab tools netem set …` (kein `pumba` mehr nötig).
- **Auf keinen Fall `frrinit.sh restart`** in einem Lab-Knoten: es beendet PID 1, Docker startet den
  Container neu und alle veth-Interfaces gehen verloren. Einzelne Daemons neu starten ist erlaubt
  (`pkill bgpd` → watchfrr respawnt), genau das machen die Topologien nach dem Setzen der Adressen,
  um FRRs „Waiting for NHT" beim Kaltstart zu vermeiden.
- **Konvergenz abwarten:** nach dem Deploy ~60 s, bevor BGP/BFD-Messwerte interpretiert werden.
- Jedes Labsheet endet mit einer **Verifikationstabelle** (erwartete Ergebnisse) und **Bezug zur Vorlesung**.

## Mac mit Apple Silicon (M1 und neuer)

containerlab braucht einen Linux-Kernel. Auf dem Mac läuft es in einer **arm64-Linux-VM**; die
containerlab-Doku empfiehlt dafür [OrbStack](https://orbstack.dev) (<https://containerlab.dev/macos/>):

```sh
brew install orbstack
orb create -a arm64 ubuntu:noble clab
orb -m clab bash -c 'curl -sL https://containerlab.dev/setup | SETUP_SSHD=false sudo -E bash -s all'
orb -m clab          # Shell in der VM; das Mac-Home ist dort unter /Users/<name> eingebunden
```

**Natives FRR-Image:** `frrouting/frr:latest` auf Docker Hub gibt es nur für **amd64** (FRR 8.4,
zuletzt aktualisiert 11/2022) — auf dem Mac läuft es emuliert über Rosetta. Das funktioniert, nativ
ist aber das offizielle Multi-Arch-Image von quay.io. Damit die Topologie-Dateien unverändert bleiben
(kein Konflikt beim `git pull`), wird es in der VM lokal unter dem erwarteten Namen getaggt:

```sh
docker pull quay.io/frrouting/frr:10.7.1
docker tag  quay.io/frrouting/frr:10.7.1 frrouting/frr:latest
```

containerlab zieht vorhandene Images nicht neu — alle Labs nutzen danach das native Image
(Kontrolle: `docker image inspect -f '{{.Architecture}}' frrouting/frr:latest` → `arm64`). Zurück
zum Docker-Hub-Image: `docker rmi frrouting/frr:latest`, beim nächsten Deploy wird es neu geladen.

Geprüft auf einem M5 mit OrbStack 2.2.4 und containerlab 0.81.1: L0, L1 (beide Szenarien) und L2 erfüllen ihre
Verifikationstabellen mit denselben Ergebnissen wie das emulierte Image, bei etwa halbem RAM je
FRR-Knoten. Sichtbare Unterschiede von FRR 10.7 gegenüber 8.4:

- **L0, Aufgabe 1.3:** `show ip route` listet die beiden Subnetze nur als `C>*`; die zusätzlichen,
  nicht gewählten `O`-Einträge fehlen. OSPF berechnet sie weiterhin (`show ip ospf route` →
  `N … directly attached`).
- Zebra loggt beim Start `failed to retrieve link settings` bzw. `generic-netlink-cmd … Not supported`
  — ohne Auswirkung.

## Historische Labs (Bestand)

| Ordner | Herkunft | Ablösung |
|---|---|---|
| `1_gns3_intro/` | GNS3-GUI, Cisco IOSv | → ersetzt durch **L0** |
| `2_dcn_stp_lag/` | GNS3 + Arista vEOS (STP, LACP, MLAG) | → **L1** (Linux-Bridges/Bonding + FRR) |
| `3_dcn_bgp_fabric/` | GNS3 + Cisco IOSv (BGP-Fabric) | → ersetzt durch **L2** |
| `4_mininet_intro/`, `4_mininet_intro-part2/` | Mininet + OpenFlow (Ryu) | → **L3** (Ryu ist seit 04/2024 ohne Commits) |
| `5_p4_intro/` | P4 via learn-sdn-hub, bmv2 | → **L4** (lokal, `prona/p4-container` aktualisieren) |
| `!old/` | ältere Varianten | Archiv |

## Bezug zum Repo `prona-p4-learning-platform/acn-lab2-dcn-clab`

**Status:** Die FRR-Portierung dieses Repos ist **lokal fertig** (Klon unter `~/Dev/acn-lab2-dcn-clab`,
Commit `9187075`): `frr/` enthält die Fabric-Topologie + Lab-Sheet, die cEOS-Szenarien liegen unter
`!old/`. **Push offen** — dafür werden die Zugangsdaten des Repos benötigt.


Das dort begonnene containerlab-Proof-of-Concept (Stand 08.10.2021, drei MSTP/LACP/MLAG-Szenarien
mit Arista cEOS) ist die Vorlage für **L1/L2**. Es wird auf FRR/Linux portiert; die cEOS-YAMLs wandern
nach `!old/`. Die Lab-Sheets (`fabric.md`, `scenario*.md`) liefern die Diskussionsfragen, die in die
neuen `labsheet.md` einfließen.
