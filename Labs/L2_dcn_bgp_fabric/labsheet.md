# Lab L2 — Leaf-Spine-Fabric mit BGP (FRR)

**Advanced Computer Networks · HS Fulda · MMNet**
Ersetzt das frühere GNS3-Lab „Leaf-Spine-Architekturen mit BGP (IOSv)“.

---

## Lernziele

- Ein **Leaf-Spine-Fabric** (4 Leafs, 2 Spines, 4 Hosts) mit **eBGP** aufbauen und in Betrieb nehmen
- **ECMP** über zwei Spine-Pfade erkennen und messen
- **Fehlertoleranz** bewerten: kontrollierter Linkausfall vs. stiller Paketverlust
- Den Nutzen von **BFD** (Bidirectional Forwarding Detection) belegen

## Voraussetzungen

- Linux mit Docker und **containerlab ≥ 0.56** (`containerlab version`)
- Image `frrouting/frr:latest` und `alpine:3.20` (beide ohne Registrierung nutzbar — **BYOD-fähig**)
- Grundkenntnisse `ip`/`ping`/`traceroute`, etwas Geduld mit BGP-Timern

**Aufwand:** ca. 90–120 Minuten · Bearbeitung einzeln oder im Team

---

## Topologie

```
        h1        h2        h3        h4       172.23.24-27.100/24
        |         |         |         |
     leaf1     leaf2     leaf3     leaf4      AS 65011-65014
        \  \   /  /   \  /   /  /
         \  \ /  /     \/   /  /
          spine1        spine2               AS 65001
```

- **Leaf ↔ Spine:** je zwei Pfade pro Leaf (`10.0.x.0/30` → spine1, `10.1.x.0/30` → spine2)
- **Leaf ↔ Host:** `172.23.2x.0/24`, Leaf ist Default-Gateway (`172.23.2x.1`)
- **Adressplan:**

| Gerät | AS | Host-Segment | Router-ID |
|---|---|---|---|
| leaf1 | 65011 | 172.23.24.0/24 | 10.20.30.1 |
| leaf2 | 65012 | 172.23.25.0/24 | 10.20.30.2 |
| leaf3 | 65013 | 172.23.26.0/24 | 10.20.30.3 |
| leaf4 | 65014 | 172.23.27.0/24 | 10.20.30.4 |
| spine1 / spine2 | 65001 | — | 10.20.30.101 / .102 |

Start und Stopp:

```bash
cd Labs/L2_dcn_bgp_fabric
containerlab deploy  -t fabric.clab.yml        # startet alle 10 Knoten
containerlab inspect -t fabric.clab.yml        # Status + Management-IPs
containerlab destroy -t fabric.clab.yml --cleanup
```

---

## Wichtig beim Start

Nach `containerlab deploy` **ca. 60 s warten**, bevor Sie messen: BGP braucht auf einem frischen
Boot einige Zyklen, bis alle Sitzungen stehen und beide Pfade in der Routingtabelle sind
(gemessen: nach 20 s nur ein Nexthop, nach 60 s beide → ECMP). Prüfen Sie zuerst:

```bash
docker exec clab-acn-l2-fabric-leaf1 vtysh -c "show ip bgp summary"     # 2 Nachbarn, Spalte State/PfxRcd > 0
docker exec clab-acn-l2-fabric-leaf1 ip route show 172.23.27.0/24       # 2 Nexthops
docker exec clab-acn-l2-fabric-leaf1 vtysh -c "show bfd peers brief"    # beide up
```

> **Nicht** `frrinit.sh restart` in einem Knoten ausführen: Das beendet PID 1, Docker startet den
> Container neu — und damit sind alle veth-Interfaces im Container weg. Einzelne Daemons dürfen
> neu gestartet werden (`pkill bgpd`, watchfrr startet ihn neu); genau das macht die Topologie
> beim Deploy automatisch, um FRRs „Waiting for NHT" nach dem Kaltstart zu vermeiden.

## Aufgabe 1 — Inbetriebnahme prüfen

1. Prüfen Sie auf `leaf1` die BGP-Sitzungen: `docker exec -it clab-acn-l2-fabric-leaf1 vtysh -c "show ip bgp summary"`
   - Wie viele Nachbarn, welcher Status, wie viele empfangene Präfixe?
2. Prüfen Sie die gelernten Routen: `ip route` bzw. `vtysh -c "show ip bgp"`
   - **Frage:** Warum taucht `172.23.27.0/24` mit **zwei** Nexthops auf?
3. Testen Sie die Ende-zu-Ende-Erreichbarkeit von `host1` nach `host4` (und umgekehrt):
   `docker exec clab-acn-l2-fabric-host1 ping -c3 172.23.27.100`
4. Prüfen Sie mit `traceroute` (auf einem Host): welche Spines werden durchlaufen?
   - **Frage:** Warum sehen Sie je nach Ziel-/Quell-Port unterschiedliche Pfade? (Hash über das 5-Tupel)

## Aufgabe 2 — Kontrollierter Linkausfall

Simulieren Sie einen Leitungsausfall so, dass BGP ihn **sofort** bemerkt:

```bash
docker exec clab-acn-l2-fabric-leaf1 ip link set eth1 down
docker exec clab-acn-l2-fabric-host1 ping -c10 -i0.5 172.23.27.100
docker exec clab-acn-l2-fabric-leaf1 ip link set eth1 up
```

1. Wie viele Pakete gehen verloren? Wie erklärt sich die Größenordnung?
2. Was zeigt `show ip bgp summary` während des Ausfalls?
3. **Frage:** Wie lange dauert die Konvergenz, und wovon hängt sie ab?

