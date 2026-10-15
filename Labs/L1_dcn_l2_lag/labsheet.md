# Lab L1 — Layer 2 im Rechenzentrum: Redundanz ohne Schleifen

**Advanced Computer Networks · HS Fulda · MMNet**
Ersetzt das frühere GNS3-Lab `2_dcn_stp_lag` (Arista vEOS). Läuft mit **Linux-Bridges und LACP**
— ohne Vendor-Images.

---

## Lernziele

- **Warum** L2-Redundanz überhaupt ein Problem ist: Broadcast-Schleifen und der Grund für STP
- **STP** beobachten: wer ist Root, welcher Port blockiert, wie lange dauert die Konvergenz?
- **Link Aggregation (LACP/802.3ad)** als Alternative: Bündelung statt Blockierung
- Beide Verfahren **messen** und die Betriebsfolgen bewerten (Ausfallzeit, Auslastung, Skalierung)

## Voraussetzungen

- Linux mit Docker und **containerlab** (siehe Lab L0)
- Images: `frrouting/frr:latest` (Debian-basiert, enthält `bridge`/`ip` aus iproute2), `alpine:3.20`
- Keine Registrierung nötig — **BYOD-fähig**

**Aufwand:** ca. 90 Minuten · Bearbeitung einzeln oder im Team

---

## Szenario 1 — Ring mit Spanning Tree

```
   h1 ── sw1 ──────── sw2 ──┐
          │                 │
          │              sw3 ── h2
          │                 │
          └──── sw4 ────────┘        (Ring = genau eine Schleife)
```

```bash
cd Labs/L1_dcn_l2_lag
containerlab deploy  -t scenario1-stp.clab.yml
containerlab inspect -t scenario1-stp.clab.yml
containerlab destroy -t scenario1-stp.clab.yml --cleanup
```

### Aufgabe 1.1 — Zustand verstehen

1. Prüfen Sie auf jedem Switch die Port-Zustände:
   ```bash
   docker exec clab-acn-l1-stp-sw1 bridge link show
   docker exec clab-acn-l1-stp-sw3 bridge link show
   ```
   **Frage:** Welcher Port ist `blocking`, und warum genau dieser?
2. Ermitteln Sie die **Root Bridge**: `docker exec clab-acn-l1-stp-sw1 bridge -d link show` und
   `cat /sys/class/net/br0/bridge/root_id` — wer ist Root, woran wird das entschieden?
3. Testen Sie die Erreichbarkeit `h1 → h2` (`docker exec clab-acn-l1-stp-h1 ping -c3 10.20.0.2`).

### Aufgabe 1.2 — Ausfall messen (Kernexperiment)

Starten Sie einen Dauer-Ping und trennen Sie **den aktiven** Link auf `sw3` (Richtung `sw4`):

```bash
docker exec clab-acn-l1-stp-h1 ping -i 0.5 -c 90 10.20.0.2     # Terminal 1
docker exec clab-acn-l1-stp-sw3 ip link set eth2 down            # Terminal 2
```

1. Wie viele Pakete gehen verloren? Rechnen Sie die Ausfallzeit aus (Intervall × verlorene Pakete).
2. Was passiert mit dem vorher blockierten Port? Prüfen Sie erneut `bridge link show`.
3. **Vergleich:** Was wäre die Ausfallzeit in einem Netz mit 20 Switches?
4. **Frage:** Warum ist STP für moderne Rechenzentren zu langsam? Was hilft (RSTP, LACP, MLAG, Fabric)?

> **Gemessenes Referenzergebnis (HS-Fulda-Testumgebung):** 61 von 90 Paketen verloren ⇒
> **ca. 30 s Ausfallzeit** — das sind die 802.1D-Timer (Max Age 20 s + Forward Delay 15 s).

---

## Szenario 2 — Link Aggregation (LACP)

```
   h1 ── sw1 ══════════ sw2 ── h2
              zwei Links = ein Bond (802.3ad)
```

```bash
containerlab deploy -t scenario2-lag.clab.yml
```

### Aufgabe 2.1 — Bündelung prüfen

1. Bond-Status ansehen:
   ```bash
   docker exec clab-acn-l1-lag-sw1 cat /proc/net/bonding/bond0
   ```
   **Frage:** Wie viele Slaves sind aktiv (`MII Status: up`), welchen Aggregator haben sie?
