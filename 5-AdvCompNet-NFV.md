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

## Kapitel 5 · Network Function Virtualization (NFV)

Wintersemester 2026/2027
Master AI – Hochschule Fulda
Sebastian Rieger · MMNet

---

## Kapitelübersicht

**5.1 Virtuelle Netze für Data Center und Cloud**
- Mandantentrennung · Overlays (VXLAN) · Anschluss an Kapitel 3

**5.2 Virtuelle Switches**
- Bauformen · Open vSwitch · CPU vs. ASIC · Beschleuniger (SR-IOV, DPDK, eBPF)

**5.3 Network Functions Virtualization (NFV)**
- ETSI-Architektur (NFVI, VNF, MANO, OSS/BSS) · Lebenszyklus · Zusammenspiel mit SDN · SD-WAN

**5.4 Cloud-native Networking (neu)**
- VNF vs. CNF · CNI · eBPF/Cilium · Service Mesh · DPU-Ausblick

*Referenzliteratur: ETSI GS NFV · 7E §9.4, §10 · SDN-Buch §8*

---

## Lernziele

Nach diesem Kapitel sollten Sie wissen…

- warum virtuelle Netze in Data Center und Cloud Overlays wie VXLAN brauchen
- welche Bauformen virtueller Switches es gibt — und was ein Software-vSwitch auf der CPU leistet
- wie man Paketverarbeitung beschleunigt: SR-IOV, DPDK, XDP/eBPF, SmartNIC/DPU
- was NFV ist, woher es kommt und wie die ETSI-Architektur aufgebaut ist
- wie Kubernetes-Netze funktionieren: CNI, eBPF/Cilium, Service Mesh
- wie sich VNFs (VM) von CNFs (Container) unterscheiden

