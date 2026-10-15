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

## Kapitel 7 · Network Application Performance — Detailfolien

Wintersemester 2026/2027
Master AI – Hochschule Fulda
Sebastian Rieger · MMNet

---

## Detailfolien zu Kapitel 7

Ergänzendes Material — nicht Teil der Vorlesung, aber klausurrelevant als Hintergrund:

- **Advanced Layer 3?** — offene Punkte (Skalierung, Mobility, BGP-Weiterentwicklung)
- **Dateidienste:** SMB 3 und NFS — Entwicklung der Layer-7-Protokolle
- **Flusskontrolle bei TCP:** Buffer Bloat, TCP Splitting, Multipath, Coded TCP
- **Hardware:** AMD Pensando „Elba" DPU-Architektur
- **Trends** im Advancement von Computer Networks

---

## Advanced Network Layer?

- Advanced Layer 7 (inkl. 5, 6) und Layer 4 in diesem Kapitel diskutiert
- Advanced Layer 2 in den vorherigen Kapiteln
- **Advanced Layer 3?**
  - Scalability (IPv6), seit >20 Jahren jetzt wirklich/endlich/überall … ;)
  - Mobility von IP-Adressen? vgl. Naming/Binding (Saltzer) – wie ist das umsetzbar? Tunnel z.B. mit LISP?
  - Weiterentwicklung von BGP? Ablösung von BGP?
  - Ausfallsicherheit Standard-Gateway/Internetzugriff (VRRP, SD-WAN, …) – ist das nicht eigentlich ein Problem im Betriebssystem? ;)
- **Trends?** Welche zusätzlichen Anforderungen kommen in der Zukunft?
  - Internet of Things (IoT)?
  - In-band Telemetry/Network Management? Machine Learning?
  - Microservices/Container? Overlay-Netze/Service Mesh mit VXLAN etc.
  - Mobile Edge Computing (MEC)?

---

## Advanced Layer 7 Protokoll: SMB 3

Server Message Block (SMB) – Windows File Share

| Version | Wesentliche Neuerungen |
|---|---|
| SMB 2.1 (2009) | Bessere Unterstützung von „large BDP": Performance auf 10 GbE, große MTU, verbessertes Operation-Locking-Modell, Branch Cache, Credits für mehrere 64k-Segmente |
| SMB3 (früher 2.2), Windows 8/2012, Samba ≥4.0 | Clusters (active/active), Distributed Caching, Multipath (Trennung von Session und Connections, Aggregation), RDMA, Encryption, … |
| SMB 3.1.1, Windows Server 2016 | Verbesserte Negotiation/Encryption, Cluster Fencing/Failover |

*Quelle: Windows 8 SMB 2.2 File Sharing Performance, MSDN, 9/2011*

---

## Advanced Layer 7 Protokoll: NFS

Entwicklungen beim Network File System (NFS)

| Version | Wesentliche Neuerungen |
|---|---|
| NFS v4.1 (RFC 5661, 1/2010) | Unterstützung von Cluster-Server-Deployments, Caching, skalierbarer paralleler Zugriff auf über mehrere Server verteilte Dateien (**pNFS**) |
| NFS v4.2 (RFC 7862, 11/2016) | Local-File-System-Unterstützung, Local-Copy, Server-Side-Copy, Sparse-File-Support/Space Reservation, Federated Access (Namespace-Traversal über Fileserver verschiedener Organisationen) |

[datatracker.ietf.org/wg/nfsv4/documents](https://datatracker.ietf.org/wg/nfsv4/documents/)

**Fazit aus der Weiterentwicklung von SMB/NFS für Advanced Layer 7?**

---

## Trends im Advancement von Computer Networks

- Sieht man z.B. auf „den großen Konferenzen": SIGCOMM, INFOCOM … „NANOG"
- Google-Scholar-Kennzahlen zu Computer Networks – warum veröffentlichen, warum Paper schreiben?
- Oder bei den Herstellern und Analysten ;-)
- Erinnern Sie sich? „Great Engineering" vs. „Good Science" ;-)

---

## Weitere Beispiele

- … Sie sind herzlich eingeladen, zu einem Paper beizutragen ;-) Es wäre nicht das erste Mal, dass Studierende beteiligt waren ;-)
- Siehe auch: [Google Scholar](https://scholar.google.com)
- … das gilt auch für Forschungsprojekte, aktuelle Themen z.B.:
  - Network Digital Twins (NDT)
  - Intent-based Routing
- Allgemein:
  - Einsatz von SDN/NFV/P4 für Traffic Engineering, Network Attack Detection
  - Netzwerk-Management/Monitoring/Telemetry & Machine Learning

---

## Flusskontrolle bei TCP

<div class="columns">
<div>

**Problembereiche**
- Hohe Bitrate bei gleichzeitig hoher Latenz → viele RTTs
- (Zu große) Puffer (Router, Endgeräte etc.) führen zusätzlich zu hoher Latenz, behindern effektive Congestion Control (vgl. „Buffer Bloat")
- Im Wireless-Bereich (WLAN, UMTS/LTE …) mehr Timeouts durch Paketverluste (Bitfehler)

</div>
<div>

**Aktuelle Entwicklungen**
- Verbesserte Congestion Control: **BBR** (Bottleneck Bandwidth and Round-Trip propagation time)
- **TCP Splitting** (Cloud)
- **Multipath TCP** (parallele Streams über mehrere/verschiedene Links)
- **Coded TCP** (Wiederherstellung defekter empfangener Segmente)

</div>
</div>

---

## Cloud-Anforderungen: TCP Splitting

- Einfache Variante, um den Durchsatz von TCP zu verbessern: mehrere TCP-Verbindungen parallel
- **Kaskadiert (hintereinander): TCP Splitting**
  - Persistente TCP-Verbindung im Backend, bleibt lange offen, daher kein Slow-Start – ist auf RTT und Bandbreite „getuned"
  - Beispiel: Verbindung zu regionalem Server eines Cloud-Anbieters (Frontend), dieser unterhält eine Verbindung zum Cloud-Rechenzentrum (Backend)
- **Parallel (nebeneinander):** mehrere TCP-Sitzungen oder z.B. Multipath TCP

![w:1100px](figures/6-netapp-performance/fig-41.png)

---

## AMD Pensando „Elba" DPU – Architektur

Interne Blockarchitektur des Pensando-DPU-ASICs „Elba": P4-programmierbare Egress-/Ingress-Pipelines, Traffic-Manager/Packet-Buffer, Arm-Kerne mit Coherent NOC, Offload-Engines (Crypto, Kompression, CRC) sowie DDR4/5-Speicheranbindung – Basis u.a. der AMD-Pensando-SmartNIC-Familie.

![h:460px](figures/6-netapp-performance/copyright/fig-42.jpeg)

*Quelle: ServeTheHome / Pensando*
