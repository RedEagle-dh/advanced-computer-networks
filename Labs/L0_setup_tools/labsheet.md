# Lab L0 — Setup, Werkzeuge und Netz-Diagnose

**Advanced Computer Networks · HS Fulda · MMNet**
Ersetzt die frühere GNS3-Einführung (`1_gns3_intro`). Ziel: **jede:r** kann auf dem eigenen Rechner
ein virtuelles Netz starten, messen und mitschneiden — ohne Vendor-Images und ohne Account.

---

## Lernziele

- **containerlab** installieren/prüfen und eine Topologie aus einer YAML-Datei starten
- Knoten inspizieren, Kommandos darin ausführen, Topologie sauber abbauen
- Mit `ping`, `traceroute`/`mtr`, `tcpdump` und `iperf3` **messen** statt raten
- Verstehen, wie Adressierung (IP via `exec`), Routing (FRR/OSPF) und Mitschnitt zusammenspielen

## Voraussetzungen

- Linux mit **Docker** (oder eine VM mit Docker); `containerlab ≥ 0.56`
- Installation: siehe <https://containerlab.dev/install/> — ein `sudo`-fähiger Nutzer genügt
- Images: `frrouting/frr:latest` (Alpine-Basis, bringt `ip`/`bridge`/`tc` mit), `alpine:3.20`
  (frei, ohne Registrierung — **BYOD-fähig**)
- **Mac mit Apple Silicon:** containerlab in einer OrbStack-VM, FRR als natives arm64-Image —
  siehe [`Labs/README.md`](../README.md), Abschnitt *Mac mit Apple Silicon*
- Tools im Container: `ping` und `traceroute` sind enthalten; **`tcpdump` und `iperf3` fehlen**
  in beiden Images und werden per `apk add …` nachinstalliert (Internetzugang aus dem Container
  nötig)

**Aufwand:** ca. 60–90 Minuten · Bearbeitung einzeln

---

## Topologie

```
 client ──── router ──── server
10.10.10.2  .1|      |.1  10.10.20.3
            10.10.10.0/24   10.10.20.0/24
```

- **router**: FRR mit **zebra** (Interfaces) und **ospfd** (Routing)
- **client/server**: Alpine-Container mit statischen Routen

```bash
cd Labs/L0_setup_tools
containerlab deploy  -t setup.clab.yml
containerlab inspect -t setup.clab.yml
containerlab destroy -t setup.clab.yml --cleanup
```

> **Wichtig:** Interface-IPs werden im Topology-File per `exec` gesetzt — das läuft **nach** dem
> Anlegen der Links. Adressen in der `frr.conf` würden von Zebra gelesen, *bevor* die Links
> existieren, und dann nie angewendet (typische Stolperfalle beim Umstieg von GNS3).

---

## Aufgabe 1 — Topologie starten und inspizieren

1. Starten Sie die Topologie. Welche Knoten laufen, welche Management-IP hat jeder?
2. Öffnen Sie eine Shell in `client` bzw. `router`:
   ```bash
   docker exec -it clab-acn-l0-setup-client sh
   docker exec -it clab-acn-l0-setup-router vtysh
   ```
3. Prüfen Sie im `router`: `show ip route` — welche Routen stehen in der RIB, welcher Protokollcode?

## Aufgabe 2 — Erreichbarkeit und Pfad messen

1. `ping -c3 10.10.20.3` vom `client` aus. Wie hoch ist die RTT?
2. `traceroute -n 10.10.20.3` — wie viele Hops? Warum genau diese?
3. Installieren Sie `tcpdump` auf dem `router` (`apk add tcpdump` — fehlt im `frrouting/frr`-Image)
   und sniffen Sie mit `tcpdump -nvi eth2 icmp` mit, während Sie parallel auf dem `client` einen
   Dauer-Ping (`ping 10.10.20.3`) laufen lassen.
   - **Frage:** Welche Pakete sehen Sie — Echo Request, Echo Reply oder beides? Ändert sich die TTL,
     wenn Pakete den Router passieren? (Gegenprobe: derselbe Mitschnitt auf `eth1`.)

## Aufgabe 3 — Störungen erzeugen und sichtbar machen

1. **Latenz/Verlust künstlich erhöhen** (auf dem Router-Link Richtung Server):
   ```bash
   containerlab tools netem set -n clab-acn-l0-setup-router -i eth2 --delay 100ms --jitter 20ms
   ping -c5 10.10.20.3          # vom client aus
   containerlab tools netem reset -n clab-acn-l0-setup-router -i eth2   # Impairments entfernen
   ```
   > Der `set`-Befehl meldet zurzeit immer `Could not get all qdiscs: extractXStats(): unsupported
   > kind: netem.` — ein Lesefehler in containerlab/go-tc (siehe Troubleshooting). Die Impairments
   > werden **trotzdem gesetzt**; Kontrolle im Router mit `tc qdisc show dev eth2`.
   - **Frage:** Wie verändert sich die RTT-Verteilung (min/avg/max)? Was erklärt das?
