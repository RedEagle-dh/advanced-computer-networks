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

## Kapitel 6 · P4 / Programmable Data Plane — Detailfolien

Wintersemester 2026/2027
Master AI – Hochschule Fulda
Sebastian Rieger · MMNet

---

## Detailfolien zu Kapitel 5 (P4)

Ergänzung zur Vorlesung `6-AdvCompNet-P4-ProgrammableDataPlane.md` — hier steht der
**vollständige** Code, in der Vorlesung nur die Kernaussage.

- **Boilerplate:** V1Model-Pipeline in Einzelteilen (Parser, Match-Action, Deparser, Graph)
- **Beispiel 1 – Repeater:** vollständiges P4-Programm
- **Beispiel 2 – L2-Switch:** Parser/Deparser, MAC-Tabelle, Broadcast-Schutz, Runtime-CLI
- **Beispiel 3 – Learning Switch:** Data Plane, CPU-Header, Control-Plane-App (Python/P4Runtime)

> 🧠 Arbeiten Sie die Beispiele im Praktikum (Lab L4) selbst durch — Code lesen reicht nicht.

---

## P4 BMv2/V1Model Includes, Types, Headers

```p4
/* -*- P4_16 ProNA Boilerplate -*- */
#include <core.p4>
#include <v1model.p4>

struct headers {
}

struct metadata {
}
```

---

## P4 BMv2/V1Model Switch Pipeline

```p4
// V1Model/BMv2 architecture
V1Switch(MyParser(),
         MyVerifyChecksum(),
         MyIngress(),
         MyEgress(),
         MyComputeChecksum(),
         MyDeparser()
) main;
```

---

## Parser

```p4
// Parser
parser MyParser(packet_in pkt,
                 out headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t std_meta) {
    state start {
        transition accept;
    }
}
```

---

## Control – Match-Action

```p4
// Match-Action
control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

control MyIngress(inout headers hdr, inout metadata meta,
                   inout standard_metadata_t std_meta) {
    apply { }
}

control MyEgress(inout headers hdr, inout metadata meta,
                  inout standard_metadata_t std_meta) {
    apply { }
}

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}
```

---

## Deparser

```p4
// Deparser
control MyDeparser(packet_out pkt, in headers hdr) {
    apply { }
}
```

---

## Pipeline Graph / Control Flow

…putting all parts together…

```p4
/* -*- P4_16 -*- */
// ProNA P4 Boilerplate
#include <core.p4>
#include <v1model.p4>

struct headers { }
struct metadata { }

// Parser
parser MyParser(packet_in pkt, out headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    state start { transition accept; } }

// Match-Action
control MyVerifyChecksum(inout headers hdr, inout metadata meta) { apply { } }
control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) { apply { } }
control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) { apply { } }
control MyComputeChecksum(inout headers hdr, inout metadata meta) { apply { } }

// Deparser
control MyDeparser(packet_out pkt, in headers hdr) { apply { } }

// V1Model/BMv2 architecture
V1Switch(MyParser(), MyVerifyChecksum(), MyIngress(), MyEgress(),
         MyComputeChecksum(), MyDeparser()) main;
```

**How can we build a network element based on that using the P4 language?**

---

## ProNA P4 Repeater

```p4
/* -*- P4_16 -*- */
// ProNA P4 Repeater
#include <core.p4>
#include <v1model.p4>

struct metadata { }
struct headers { }

// Parser can stay empty, not necessary, protocol agnostic, working on physical layer/layer 1
parser MyParser(packet_in pkt, out headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    state start { transition accept; }
}

// we do not know about protocols, we do not need to care or even know about checksums, can stay empty...
control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    apply {
        // forward packets coming in from port 1 to port 2 and vice versa
        if (std_meta.ingress_port == 1) { std_meta.egress_spec = 2; }
        if (std_meta.ingress_port == 2) { std_meta.egress_spec = 1; }
    }
}

// no further changes or adaption on outgoing data necessary, egress pipeline definition can stay empty
control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    apply { }
}

// nothing changed, so no need to calculate new checksums or deparse modified header fields
control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply { }
}

control MyDeparser(packet_out pkt, in headers hdr) {
    apply { }
}

V1Switch(MyParser(), MyVerifyChecksum(), MyIngress(), MyEgress(),
         MyComputeChecksum(), MyDeparser()) main;
```