## Aufgabe 3 — Stiller Paketverlust (der gemeine Fall)

Ein Ausfall, der **keine** Link-Down-Meldung erzeugt (z. B. degradierte Optik, falsch konfigurierter Filter):

```bash
# 100 % Paketverlust auf dem Link leaf1 → spine1
containerlab tools netem set -n clab-acn-l2-fabric-leaf1 -i eth1 --loss 100
docker exec clab-acn-l2-fabric-host1 ping -c10 -i0.5 172.23.27.100

# Verlust wieder entfernen
containerlab tools netem set -n clab-acn-l2-fabric-leaf1 -i eth1
```

1. Was beobachten Sie **mit** aktivem BFD (Standard in dieser Topologie)?
2. Stellen Sie BFD für einen Nachbarn ab und wiederholen Sie den Versuch:
   ```bash
   docker exec -it clab-acn-l2-fabric-leaf1 vtysh
   conf t
     router bgp 65011
       no neighbor 10.0.1.1 bfd
   end
   ```
   Was passiert jetzt mit dem Ping? Wie lange dauert die Reaktion?
3. **Frage:** Warum ist das für Produktionsnetze der wichtigere Fall — und welche Alternativen zu BFD kennen Sie?

## Warum sieht man zwei Nexthops? (ECMP in eBGP)

Damit ein Router **beide** gelernten Wege in die Weiterleitungstabelle aufnimmt, müssen die Pfade
*equal* sein (gleiche AS-Pfad-Länge, gleiche Metrik) **und** Multipath erlaubt sein. Die Topologie
setzt dafür explizit `maximum-paths 2` in der `address-family ipv4 unicast`. Ohne diese Zeile bleibt
es bei einem einzigen (besten) Pfad — die Redundanz existiert dann nur als Reserve, nicht als
Bündelung. Prüfen Sie beides: einmal mit, einmal ohne `maximum-paths 2`.

## Aufgabe 4 — Fabric bewerten (Diskussion)

1. **Oversubscription:** Wie viele Hosts können gleichzeitig mit voller Bandbreite zu Hosts hinter anderen Leafs sprechen? Was ändert sich, wenn Sie auf einen Spine verzichten?
2. **Bisektionsbandbreite:** Bestimmen Sie sie für diese Topologie (Annahme: jeder Leaf-Spine-Link 10 GbE).
3. **Skalierung:** Was kostet es, auf 8 Leafs und 4 Spines zu erweitern — Ports, Kabel, AS-Nummern?
4. **Vergleich:** Ordnen Sie die Topologie in „klassischer 3-Tier-Tree“ vs. „Leaf-Spine“ ein (vgl. Vorlesung Kapitel 2).
5. **Eigene Erweiterung:** Ergänzen Sie einen fünften Host an `leaf1` (eigenes /24) und bringen Sie ihn per BGP ins Fabric.

---

## Verifikation (erwartete Ergebnisse)

| Prüfschritt | Erwartung |
|---|---|
| `show ip bgp summary` auf einem Leaf (nach ~60 s) | 2 Nachbarn, **Spalte `State/PfxRcd` zeigt 3** (Zahl = empfangene Präfixe; FRR schreibt nicht „Estab") |
| `show ip bgp summary json` | `"state":"Established"` bei allen Nachbarn (skript-freundlich) |
| `ip route show 172.23.27.0/24` | **zwei** Nexthops (ECMP über spine1 und spine2) |
| `show bfd peers brief` | beide BFD-Sessions `up` |
| `show running-config` (address-family) | `maximum-paths 2` gesetzt — sonst wird nur **ein** Spine-Pfad installiert |
| `host1 → 172.23.27.100` | 0 % Paketverlust, RTT < 1 ms |
| `ip link set eth1 down` | kurzer Verlust (≤ 1 Paket), danach 0 % |
| `netem --loss 100` **mit** BFD | 0 % Verlust — Pfad wird umgeschaltet |
| `netem --loss 100` **ohne** BFD | Verlust bis zur BGP-Reaktion (Sitzung stirbt erst nach Hold-Time, Standard 180 s!) |

## Hinweise & Troubleshooting

- **Keine BGP-Sitzung:** Stimmen `remote-as` und die Interface-Adressen? `vtysh -c "show ip bgp neighbors"`
- **Routen werden gelernt, aber keine Konnektivität:** Prüfen Sie `next-hop-self` auf den Spines — ohne diese Einstellung zeigen Remote-Leafs auf unerreichbare Nachbaradressen.
- **Hosts ohne Route:** `ip route` auf dem Host prüfen (Management-Default bleibt über `eth0` bestehen; das Lab nutzt deshalb eine explizite Route für `172.23.0.0/16`).
- **vtysh meldet fehlende `vtysh.conf`:** kosmetisch; im Lab ist `configs/vtysh.conf` eingebunden.
- Netzwerkverkehr mitschneiden: `docker exec clab-acn-l2-fabric-leaf1 tcpdump -ni eth1 port 179`

## Bezug zur Vorlesung

- Kapitel 2 (Data Center Networking): Leaf-Spine, Oversubscription, Bisektionsbandbreite, ECMP
- Kapitel 4 (SDN): zentrale vs. verteilte Control Plane — hier ist die Control Plane **verteilt**
- 7E §4.5 „Routing in Datacenters“ · SDN-Buch Ch. 3.5/7 (Leaf-Spine-Fabric)

> Dieses Lab ist der Nachfolger von `3_dcn_bgp_fabric` (GNS3 + Cisco IOSv). Der wesentliche Unterschied:
> Es läuft **ohne Vendor-Images und ohne Account** auf jedem Linux mit Docker.
