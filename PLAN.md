# Advanced Computer Networks (ACN) — Planung WiSe 2026/27

Foliensatz und Ablaufplan der Lehrveranstaltung *Advanced Computer Networks* (Master AI,
Hochschule Fulda, Prof. Sebastian Rieger, MMNet). Arbeitsgrundlage der Überarbeitung: `PLANNED-CHANGES.md`
(vorerst nicht im Repo), Lab-Konventionen: `Labs/README.md`, Repository- und Build-Anweisungen: `AGENTS.md`.

## Ausrichtung

- **8 Kapitel** (K1–K8) auf **14 Vorlesungseinheiten à 90 Min** (L1–L14) abgebildet, plus L15
  (Wiederholung/Klausur). **L16 (Paper-Diskussion) entfällt in WiSe 26/27** — der verspätete
  Semesterstart und die Konferenzwoche lassen keinen Platz für eine 16. Einheit (s. Ablaufplan).
  Zielbudget 30 ± 5 Folien pro Einheit.
- Zielbild: **~240 Vorlesungsfolien** (vorher 264 in 6 Kapiteln); Code-/Backup-Folien wandern in
  Detaildecks (`…-Detail.md`), die nicht mitgedruckt werden.
- **Referenzliteratur:** Peterson/Davie, *Computer Networks: A Systems Approach*, 7. Auflage (CC BY 4.0,
  <https://7e.systemsapproach.org>) plus SDN-Buch (<https://sdn.systemsapproach.org>, CC BY-NC-ND 4.0 —
  nur verlinken/zitieren). Quellenangabe je Folie als Fußzeile (`*7E §4.5 …*`).
- **Didaktische Marker** wie im KP-Deck: 💡 (Hands-on/Demo/Praxis, immer mit Link), 🧠 (Food for thought),
  Abschlussfolien je Kapitel (Lernzielkontrolle ✍️🧠, Praktische Übungen 🛠️🧑‍🔬, Weiterführende Literatur 💡).
- **Praktikum:** containerlab (FRR-first) + Mininet statt GNS3; Labs L0–L6, siehe unten.

## Struktur des Foliensatzes

| Deck | Kapitel | Inhalt |
|---|---|---|
| `0-AdvCompNet-Gliederung.md` | — | Organisation, Kapitelübersicht, Leistungsnachweis |
| `1-AdvCompNet-Anforderungen.md` | K1 | Anforderungen & Performance, Skalierbarkeit & Design-Prinzipien (L1/L2) |
| `2-AdvCompNet-DataCenterNetworking.md` | K2 | Rechenzentren: Aufbau/Evolution, Clos/Leaf-Spine, Fehlertoleranz (L3/L4) |
| `3-AdvCompNet-Netzvirtualisierung.md` | K3 | VLAN, VXLAN/EVPN, Overlays, VPN/Zero Trust, Microsegmentation (L5) |
| `4-AdvCompNet-SDN.md` | K4 | SDN-Paradigma, Data/Control Plane, ONOS, Google B4/Jupiter, Telemetrie (L6/L7) |
| `5-AdvCompNet-NFV.md` | K5 | ETSI-NFV, vSwitch/DPDK, Cloud-native (CNI/eBPF), SD-WAN, Service Mesh (L8) |
| `6-AdvCompNet-P4-ProgrammableDataPlane.md` | K6 | PISA, Match-Action, P4Runtime, „nach Tofino", DPUs (L9/L10) |
| `7-AdvCompNet-NetworkApplicationPerformance.md` | K7 | HTTP/3/QUIC, Congestion Control (CUBIC/BBR), TAPS, RPC/RDMA (L11/L12) |
| `8-AdvCompNet-NetworksForAI.md` | K8 | Rail-optimized Clos, AllReduce, IB/RoCE/UEC, DCQCN, AI for Networking (L13/L14) |
| `…-Detail.md` (K6, K7) | — | Backup-/Code-Folien (Selbststudium, nicht im Vorlesungs-PDF) |

Alle Decks sind eigenständige Marp-Markdown-Dateien; die Slidev-Fassung (Präsentation) wird per
`devenv shell -- slidev-convert` erzeugt. Copyright-kritische Bilder liegen lokal in
`figures/<kapitel>/copyright/` (nicht im Repo, nicht in den veröffentlichten PDFs — siehe `AGENTS.md`).

## Ablaufplan (Montage, WiSe 2026/27)