2. **Durchsatz messen:** installieren Sie `iperf3` in beiden Containern (`apk add iperf3`), starten
   Sie den Server auf `server` (`iperf3 -s`) und den Client auf `client` (`iperf3 -c 10.10.20.3`).
   - Wiederholen Sie die Messung mit 100 ms Delay auf dem Link. Was ändert sich?
   - **Frage:** Warum bricht der Durchsatz ein, obwohl die Linkrate 10 Gbit/s beträgt?
3. **Route kaputt machen:** Deaktivieren Sie OSPF-Netz auf dem Router (`vtysh` → `conf t` →
   `router ospf` → `no network 10.10.20.0/24 area 0`). Was passiert mit dem Ping? Rückgängig machen!

## Aufgabe 4 — Reflexion

1. Recherchieren Sie, wie GNS3 funktioniert (Emulation von Router-/Switch-Images, GUI-Aufbau), und
   vergleichen Sie das Setup mit containerlab. Denken Sie dabei z. B. an: Container sind zwar auch in
   GNS3 möglich, Topologien werden aber in der GUI zusammengeklickt und konfiguriert; die GUI
   braucht mehr Ressourcen und Installation — auch bei GNS3 mit Server-Backend, wie wir es bislang
   genutzt haben. Was ist einfacher, was schwieriger?
2. Wo liegen die Grenzen der Container-Netze (z. B. keine Router-Images mit proprietärem Datenpfad)?
3. **Ausblick:** In Lab L2 bauen Sie damit ein komplettes Leaf-Spine-Fabric mit BGP auf.

---

## Verifikation (erwartete Ergebnisse)

| Prüfschritt | Erwartung |
|---|---|
| `containerlab inspect` | 3 Knoten `running` |
| `show ip route` im Router | beide Subnetze, Quelle `connected` und/oder `OSPF` |
| `ping` client → server | 0 % Verlust, RTT < 1 ms |
| `traceroute` client → server | 2 Hops (10.10.10.1, 10.10.20.3) |
| `tcpdump -nvi eth2` bei Dauer-Ping | Echo Request **TTL 63**, Echo Reply **TTL 64**; auf `eth1` 64/63 — der Router senkt die TTL um genau 1 |
| `netem --delay 100ms` | RTT steigt deutlich, Verlust bleibt 0 |
| `iperf3` über den Link mit 100 ms Delay | Durchsatz bricht ein (BDP-/Fenster-Grenze, vgl. Kapitel 1) |

## Troubleshooting

- **Container startet nicht:** `docker ps -a`, Logs prüfen (`docker logs clab-acn-l0-setup-router`).
- **Kein Ping:** `ip addr` und `ip route` in beiden Endpunkten prüfen — häufig fehlt die Route bzw. das
  `ip link set … up`.
- **`tools netem set` meldet `unsupported kind: netem`:** bekannter Lesefehler in der
  containerlab-Abhängigkeit go-tc (kann die Statistiken eines netem-Qdiscs nicht parsen, v0.4.8 und
  auch aktueller Stand) — **kein NixOS-/Distributionsproblem**, trifft jede Linux-Installation.
  Der netem-Qdisc ist trotzdem aktiv (Kontrolle: `tc qdisc show dev <if>`); Entfernen funktioniert
  mit `containerlab tools netem reset -n <node> -i <if>`.
- **`tcpdump`/`iperf3` fehlen:** `apk add tcpdump` bzw. `apk add iperf3` im jeweiligen Container.
  Wenn `apk` hängt: Die Topologie schaltet das Mgmt-IPv6 ab (`ipv6-subnet: ""`), weil die Container
  sonst eine IPv6-Default-Route ohne echten IPv6-Egress bekommen und AAAA-first-Clients (busybox)
  am toten Pfad blockieren. Hinter VPN/eduVPN/Tailscale kann zusätzlich der Docker-DNS-Upstream
  unerreichbar sein → im Container DNS umstellen
  (`echo "nameserver 9.9.9.9" > /etc/resolv.conf`); Kontrolle:
  `wget -T5 -O /dev/null https://dl-cdn.alpinelinux.org 2>&1 | tail -1`.
- **`vtysh` warnt „Can't open vtysh.conf":** kosmetisch; im Lab ist `configs/vtysh.conf` eingebunden.
- **Alles hängt:** `containerlab destroy -t setup.clab.yml --cleanup` und neu deployen.

## Bezug zur Vorlesung

- Kapitel 1: Latenz, Bitrate, Bandwidth-Delay-Product, Messmethoden
- Kapitel 2/4: Topologien und Control Plane (hier OSPF, in L2 BGP)