…only two lines of code added in boilerplate: select egress port based on ingress

---

## Ethernet Header, Parser and Deparser

```p4
// ...
typedef bit<48> macAddr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

struct headers {
    ethernet_t ethernet;
}
// ...

// Parser to extract ethernet header, switch is working on data link layer/layer 2
parser MyParser(packet_in pkt, out headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    state start {
        pkt.extract(hdr.ethernet);
        transition accept;
    }
}

// need to deparse (i.e., serialize) extracted data and added headers (CPU header) to prepend them to outgoing packet
control MyDeparser(packet_out pkt, in headers hdr) {
    apply {
        pkt.emit(hdr.ethernet);
    }
}
```

- `extract` takes 48 + 48 + 16 bits (14 bytes) from the beginning of the packet
- Be sure to deparse all previously parsed and extracted or modified header data in egress

---

## Naive Layer 2 Forwarding

Can we use the extracted header fields afterwards directly to do the following?

```p4
if (hdr.ethernet.dstAddr == 1) { std_meta.egress_spec = 1; }
if (hdr.ethernet.dstAddr == 2) { std_meta.egress_spec = 2; }
```

That's possible and not as dumb as the repeater… but what about additional hosts? Where to send the broadcast destination? Better use a MAC address table for match-action…

---

## Ingress: MAC Address Table (Match-Action)

```p4
control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    // action to forward packet to egress port
    action forward(bit<9> egress_port) {
        std_meta.egress_spec = egress_port;
    }

    // action to broadcast packet (e.g., when destination MAC address is unknown or broadcast/multicast address)
    action broadcast() {
        std_meta.mcast_grp = 1;
    }

    // MAC address table, if destination mac address match, specified action will be applied
    table dstMacAddr {
        key = { hdr.ethernet.dstAddr: exact; }
        actions = { forward; broadcast; }
        size = 4096;
        default_action = broadcast;
    }

    apply { dstMacAddr.apply(); }
}
```

Table can hold, e.g.:

| Key | Action | Action parameter |
|---|---|---|
| 00:00:00:00:00:01 | forward | 1 |
| (default) | broadcast |  |

Action `forward` is called like a function, getting `egress_port` as parameter. Action `broadcast` sets the multicast group in standard metadata of the switch (V1Model broadcast support).

---

## Egress: Preventing Broadcast Loops

```p4
// filter broadcasts going out on the port they came in
control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    apply {
        // if packet is going to a multicast group (i.e., is a broadcast or multicast)
        if (std_meta.mcast_grp == 1) {
            // if egress port is the same as the ingress port
            if (std_meta.egress_port == std_meta.ingress_port) {
                mark_to_drop(std_meta);
            }
        }
    }
}
```

We need to make sure that broadcasts only go out to "all other ports" and not the one they were received on (otherwise we produce a loop). Hence drop broadcasts if they are about to go out on the port they came in from.

---

## Runtime CLI: Filling the MAC Address Table

- We need to add entries to fill the table during runtime (otherwise after initial start tables will be empty) → P4 code only specifies data plane logic, runtime is handled by P4Runtime in the Control Plane
- Can use an API (e.g., Python, gRPC) or a CLI of the switch

```text
p4@p4:~/ProNA$ simple_switch_CLI --thrift-port 9090
Obtaining JSON from switch...
Done
Control utility for runtime P4 table manipulation

RuntimeCmd: show_tables
MyIngress.dstMacAddr           [implementation=None, mk=ethernet.dstAddr(exact, 48)]

RuntimeCmd: help table_add
Add entry to a match table: table_add <table name> <action name> <match fields> => <action parameters> [priority]

RuntimeCmd: table_add MyIngress.dstMacAddr forward 0x00000a000001 => 1
Adding entry to exact match table MyIngress.dstMacAddr
match key:           EXACT-00:00:0a:00:00:01
action:              forward
runtime data:        00:01
Entry has been added with handle 0

RuntimeCmd: table_add MyIngress.dstMacAddr forward 0x00000a000002 => 2
Adding entry to exact match table MyIngress.dstMacAddr
match key:           EXACT-00:00:0a:00:00:02
action:              forward
runtime data:        00:02
Entry has been added with handle 1
```