Wöchentlicher Termin: **Montag, 9:50–11:20 (Vorlesung) und 11:40–13:10 (Praktikum)**.

- **Mo 19.10.2026** = erste Lehrveranstaltung (der Semesterstart am Fr 16.10. entfiel wegen der
  Erstsemestereinführung — 19.10. ist der reguläre erste Termin).
- **Konferenzreise ab Fr 23.10.** → der Termin in der zweiten Woche wird durch **Flipped Classroom
  zu den L2-Inhalten** ersetzt (Auftrag + Material, Auswertung am Folgetermin).
- **Weihnachtspause 21.12.2026–10.1.2027** (21.12., 28.12., 4.1. entfallen).
- **Letzter LV-Termin: Mo 1.2.2027**; **Mo 8.2.2027 entfällt (Rosenmontag)**.
- **L16 (Paper-Diskussion) entfällt.** Damit stehen 13 Termine für L1–L15: L1 allein, L2 als
  Flipped Classroom mit Auswertung vor L3, L11/L12 und L13/L14 als Doppelblöcke.

| # | Datum | KW | Inhalt | Kapitel |
|---|---|---|---|---|
| L1 | Mo 19.10.2026 | 43 | Anforderungen & Performance | K1 |
| FC | Mo 26.10.2026 | 44 | **entfällt** (Konferenzreise) → Flipped Classroom zu L2 (Skalierbarkeit & Design-Prinzipien) | K1 |
| L2+L3 | Mo 02.11.2026 | 45 | Auswertung Flipped Classroom + Data Center: Aufbau & Evolution | K1/K2 |
| L4 | Mo 09.11.2026 | 46 | Data Center: Fabric & Fehlertoleranz | K2 |
| L5 | Mo 16.11.2026 | 47 | Netzvirtualisierung & Overlays | K3 |
| L6 | Mo 23.11.2026 | 48 | SDN: Paradigma & Data Plane | K4 |
| L7 | Mo 30.11.2026 | 49 | SDN: Control Plane & Betrieb | K4 |
| L8 | Mo 07.12.2026 | 50 | NFV & Cloud-native Networking | K5 |
| L9 | Mo 14.12.2026 | 51 | Programmable Data Plane: P4 | K6 |
| — | 21.12.–10.1. | 52–1 | **Weihnachtspause** (21.12., 28.12., 4.1. entfallen) | — |
| L10 | Mo 11.01.2027 | 2 | P4: Runtime, Hardware & Ökonomie | K6 |
| L11+L12 | Mo 18.01.2027 | 3 | Transport im Wandel + Multipath QUIC, TAPS & RPC/RDMA (Doppelblock) | K7 |
| L13+L14 | Mo 25.01.2027 | 4 | Netze für KI: Training + Congestion & Ausblick (Doppelblock) | K8 |
| L15 | Mo 01.02.2027 | 5 | Wiederholung & Klausurvorbereitung — **letzter LV-Termin** | — |
| — | Mo 08.02.2027 | 6 | entfällt (Rosenmontag) | — |

Im Praktikumsblock (11:40–13:10) laufen die Labs L0–L6 parallel zu den Kapiteln (Zuordnung siehe unten);
Ausfälle (Konferenz, Feiertage) werden im Lab-Track durch Selbststudium des Lab-Sheets aufgefangen.

## Praktikum: Labs L0–L6 (containerlab + Mininet)

Zielstack (Entscheidungen 2026-09-24/10-04): **FRR, wo es geht** (`frrouting/frr`, BYOD ohne Account),
**Nokia SR Linux** nur wo FRR fehlt (gNMI/Telemetrie), **Mininet** für SDN/OpenFlow und P4,
**GNS3 wird abgelöst**. Link-Impairments über `containerlab tools netem`. Detailrezepte und Stolperfallen:
`Labs/README.md`, `PLANNED-CHANGES.md` §4/§9.