2. Erreichbarkeit testen (`clab-acn-l1-lag-h1` → `10.21.0.2`).
3. **Frage:** Wie viel Bandbreite steht zwischen den Switches zur Verfügung, wenn jede Leitung 10 GbE hat?

### Aufgabe 2.2 — Ausfall messen

```bash
docker exec clab-acn-l1-lag-h1 ping -i 0.2 -c 100 10.21.0.2   # Terminal 1
docker exec clab-acn-l1-lag-sw1 ip link set eth1 down           # Terminal 2
```

1. Wie viele Pakete gehen verloren? Wie erklärt sich der Unterschied zu Szenario 1?
2. Prüfen Sie den Bond-Status erneut — was zeigt `Currently Active Slave`?
3. **Frage:** Warum braucht LACP (im Gegensatz zu STP) keine Blockierung, obwohl es einen Loop gibt?

> **Gemessenes Referenzergebnis:** **0 % Paketverlust** beim Ausfall eines Bündel-Links.

### Aufgabe 2.3 — Auslastung der Bündel-Links

1. Erzeugen Sie Last (z. B. `iperf3` in beiden Hosts) und beobachten Sie die Zähler:
   ```bash
   docker exec clab-acn-l1-lag-sw1 ip -s link show eth1
   docker exec clab-acn-l1-lag-sw1 ip -s link show eth2
   ```
   **Frage:** Verteilt der Bond einen einzelnen TCP-Strom auf beide Links? Warum (nicht)?
   Welche Rolle spielt das Hashing (vgl. ECMP im Fabric, Lab L2)?

---

## Aufgabe 3 — Bewertung und Ausblick

1. Vergleichen Sie STP und LACP in einer Tabelle: **Konvergenz, Bandbreitennutzung, Konfiguration,
   Verhalten bei mehr als zwei Switches**.
2. **MLAG/MC-LAG:** Was löst es, was STP und LACP allein nicht können? Wo braucht es proprietäre
   Erweiterungen (und warum ist das in einem offenen RZ problematisch)?
3. **Ausblick Fabric:** Erklären Sie, warum Leaf-Spine mit **L3 bis zum ToR** das L2-Redundanzproblem
   grundsätzlich umgeht (vgl. Lab L2 und Vorlesung Kapitel 2).

---

## Verifikation (erwartete Ergebnisse)

| Prüfschritt | Erwartung |
|---|---|
| `bridge link show` (Szenario 1) | genau **ein** Port `blocking`, alle anderen `forwarding` |
| `h1 → h2` (Szenario 1) | 0 % Verlust im Normalbetrieb |
| Linkausfall (Szenario 1) | ~30 s Ausfall, danach 0 % Verlust; blockierter Port wird aktiv |
| `cat /proc/net/bonding/bond0` | Mode `IEEE 802.3ad`, **beide** Slaves `MII Status: up` |
| `h1 → h2` (Szenario 2) | 0 % Verlust |
| Linkausfall (Szenario 2) | **0 %** Verlust, ein Slave `down`, Bond bleibt `up` |

## Stolperfallen

- **Bridge-Werkzeuge:** `bridge`/`ip` kommen aus **iproute2**. Alpine-BusyBox kennt `ip link add … type bridge`
  nur eingeschränkt — deshalb laufen die Switches hier im `frrouting/frr`-Image (Debian-Basis).
- **STP-Zeiten:** Nach dem Start ca. **30–50 s** warten, bevor Sie messen — die Bridge durchläuft
  Listening/Learning.
- **Bond-Reihenfolge:** Slaves müssen **down** sein, bevor sie `master bond0` bekommen, sonst meckert der Kernel.
- **`miimon 100`** (100 ms) macht den Ausfall schnell erkennbar; ohne `miimon` bleibt der Bond auf einem
  toten Link stehen.

## Bezug zur Vorlesung

- Kapitel 2 (Data Center Networking): 3-Tier-Tree, Oversubscription, Fabric-Alternativen
- Kapitel 3 (Netzvirtualisierung): VLANs und warum L2-Domänen klein bleiben sollen
- 7E §4.2 „Spanning Tree Protocol", §3.1 „Communication Links" · SDN-Buch Ch. 3.5 (Leaf-Spine)