---

## Runtime CLI: Multicast Group for Broadcasts

- Need to create multicast group 1 (`std_meta.mcast_grp = 1`); by default the switch does not know which ports should belong to the same broadcast domain (e.g., VLAN)
- Create a node 0, add all ports (1, 2) to it, and associate node 0 to multicast group 1
- …after adding this multicast group, we could even delete all entries in table `dstMacAddr`, as unknown MAC addresses (not having an entry in the table) will default to broadcast

```text
RuntimeCmd: mc_mgrp_create 1
Creating multicast group 1

RuntimeCmd: mc_node_create 0 1 2
Creating node with rid 0, port map 110 and lag map
node was created with handle 0

RuntimeCmd: mc_node_associate 1 0
Associating node 0 to multicast group 1

RuntimeCmd: table_delete MyIngress.dstMacAddr 1
Deleting entry 1 from MyIngress.dstMacAddr

RuntimeCmd: table_delete MyIngress.dstMacAddr 0
Deleting entry 0 from MyIngress.dstMacAddr
```

"h1 ping h2" will work… and we created a static Layer 2 switch. How can we implement dynamic MAC address learning (also known as "flooding and filtering")?

---

## Ingress: Learning Source MAC Addresses

```p4
// extend basic forwarding logic to include learning of MAC addresses and achieve flood & filter
control MyIngress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    // action to learn source MAC address, copy ingress_port to be available in egress, clone packet to CPU port (ingress to egress)
    action learnSrcMacAddr() {
        meta.ingressPort = std_meta.ingress_port;
        clone3(CloneType.I2E, MIRROR_SESSION_ID, meta);
    }

    // source MAC address table, if source MAC address matches, do nothing, otherwise send MAC address to CPU port to get learned
    table srcMacAddr {
        key = { hdr.ethernet.srcAddr: exact; }
        actions = { learnSrcMacAddr; NoAction; }
        size = TABLE_SIZE_L2_FORWARDING;
        default_action = learnSrcMacAddr;
    }

    // destination MAC address table, if destination mac address matches, specified action will be applied
    table dstMacAddr {
        key = { hdr.ethernet.dstAddr: exact; }
        actions = { forward; broadcast; }
        size = TABLE_SIZE_L2_FORWARDING;
        default_action = broadcast;
    }

    apply {
        srcMacAddr.apply();
        dstMacAddr.apply();
    }
}
```

Idea: if incoming source MAC address is already in the table, do nothing (`NoAction`); if not, learn it by cloning the packet from ingress to egress (I2E) and sending it to the CPU port (using a port mirror in the switch).

---

## CPU Header and Egress: Sending Learn Events to the Control Plane

```p4
// cpu header prepended to packets going to the CPU, containing source MAC address to learn and ingress port
header cpu_t {
    bit<48> srcAddr;
    bit<16> ingressPort;
}

// we need metadata now, that will carry over a value from ingress to egress
struct metadata {
    bit<9> ingressPort;
}

// send cloned packets to CPU/control plane
control MyEgress(inout headers hdr, inout metadata meta, inout standard_metadata_t std_meta) {
    apply {
        if (std_meta.instance_type == 1) { // if packet was cloned (instance_type == 1): populate cpu header
            hdr.cpu.setValid();
            hdr.cpu.srcAddr = hdr.ethernet.srcAddr;
            hdr.cpu.ingressPort = (bit<16>) meta.ingressPort;
            hdr.ethernet.etherType = L2_LEARN_ETHER_TYPE; // set ether_type to custom value defined for our app
            truncate((bit<32>) 22); // get only start of packet - Ethernet (14 bytes) + CPU Header (8 bytes)
        }
    }
}

// need to deparse (i.e., serialize) extracted data and added headers (CPU header) to prepend them to outgoing packet
control MyDeparser(packet_out pkt, in headers hdr) {
    apply {
        pkt.emit(hdr.ethernet);
        pkt.emit(hdr.cpu);
    }
}
```

Use a custom CPU header added to packets sent to the controller via CPU port (containing MAC address to learn + ingress port) — remember "programming protocol-independent packet processors": the CPU header is a "new protocol" that we just invented and taught our switch ;-)

