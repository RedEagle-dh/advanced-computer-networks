---
marp: true
theme: default
paginate: true
html: true
inlineSVG: true
header: "Advanced Computer Networks | HS Fulda – Master AI"
footer: "Sebastian Rieger · MMNet · Hochschule Fulda"
style: |
  :root {
    --color-primary: #003366;
    --color-accent:  #0066cc;
    --color-light:   #e8f0f8;
  }
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 22px;
    color: #1a1a1a;
    background: #ffffff;
  }
  h1 {
    color: var(--color-primary);
    font-size: 1.8em;
    border-bottom: 3px solid var(--color-accent);
    padding-bottom: 0.2em;
  }
  h2 {
    color: var(--color-accent);
    font-size: 1.3em;
  }
  section.title {
    background: var(--color-primary);
    color: #ffffff;
    text-align: center;
    justify-content: center;
  }
  section.title h1 {
    color: #ffffff;
    border-bottom: 3px solid #ffffff;
    font-size: 2em;
  }
  section.title p, section.title h2 {
    color: #cce0ff;
  }
  section.section-break {
    background: var(--color-accent);
    color: #ffffff;
    justify-content: center;
    text-align: center;
  }
  section.section-break h1 {
    color: #ffffff;
    border-color: #ffffff;
    font-size: 2.2em;
  }
  section.section-break p {
    color: #cce0ff;
    font-size: 1.1em;
  }
  ul { margin: 0.4em 0; padding-left: 1.4em; }
  li { margin: 0.3em 0; }
  table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
  th { background: var(--color-primary); color: white; padding: 6px 10px; }
  td { padding: 5px 10px; border-bottom: 1px solid #ddd; }
  tr:nth-child(even) td { background: var(--color-light); }
  code { background: var(--color-light); padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }
  blockquote {
    border-left: 4px solid var(--color-accent);
    background: var(--color-light);
    padding: 0.5em 1em;
    margin: 0.5em 0;
    border-radius: 0 4px 4px 0;
  }
  .columns { display: grid; grid-template-columns: 1fr 1fr; gap: 1em; }
  .columns3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.8em; }
  .columns4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.6em; align-items: start; }
  .cols-tree { display: grid; grid-template-columns: 1.2fr 1.1fr 1fr; gap: 1em; align-items: start; }
  .columns-15 { display: grid; grid-template-columns: 1.5fr 1fr; gap: 1em; align-items: start; }
  .card {
    background: var(--color-light);
    border-left: 4px solid var(--color-accent);
    border-radius: 0 6px 6px 0;
    padding: 0.6em 0.8em;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
  img[alt~="float-right"] {
    float: right;
    margin: 0 0 0.6em 1em;
  }
  /* Marker-Kasten: Hands-on / Praxisbeispiel / Demo (PLANNED-CHANGES 2.2) */
  .hands-on {
    border-left: 4px solid #b8860b;
    background: #fff8e1;
    border-radius: 0 6px 6px 0;
    padding: 0.5em 0.8em;
    margin: 0.6em 0;
  }
  /* Marker-Kasten: Food for thought / Hintergrund / kritische Frage */
  .food-for-thought {
    border-left: 4px solid #00695c;
    background: #e0f2f1;
    border-radius: 0 6px 6px 0;
    padding: 0.5em 0.8em;
    margin: 0.6em 0;
  }
  /* Kernaussage einer Folie */
  .takeaway {
    border-left: 4px solid var(--color-primary);
    background: var(--color-light);
    font-weight: 600;
    padding: 0.5em 0.8em;
    border-radius: 0 6px 6px 0;
  }
---

<!-- _class: title -->

# Advanced Computer Networks

## Kapitel 0 · Organisatorisches

Wintersemester 2026/2027
Master AI – Hochschule Fulda
Sebastian Rieger · MMNet

---

## Dozent

<div class="columns">
<div>

**Sebastian Rieger**
Professur „Multimediale Kommunikationsnetze" (MMNet)

sebastian.rieger@informatik.hs-fulda.de
Raum 46.126 · -3116
Sprechstunde: Do 11:40–13:10 Uhr *(Anmeldung erwünscht, weitere Termine n. Absprache)*
Online-Sprechstunde: → Link in Moodle

**Forschung (MMNet):**
Network Digital Twins · Future Internet Architectures · AI/ML in Networking
→ [mmnet.informatik.hs-fulda.de](https://mmnet.informatik.hs-fulda.de)

</div>
<div>

**Werdegang:**

- Studium Angewandte Informatik, HS Fulda (1998–2003)
- Wiss. Mitarbeiter/Assistent, GWDG Göttingen (2003–2010)
- Promotion, Universität Göttingen (2007)
- Projekt-/Abteilungsleiter, SCC / KIT Karlsruhe (2010–2012)
- Lehraufträge: HS Fulda, HAWK Göttingen, HS Karlsruhe, Uni Göttingen, KIT (2004–2012)
- **Seit 2012: Professur HS Fulda**

> Themen aus meiner Forschung fließen in die LVA ein – Abschlussarbeiten/Projekte in diesem Bereich sind willkommen!

</div>
</div>

---

## Inhalte der Lehrveranstaltung

1. **Anforderungen** – Aufbau von Netzinfrastrukturen, aktuelle Herausforderungen
2. **Data Center Networking** – Lastverteilung, Skalierung, Fehlertoleranz (Layer 2/3, Fabrics)
3. **Netzvirtualisierung & Overlays** – VLAN, VXLAN/EVPN, VPN, Microsegmentation
4. **Software-defined Networking (SDN)** – Control/Data Plane, Controller, Betrieb & Telemetrie
5. **Network Function Virtualization (NFV)** – VNF, virtuelle Switches, Cloud-native Networking
6. **P4 / Programmable Data Plane** – PISA, P4, P4Runtime, programmierbare Hardware & DPUs
7. **Network Application Performance** – Load Balancer, QUIC/HTTP3, Congestion Control, Multipath/TAPS, RDMA
8. **Netze für KI** – Trainings-/Inferenz-Workloads, Collectives, UET/InfiniBand, AI for Networking

<br/>

**Optional/Ausblick:** fortgeschrittene Access-Netze (Mobilfunk/Wireless/IoT, Optical Networks), Weitverkehrsnetze (Carrier Ethernet, DCI), Traffic Engineering, Information-centric Networking, Future Internet, Energieeffizienz

---

## Struktur der Lehrveranstaltung

<div class="columns">
<div>

**Vorlesung (2 SWS · seminaristischer Unterricht)**

- Vorstellung/Diskussion aktueller Anforderungen im Bereich Computer Networks
- Fokus: **Network Edge** (Client- sowie Server-/Data-Center-Seite)
- Vorträge/Diskussion zu Stand von Wissenschaft & Technik anhand wissenschaftlicher Paper

**Praktikum (2 SWS)**

- Exemplarische Praxisbeispiele zu aktuellen Herausforderungen/Lösungen
- Übung von Klausuraufgaben

</div>
<div>

**Modul:** AI5022MP · Master AI
**Umfang:** 4 SWS (2 SU + 2 Praktikum)

**Voraussetzungen:**
notwendig: keine
empfohlen: Computernetzwerke, Betriebssysteme, Verteilte Systeme

**Prüfungsform:** Klausur (60 Min.) oder semesterbegleitende Leistung

> Ausgangspunkt: Kenntnisse Rechnernetze aus dem Bachelor (z. B. „Kommunikationsnetze<br/>und -protokolle")

</div>
</div>

---

## Praktikum – Übersicht

**Übung 1 · Setup, Routing & Switching, Data Center Networking**

- Lab L0: Werkzeuge & Setup (containerlab, Mininet, Wireshark/`iperf3`) — **löst die GNS3-Einführung ab**
- Lab L1: Layer 2 im Rechenzentrum — Link Aggregation/Bonding, Spanning-Tree-Vergleich
- Lab L2: Leaf-Spine-Fabric mit BGP (**FRR**) + Fehlertoleranz (Linkausfall, Konvergenzzeit)
- Übungsaufgaben: Internet Design Principles, Anforderungen an Computer Networks

<div style="display: grid; grid-template-columns: 1.5fr 0.5fr; gap: 1em;">
<div>

**Übung 2 · Netzvirtualisierung, SDN & NFV**

- Lab L3: SDN mit **Mininet** und OpenFlow, eigene Topologien
- Lab L4: Programmable Data Plane mit **P4** (bmv2, P4Runtime)
- Übungsaufgaben: VLAN/Overlay-Konzepte, Controller-Aufbau

**Übung 3 · Transport, Multipath & Netze für KI**

- Lab L5: **Multipath QUIC & TAPS** (Scheduling, Failover, Aggregation)
- Lab L6: **Net for AI** (Incast, Tail-Latency, ECN≠PFC, ECMP≠Packet Spraying)
- Network Application Performance: Transport-/Anwendungsprotokolle

</div>
<div>

> Eigenständige Bearbeitung, ggf. im Team · virtuelle Netzlabor-Umgebung (containerlab/Mininet, **BYOD-fähig** — keine registrierungspflichtigen Vendor-Images) · optional via Hochschul-VPN im NetLab

</div>
</div>

---

## Leistungsnachweis

<div class="columns3">
<div class="card">

**📝 Klausur**
60 Minuten
am Ende des Semesters

Alternativ: Portfolio

</div>
<div class="card">

**🔬 Praktikum**
Aufgaben aus den
3 Übungsblöcken

Vertiefen die Lehrinhalte, fließen in die Prüfungsinhalte ein

</div>
<div class="card">

**📋 Vorbereitung**
Klausurübung mit Demo-Klausur
am Ende der LVA

„Katalog mit Wiederholungsfragen"

</div>
</div>

<br/>

**Modulkennnummer:** AI5022MP · Master AI  
**Voraussetzungen:** keine formalen (empfohlen: Computernetzwerke, Betriebssysteme, Verteilte Systeme)

---

## Lernergebnisse (Qualifikationsziele)

**Kenntnisse:**
Anforderungen fehlertoleranter, leistungsfähiger und skalierbarer IT-Services an Computernetzwerken; Lösungen für Performance, Fehlertoleranz und Skalierbarkeit in Netzen von Unternehmen, Rechenzentren und Service Providern

**Fähigkeiten:**

- Aktuellen Forschungsstand bewerten, Anforderungen analysieren und geeignete Konzepte für die Netzplanung einsetzen
- Konzepte für die Leistungsfähigkeit aktueller Netze bei eigenen Diensten/Anwendungen einsetzen und bewerten
- Netz-Virtualisierung und Werkzeuge für Netz-Automatisierung/-Programmierbarkeit einsetzen
- Fortgeschrittene Werkzeuge für Performance-Analyse, -Simulation und -Emulation nutzen

**Kompetenzen:**
Aktive Mitwirkung an der angewandten Forschung im Bereich Computernetzwerke

---

## Literatur

**Primär:**

- Peterson, Davie: *Computer Networks: A Systems Approach*, 7. Auflage (online, 2026) — [7e.systemsapproach.org](https://7e.systemsapproach.org/) *(CC BY 4.0)*
- Peterson, Cascone, O'Connor, Vachuska, Davie: *Software-Defined Networks: A Systems Approach* (online) — [sdn.systemsapproach.org](https://sdn.systemsapproach.org/)
- Ergänzend (auch deutsch): Kurose, Ross: *Computernetzwerke*, Addison-Wesley ([Überblick](https://gaia.cs.umass.edu/kurose_ross/ppt.php))

**Standards & Primärquellen:** RFCs (QUIC, TAPS, HTTP/3, VXLAN), Ultra-Ethernet-Spezifikation, ETSI NFV, Intel-PCN zum Tofino-EOL — jeweils direkt an der Folie verlinkt

**Weiterführende Themen:**

- [packetpushers.net](https://packetpushers.net/) · [ipspace.net](https://www.ipspace.net/Main_Page) · [rule11.tech/hedge](https://rule11.tech/hedge/) · [requestforcomments.de](https://requestforcomments.de/)
- Talks zu Netzwerkgrundlagen bei CCC, FrOSCon usw.
- Wissenschaftliche Paper der LVA über [scholar.google.com](http://scholar.google.com) (aus dem HS-Netz/VPN)

**Verwandte Graduate-Kurse** *(Dank für Inhalte/Anregungen)*:
CS244 (Stanford) · Advanced Computer Networks (ETHZ) · Advanced Topics in Communication Networks (ETHZ)

---

<!-- _class: section-break -->

# Und wo kann ich das alles brauchen?

---

## Diskussion

- Welche Computer Networks nutzen Sie?
- Welche Herausforderungen stellen sich für diese?
- Wo sehen Sie aktuell oder zukünftig Probleme?
- Wie würden Sie diese in „Advanced Computer Networks" adressieren?