| Lab | Ordner | Thema / Stack | Zuordnung | Status |
|---|---|---|---|---|
| L0 | `Labs/L0_setup_tools/` | Setup & Werkzeuge: Topologie starten, `ping`/`traceroute`/`tcpdump`/`iperf3`, Störungen via `netem` | zu L1 (Einstieg) | ✅ gebaut & verifiziert |
| L1 | `Labs/L1_dcn_l2_lag/` | DCN Layer 2: STP-Ring vs. LACP-Bond (containerlab, Bridges/Bonds, FRR) | zu L3/L4 (K2) | ✅ gebaut & verifiziert (STP ~30 s Ausfall vs. LACP 0 % Verlust) |
| L2 | `Labs/L2_dcn_bgp_fabric/` | DCN Layer 3: Leaf-Spine-BGP-Fabric, ECMP, Fehlertoleranz/BFD, Konvergenzmessung (FRR `bgpd`) | zu L4 (K2) | ✅ gebaut & verifiziert (6/6 BGP, 12/12 Pings, BFD-Failover) |
| L3 | `Labs/L3_sdn_mininet/` | SDN mit Mininet/OpenFlow: eigenes Image `acn-l3-mininet` (Mininet 2.3.0 + OVS 3.3.9 + os-ken 4.2.2), Controller-Verhalten messbar | zu L6/L7 (K4) | ✅ gebaut & verifiziert (pingall 0 %, ohne Controller 100 %, mit os-ken 0 %) |
| L4 | `Labs/L4_p4_intro/` | Programmable Data Plane: p4lang-Images (`p4c` 1.2.5.18 + `bmv2` 1.15.7) in containerlab, P4-Code vorbereitet (Aufgaben von `5_p4_intro` übernommen) | zu L9/L10 (K6) | ✅ gebaut & verifiziert (Tabellenbefüllung 0 %, P4Runtime vorbereitet) |
| L5 | `Labs/L5_multipath_quic_taps/` | **Neu:** Multipath QUIC & TAPS — Client mit 2 Pfaden (10 ms vs. 80 ms + 2 % Loss, `netem`), Single-Path vs. Aggregation vs. Failover, Scheduling-Vergleich, Reordering/Head-of-Line, TAPS-Anwendung (RFC 9621–9623); Stack: **picoquic** (Fallback ngtcp2), qlog/`tshark` als Beobachtungsweg | zu L11/L12 (K7) | ⏳ neu zu bauen (P6) |
| L6 | `Labs/L6_networking_for_ai/` | **Neu:** Networking for AI — Leaf-Spine + Incast (`iperf3 -P`), Tail-Latency/Straggler, ECN/AQM (`ss -ti`), ECMP vs. Packet Spraying, Ring-AllReduce-Simulation (Python), IB/RoCE/UEC-Diskussion | zu L13/L14 (K8) | ⏳ neu zu bauen (P6) |

Übungsblätter/Fragen: `Exercises/ub1..ub3` und `Questions/q1..q9` referenzieren noch die alten
Kapitelnummern (K1–K6) und GNS3-Lab-Namen; sie werden auf K1–K8 und L0–L6 umgestellt und um Fragen
zu Multipath QUIC/TAPS und Networking for AI ergänzt (je 6–10 im bestehenden Stil).

## Veröffentlichung & Lizenz

- **Public GitHub Repo:** <https://github.com/srieger1/advanced-computer-networks> (Muster:
  [srieger1/cloud-services](https://github.com/srieger1/cloud-services)) mit den Decks und `Labs/`.
  Build/Veröffentlichung siehe `AGENTS.md`.
- **CI (GitHub Pages):** bei Push auf `main` werden alle Decks als PDF gerendert — **ohne**
  copyright-kritische Bilder (Zeilen auf `figures/*/copyright/` werden vor dem Rendern gestrichen).
  Copyright-Material erscheint nur in der lokalen Präsentation (Marp/Slidev). Übersichtsseite über
  `tools/site.mjs`; lokal dasselbe: `devenv shell -- pages`.
- **Lizenzen wie bei cloud-services:** Inhalte **CC BY 4.0** (`LICENSE`), Werkzeuge **MIT** (`LICENSE-MIT`).
  Copyright-kritisches Material ist per `copyright/`-Konvention ausgeschlossen; 7E-Abbildungen laufen
  unter CC BY 4.0 mit Attributionszeile.

## Offene Punkte

- Labs L5 und L6 bauen (P6) — Stack picoquic bzw. Incast/ECN-Setup.
- `Exercises/`/`Questions/` auf K1–K8 und L0–L6 mappen (P7), neue Fragen für K7-Neu/K8.
- Entscheidung über die **13 unreferenzierten OK-Bilder** (Liste in `PLANNED-CHANGES.md`):
  löschen (Clean Cutover) oder archivieren — copyright-kritische sind bereits in `copyright/`.