---

## Control Plane App (Python, P4Runtime)

```python
from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import SimpleSwitchAPI
from scapy.all import Ether, sniff, Packet, BitField

L2_LEARN_ETHER_TYPE = 0x4221
MIRROR_SESSION_ID = 99

class CpuHeader(Packet):
    name = 'CpuPacket'
    fields_desc = [BitField('macAddr', 0, 48), BitField('ingressPort', 0, 16)]

class LearningSwitchControllerApp(object):
    def __init__(self, switchName): ...
    def init(self): ...
    def add_mirror(self): ...
    def add_mcast_grp(self): ...
    def learn(self, learningData): ...
    def recv_msg_cpu(self, pkt): ...
    def run_cpu_port_loop(self): ...

if __name__ == "__main__":
    import sys
    switchName = sys.argv[1]
    controller = LearningSwitchControllerApp(switchName).run_cpu_port_loop()
```

- Implementation of a Python App on the Control Plane using P4Runtime
- Uses the Switch API to execute RuntimeCmds (which we did manually before), configuring table entries, multicast groups and mirror sessions during runtime
- Uses scapy to sniff on the CPU port and use received packets (using the defined CPU header) to learn new MAC addresses and insert them in the tables

---

## Controller App: Initialization

```python
class LearningSwitchControllerApp(object):
    def __init__(self, switchName):
        self.topo = Topology(db="topology.db")
        self.switchName = switchName
        self.thrift_port = self.topo.get_thrift_port(switchName)
        self.cpu_port = self.topo.get_cpu_port_index(self.switchName)
        self.controller = SimpleSwitchAPI(self.thrift_port)
        self.init()

    def init(self):
        self.controller.reset_state()
        self.add_mcast_grp()
        self.add_mirror()
```

Upon initialization of the `LearningSwitchControllerApp` class, establish a connection to the switch in the running topology (uses `p4-utils` of nsg-ethz), add mcast groups to the switch, and add a mirror session (to mirror packets to the CPU port) to the switch.

---

## Controller App: Multicast Group & Mirror Session

```python
def add_mcast_grp(self):
    interfaces_to_port = self.topo[self.switchName]["interfaces_to_port"].copy()
    # filter lo and cpu port
    interfaces_to_port.pop('lo', None)
    interfaces_to_port.pop(self.topo.get_cpu_port_intf(self.switchName), None)
    mc_grp_id = 1
    rid = 0
    # add multicast group
    self.controller.mc_mgrp_create(mc_grp_id)
    port_list = interfaces_to_port.values()[:]
    # add multicast node group
    handle = self.controller.mc_node_create(rid, port_list)
    # associate with mc grp
    self.controller.mc_node_associate(mc_grp_id, handle)

def add_mirror(self):
    if self.cpu_port:
        self.controller.mirroring_add(MIRROR_SESSION_ID, self.cpu_port)
```

Add mcast groups to the switch using the API — this is what we did manually before using `mc_mgrp_create`, `mc_node_create` and `mc_node_associate` (mirror session could also be done manually via the CLI).

---

## Controller App: Learning Loop

```python
def learn(self, learningData):
    for macAddr, ingressPort in learningData:
        print "macAddr: %012X ingressPort: %s" % (macAddr, ingressPort)
        self.controller.table_add("srcMacAddr", "NoAction", [str(macAddr)])
        self.controller.table_add("dstMacAddr", "forward", [str(macAddr)], [str(ingressPort)])

def recv_msg_cpu(self, pkt):
    packet = Ether(str(pkt))
    if packet.type == L2_LEARN_ETHER_TYPE:
        cpu_header = CpuHeader(bytes(packet.payload))
        self.learn([(cpu_header.macAddr, cpu_header.ingressPort)])

def run_cpu_port_loop(self):
    cpu_port_intf = str(self.topo.get_cpu_port_intf(self.switchName).replace("eth0", "eth1"))
    sniff(iface=cpu_port_intf, prn=self.recv_msg_cpu)
```

Continuously sniff for packets on the CPU port interface and treat received packets as information to learn about new MAC addresses on ingress ports; add learned MAC addresses and their ports using the switch API's `table_add`.