> **Bezug zur Referenzliteratur:** ETSI GS NFV · 7E §9.4 (Virtual Networks for Datacenters) und §10 (Operating Networks) — [7e.systemsapproach.org](https://7e.systemsapproach.org/)

---

<!-- _class: section-break -->

# 5.1 Virtuelle Netze für Data Center und Cloud

Mandantentrennung · Overlays · VXLAN

---

## Multi-tenant Virtual (Cloud) Networks

<div class="columns">
<div>

- Virtuelle Netze sind die Basis jeder Cloud-Virtualisierung
  - Public Cloud: AWS VPC, Azure VNet, Google Cloud VPC
- Ziel: viele Mandanten auf **einer** physischen Infrastruktur — isoliert, flexibel, skalierbar
- Beteiligt sind virtuelle Switches im Host **und** die physische Fabric (vgl. Kapitel 2)
- Technologien: VLAN (Kapitel 3), **VXLAN** und Container-Overlays (Cilium, Kubernetes)

</div>
<div>

![h:250px](figures/4-nfv/fig-03-hypervisor.png)

</div>
</div>

**Fazit:** Ohne Overlay gibt es keine Mandantentrennung über gemeinsam genutzter physischer Infrastruktur.

*7E §9.4 – Virtual Networks for Datacenters*

---

## Virtual Extensible LAN (VXLAN)

<div class="columns-15">
<div>

- Kapselung: **Ethernet → VXLAN → UDP → IP → Ethernet** (UDP-Port 4789)
- VXLAN Network Identifier (VNI): 24 Bit → ~16 Mio. Segmente statt 4096 VLANs
- VTEP: En-/Decapsulation, MAC-Lerntabelle, Flood & Filter bei BUM-Traffic
- Tunnel als Unicast zu bekannten VTEPs oder über eine IP-Multicast-Gruppe
- L2 transparent über L3 → Grundlage für EVPN und Container-Overlays

**Fazit:** VXLAN löst das VLAN-Skalierungsproblem, indem es Layer 2 in Layer 3 verpackt.

</div>
<div>

| MAC | VNI | VTEP |
| --- | --- | --- |
| b1 | 100 | x |
| g1 | 200 | x |
| b2 | 100 | y |
| g2 | 200 | z |

![h:150px](figures/4-nfv/fig-04.png)

</div>
</div>

*RFC 7348 §4–5* · *7E §9.4* · *💡 [RFC 7348](https://www.rfc-editor.org/rfc/rfc7348)*

---

<!-- _class: section-break -->

# 5.2 Virtuelle Switches

Bauformen · Open vSwitch · CPU vs. ASIC · Beschleuniger

---

## Vom physischen NIC zum virtuellen Switch

- Der Hypervisor nutzt die **PNICs** (Physical NICs) des Servers, meist redundant angebunden
- Jede VM bekommt eine **VNIC** (virtuelle Netzwerkkarte)
- Der **vSwitch** verbindet VNICs untereinander und mit der PNIC — Traffic bleibt zunächst im Host
- Anbindung an die physische Fabric per Trunk (VLAN) oder als Overlay (VXLAN) je Mandant
- Der vSwitch ist damit selbst eine virtualisierte Netzfunktion (VNF)

<div class="takeaway">

**Fazit:** Virtualisierung endet nicht an der VM — der erste Netz-Hop liegt im Hypervisor.

</div>

*SDN-Buch §8.3.2 – Virtual Switches* · *EMC AA, „Cloud Infrastructure and Services"*

---

## Virtuelle Switches: Bauformen

- Ein Software-Layer-2-Switch im Host: isoliert VM-Traffic, nutzt die PNIC gemeinsam, zentral im Hypervisor verwaltet

<div class="columns">
<div class="card">

**Im Hypervisor mitgeliefert**

- VMware vSwitch, Microsoft Hyper-V vSwitch, Linux Bridge
- Konfiguration über die Virtualisierungsplattform

</div>
<div class="card">

**Als eigene VM oder Appliance**

- vSwitch in einer VM mit mehreren VNICs
- vgl. FRR, VyOS, Arista vEOS (Übung Data Center Networking; heute FRR-first)
- Open vSwitch in beiden Rollen

</div>
</div>

**Fazit:** Die Bauform entscheidet, wer den vSwitch betreibt: Hypervisor, eigene VM oder Open Source.

*SDN-Buch §8.3.2*

---

## Open vSwitch: der Standard im Linux-Host

- De-facto-Standard für Software-Switching: Kernel-Datapath plus `ovs-vswitchd`
- Volle Layer-2/3-Features: VLAN-Trunking, Bonding, QoS und Flow-Tabellen (OpenFlow)
- Tunneling mit VXLAN, Geneve und GRE — damit Overlay-Rand direkt im Host
- Im Einsatz in OpenStack, Kubernetes (OVN) und Proxmox
- 💡 [openvswitch.org](https://www.openvswitch.org/) – Doku und Kommandos für eigene Experimente
- 💡 [SDN-Buch §8.4](https://sdn.systemsapproach.org/netvirt.html) – OVN als Beispiel

<div class="takeaway">

**Fazit:** Der vSwitch ist die Datenpfad-Instanz im Host — Open vSwitch macht sie programmierbar.

</div>

*Pfaff et al., „The Design and Implementation of Open vSwitch", NSDI 2015*

---

## Was leistet ein Software-vSwitch auf der CPU?

- Software-vSwitch (OVS mit DPDK) auf x86-Servern: Größenordnung **100 Gb/s** pro Server mit vielen Kernen
- Switch-ASIC (Broadcom Tomahawk) liegt um Faktor **100–1000** darüber:
  - Tomahawk 5: 51,2 Tb/s (2022)
  - Tomahawk 6: 102,4 Tb/s (angekündigt 6/2025, Serienfertigung 3/2026)
  - Tomahawk Ultra: 51,2 Tb/s bei ~250 ns Switch-Latenz (7/2025), für AI-Scale-up
- 💡 [Broadcom Tomahawk 6 – Produktankündigung 6/2025](https://www.broadcom.com/company/news/product-releases/63146)

<div class="food-for-thought">

🧠 Reicht Software für Firewall und Load Balancer im Rechenzentrum — oder braucht jede Netzfunktion einen ASIC?

</div>

**Fazit:** Ein Software-vSwitch kostet CPU — Beschleunigung ist deshalb keine Option, sondern Pflicht.

*Quelle: Broadcom-Produktankündigungen 2022–2026*

---

## Paketverarbeitung beschleunigen

<div class="columns">
<div>

**Offload und Passthrough**

- Hypervisor-Offload: virtio-net/vhost-net (KVM), vmxnet3, PCIe-Passthrough
- SR-IOV: virtuelle Funktionen (VF) umgehen den vSwitch — schnell, aber ohne Kontrolle im Datenpfad

**Bypass und Kernel-Datapath**

- 💡 [DPDK](https://www.dpdk.org/): Poll-Mode-Treiber im User Space, Zero-Copy
- 💡 [eBPF/XDP](https://ebpf.io/): Pakete an der NIC verarbeiten, ohne den Kernel zu umgehen

</div>
<div>

**Auf der Karte**

- SmartNIC/DPU mit eigenen Kernen und Beschleunigern → Kapitel 6

![h:200px](figures/4-nfv/copyright/fig-08.png)

**Fazit:** Was der Host nicht leistet, wandert nach unten — in den Kernel, den User Space oder auf die Karte.

</div>
</div>

*Quelle: Google Cloud Blog, „Andromeda 2.1"*

---

<!-- _class: section-break -->

# 5.3 Network Functions Virtualization (NFV)

ETSI-Architektur · MANO · Zusammenspiel mit SDN · SD-WAN

---

## Idee von NFV – und was NFV von SDN unterscheidet

<div class="columns">
<div class="card">

**NFV: Funktion von Hardware lösen**

- Netzfunktionen (Firewall, NAT, Load Balancer, Router, 5G-Core) als Software
- VNFs laufen als VMs auf Standard-Servern (COTS) statt auf Spezialhardware
- Ursprung: Betreiber-Initiative — NFV-White-Paper 10/2012 auf dem SDN & OpenFlow World Congress in Darmstadt; ETSI ISG NFV gegründet 11/2012

</div>
<div class="card">

**SDN: Steuerung von Hardware lösen**

- Trennung von Control und Data Plane (Kapitel 4)
- Ursprung: Forschung, Stanford ~2008
- **Unterschied:** NFV virtualisiert Funktionen (L4–7), SDN Steuerung und Weiterleitung (L2–3)

</div>
</div>

**Fazit:** NFV und SDN lösen verschiedene Probleme — deshalb werden sie fast immer zusammen eingesetzt.

*ETSI GS NFV* · *💡 [ETSI NFV](https://www.etsi.org/technologies/nfv)*

---

## ETSI-NFV-Architektur: NFVI, VNF, MANO, OSS/BSS

<div class="columns-15">
<div>

- **VNF:** virtualisierte Netzfunktion (Software-Image) — heute oft Container (CNF, → 5.4)
- **NFVI:** Compute, Storage, Network — Virtualisierungsschicht plus physische Ressourcen
- **VNFM:** VNF-Manager — Lebenszyklus einzelner VNF (Instantiate, Scale, Heal)
- **VNFO:** NFV-Orchestrator — orchestriert Services und Ressourcen; VNFM + VNFO = **MANO**
- **OSS/BSS, EMS:** Betriebs- und Business-Systeme, Element-Management
- **Reference Points** (Vi-Vn, Or-Vi, Or-Vnfm …) als Schnittstellen

</div>
<div>

![h:300px](figures/4-nfv/copyright/fig-12.png)

</div>
</div>

**Fazit:** NFV trennt Funktion, Infrastruktur und Management — MANO steuert beides.

*ETSI GS NFV 002 – Architectural Framework* · *💡 [ETSI NFV](https://www.etsi.org/technologies/nfv)*

---

## MANO: Orchestrierung und VNF-Lebenszyklus

<div class="columns">
<div>

**Lebenszyklus**

- Onboarding: VNF-Paket mit Deskriptor (VNFD) und Images
- Instantiate: VNF auf der NFVI ausrollen, Service verknüpfen (VNF Forwarding Graph)
- Betrieb: Scale Out/In, Heal, Update, Terminate

</div>
<div>

**Umsetzungen**

- VIM: OpenStack (Nova, Neutron) stellt die NFVI bereit
- MANO: OSM (ETSI-Referenz), ONAP (Linux Foundation), OpenStack Tacker
- Konkurrenz heute: Container mit Kubernetes und Helm statt VNF-Pakete (→ 5.4)

</div>
</div>

<div class="food-for-thought">

🧠 MANO ist seit 2012 standardisiert — warum hat sich trotzdem Kubernetes in der Praxis durchgesetzt?

</div>

*ETSI GS NFV-MAN 001 / GS NFV-IFA 010*

---

## Zusammenspiel von SDN und NFV

<div class="columns">
<div>

**Was NFV allein nicht kann**

- VNFs müssen verbunden werden: Service Function Chaining (SFC)
- Verkehr muss durch die richtige Kette laufen — das ist Steuerung
- Skalierung und Umleitung brauchen dynamische Connectivity

</div>
<div>

**Was SDN beiträgt**

- Die programmierbare Control Plane liefert Pfade und Policies
- Northbound (Layer 4–7) die NFV-Orchestrierung, southbound (Layer 2–3) das Netz
- Betriebsbeispiel: SD-WAN (Kapitel 4 und nächste Folie)

</div>
</div>

**Fazit:** NFV liefert die Funktionen, SDN die Wege dazwischen — beide ergänzen sich, sind aber nicht dasselbe.

*7E §10 – Operating Networks* · *SDN-Buch §8.6 – Is Network Virtualization SDN?*

---

## SD-WAN: Konzept

- WAN-Overlay über beliebigem Underlay: MPLS, Breitband-Internet, LTE/5G
- Zentrale Steuerung: Policies je Anwendung statt Konfiguration je Link
- Dynamisches Load Sharing und Failover über mehrere WAN-Links, reagierend auf die Link-Qualität
- Ablösung von MPLS: Internet-Anbindung plus Overlay statt teurer MPLS-Strecke — günstiger und flexibler
- Zero-Touch-Provisioning: die Zweigstelle holt ihre Konfiguration selbst (vgl. Kapitel 4 – Google B4)
- SD-WAN-Komponenten sind selbst VNFs/CNFs — der Edge ist eine virtuelle Appliance

<div class="columns">
<div>

![h:160px](figures/4-nfv/copyright/fig-14-ohne.png)

</div>
<div>

![h:160px](figures/4-nfv/copyright/fig-14-mit.png)

</div>
</div>

**Fazit:** SD-WAN ersetzt die teure WAN-Strecke durch ein steuerbares Overlay.

*Quelle: VeloCloud (Arista)* · *💡 [flexiWAN](https://flexiwan.com/) (Open Source)*

---

## SD-WAN: Produkt und Markt

- Der Markt ist konsolidiert: VeloCloud → **Arista**, Viptela → **Cisco**, daneben Versa, Fortinet, Palo Alto
- Netzbetreiber verkaufen SD-WAN als Managed Service, dazu Open Source (flexiWAN)
- **SASE:** SD-WAN plus Security (SWG, ZTNA, CASB) aus der Cloud — Netz und Sicherheit konvergieren
- Für Betreiber wird das WAN zum Software-Produkt: Betriebs- und Skills-Wandel, nicht nur Technik
- 💡 [7E §10.3 – Network Configuration](https://7e.systemsapproach.org/operations.html) – Automatisierung als Grundlage

<div class="takeaway">

**Fazit:** SD-WAN ist kein Protokoll, sondern ein Betriebsmodell.

</div>

*Marktüberblick: Anbieter- und Betreiber-Websites, Stand 9/2026*

---

<!-- _class: section-break -->

# 5.4 Cloud-native Networking

VNF vs. CNF · CNI · eBPF/Cilium · Service Mesh · DPUs

---

## VNF oder CNF? VM-Image vs. Container

| | **VNF (VM)** | **CNF (Container)** |
| --- | --- | --- |
| Artefakt | VM-Image (qcow2) + VNF-Deskriptor | Container-Image + Helm-Chart |
| Isolation | eigener Kernel, Hypervisor | geteilter Kernel, Namespaces/cgroups |
| Startzeit | Sekunden bis Minuten | Millisekunden bis Sekunden |
| Speicherbedarf | GB | MB |
| Skalierung | Replikate als VMs, Live-Migration | Replikate als Pods, Rolling Upgrades |
| Betrieb | MANO mit OpenStack | Kubernetes, GitOps |

<div class="food-for-thought">

🧠 Ist eine VNF heute nicht einfach ein Container? Was bleibt vom ETSI-Modell — und was nicht?

</div>

**Fazit:** CNF ist nicht „kleiner", sondern anders betrieben — deklarativ und elastisch.

*💡 [CNCF](https://www.cncf.io/)* · *ETSI GR NFV-IFA 029 – Cloud-native VNFs*

---

## Kubernetes-Networking: das CNI

- Kubernetes-Netzmodell: **jeder Pod hat eine eigene IP**, flaches Netz, kein NAT zwischen Pods
- **CNI** (Container Network Interface): Plug-in für IP-Adressvergabe, Routing und Policy
- Overlay-CNIs kapseln (VXLAN/Geneve), Routing-CNIs verteilen Pod-Routen per BGP
- Dienste: ClusterIP, NodePort, LoadBalancer — realisiert von kube-proxy **oder** direkt im Datenpfad
- 💡 [Kubernetes – Cluster Networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) – Netzmodell und CNI
- 💡 [CNCF Landscape](https://landscape.cncf.io/) – CNI- und Mesh-Projekte im Überblick

**Fazit:** Das Pod-Netz ist ein eigenes Overlay — Kubernetes macht daraus ein Flat Network.

*7E §10.2 – Host Configuration* · *CNCF*

---

## eBPF statt iptables: Cilium

- Klassisch schreibt kube-proxy iptables-Ketten — das Regelwerk wächst linear und wird teuer
- **eBPF** führt Programme im Kernel an Hooks aus (XDP, TC); **Maps** ersetzen Regelketten
- Cilium ersetzt kube-proxy im eBPF-Datenpfad (`kubeProxyReplacement`) — Lastverteilung an der NIC
- Dazu NetworkPolicy (L3/L4), Filterung auf L7 (HTTP, gRPC, DNS) und Hubble-Telemetrie
- 💡 [Cilium](https://cilium.io/) – CNI, kube-proxy-Ersatz und Service Mesh auf eBPF
- 💡 [ebpf.io](https://ebpf.io/) – was eBPF ist und wo es ansetzt

**Fazit:** Netzfunktionen wie NAT, Load Balancing und Policy sind heute Kernel-Programme.

*Cilium-Doku (docs.cilium.io)* · *vgl. Kapitel 6*

---

## Service Mesh als Overlay

- Problem: Microservices brauchen mTLS, Retries, Timeouts, Tracing, Traffic-Splitting — in jeder Sprache neu?
- Lösung: ein **L7-Netz** über dem Pod-Netz, in dem diese Funktionen zentral konfiguriert werden
- Zwei Bauformen: Sidecar-Proxy je Pod (Envoy) oder eBPF-Datenpfad (Cilium)
- Die Control Plane (Istio, Linkerd) verteilt die Konfiguration; der Datenpfad bleibt dezentral
- Kosten: zusätzliche Hops, Komplexität und Ressourcen je Sidecar
- 💡 [Istio](https://istio.io/) – Referenzimplementierung mit dokumentiertem Datenpfad

<div class="takeaway">

**Fazit:** Ein Service Mesh ist ein Overlay der anderen Art — es virtualisiert Verhalten, nicht Links.

</div>

*CNCF Landscape* · *7E §16 – Overlay Networks*

---

## Ausblick: DPU-beschleunigte Netzfunktionen

- DPU/IPU: eigene CPU-Kerne, NIC-ASIC und Beschleuniger auf einer Karte im Server
- Verschiebt vSwitch, CNI-Datenpfad, IPsec/mTLS und Storage (NVMe-oF) vom Host auf die Karte
- Host-Kerne bleiben frei für Workloads — Trennung von Infrastruktur und Anwendung
- Netzfunktionen laufen auf der DPU selbst als Container (NVIDIA DOCA, AMD Pensando)
- Marktstand 9/2026: NVIDIA BlueField-4 mit 800 Gb/s (angekündigt 3/2025), AMD Pensando Salina mit 400 Gb/s
- 💡 [NVIDIA – DPU-Produktseite](https://www.nvidia.com/en-us/networking/products/data-processing-unit/)

**Fazit:** Die nächste Auslagerungsstufe nach Kernel und User Space ist die Karte selbst.

*Vendor-Doku 2025/2026 (NVIDIA, AMD)* · *vgl. Kapitel 6 und 8*

---

## Lernzielkontrolle ✍️🧠

- Warum brauchen Cloud-Netze Overlays wie VXLAN — und was leistet der 24-Bit-VNI?
- Wie unterscheiden sich virtuelle und physische Switches in einem Hypervisor-Host?
- Was kann ein Software-vSwitch auf der CPU, was kann er nicht?
- Wann hilft SR-IOV, wann DPDK, wann XDP/eBPF?
- Was ist der Unterschied zwischen NFV und SDN?
- Erklären Sie NFVI, VNF, VNFM, VNFO und OSS/BSS in je einem Satz.
- Was orchestriert MANO über den Lebenszyklus einer VNF hinweg?
- Welches Problem löst SD-WAN, das MPLS nicht löst?
- Was unterscheidet ein CNI-Overlay von einem Routing-CNI?
- Warum ersetzt eBPF die iptables-Ketten von kube-proxy?
- Wozu dient ein Service Mesh — und was kostet es?

*Bezug: ETSI GS NFV · RFC 7348 · 7E §9.4, §10 · SDN-Buch §8*

---

## Praktische Übungen und Demo-Links 🛠️🧑‍🔬

1. **VXLAN von Hand bauen (containerlab):** `ip link add vxlan10 type vxlan id 10 remote … dstport 4789`, dazu eine Bridge — Ping über das Overlay
2. **Kapselung entschlüsseln:** `tcpdump -i eth0 -vv udp port 4789` — äußere Köpfe lesen, VNI und inneres Ethernet identifizieren
3. **Open vSwitch:** `ovs-vsctl add-br br-vx`, `ovs-vsctl add-port br-vx vxlan0 -- set interface vxlan0 type=vxlan options:remote_ip=…`, Flows mit `ovs-ofctl dump-flows` prüfen
4. **Container-Netzwerk mit Cilium:** Kind-/k3s-Cluster, Cilium mit `kubeProxyReplacement=true` installieren, `cilium status` und `hubble observe` — Service-Lastverteilung im Datenpfad beobachten
5. **SD-WAN-Idee nachstellen:** zwei Uplinks mit `containerlab tools netem` (Delay/Loss) versehen und die Policy im Overlay umschalten
   - 💡 [containerlab](https://containerlab.dev/) · 💡 [Cilium – Getting Started](https://docs.cilium.io/en/stable/gettingstarted/) · 💡 [Open vSwitch – Doku](https://www.openvswitch.org/)

*Lab-Stack: containerlab, Cilium, Open vSwitch — vgl. Kapitel 1–4 (Übungen)*

---

## Weiterführende Literatur & Links 💡

<div class="columns3">
<div class="card">

**Primärquellen**

- 💡 [ETSI NFV – Technologie und Spezifikationen](https://www.etsi.org/technologies/nfv) · [ETSI GS NFV 002 (PDF)](https://www.etsi.org/deliver/etsi_gs/NFV/001_099/002/01.02.01_60/gs_NFV002v010201p.pdf)
- 💡 [RFC 7348 – VXLAN](https://www.rfc-editor.org/rfc/rfc7348)

</div>
<div class="card">

**Referenzliteratur**

- 💡 [7E §9.4 – Virtual Networks for Datacenters](https://7e.systemsapproach.org/virtual.html) · [7E §10 – Operating Networks](https://7e.systemsapproach.org/operations.html)
- 💡 [SDN-Buch §8 – Network Virtualization](https://sdn.systemsapproach.org/netvirt.html)

</div>
<div class="card">

**Praxis und Werkzeuge**

- 💡 [Cilium](https://cilium.io/) · [ebpf.io](https://ebpf.io/)
- 💡 [DPDK](https://www.dpdk.org/) · [Open vSwitch](https://www.openvswitch.org/)
- 💡 [CNCF](https://www.cncf.io/) · [containerlab](https://containerlab.dev/)
- 💡 [Kapitel 3 – Netzvirtualisierung](3-AdvCompNet-Netzvirtualisierung.md) · [Kapitel 6 – P4](6-AdvCompNet-P4-ProgrammableDataPlane.md)

</div>
</div>

> 🧠 Welche Netzfunktion in Ihrem Umfeld würden Sie virtualisieren — und welche bewusst auf Hardware lassen?
