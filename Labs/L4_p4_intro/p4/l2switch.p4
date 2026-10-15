/* ACN Lab L4 — Beispiel 2: Minimalistischer Layer-2-Switch
 *
 * Weiterleitung über eine Tabelle mit exakten MAC-Adressen (kein MAC-Learning —
 * das macht erst Beispiel 3). Unbekannte Ziele werden gedroppt; Broadcast/Multicast
 * läuft über eine Multicast-Gruppe, die per simple_switch_CLI angelegt wird.
 *
 * Die Tabelle wird per simple_switch_CLI befüllt, z. B. (Reihenfolge wichtig):
 *   mc_mgrp_create 1                                  # Multicast-Gruppe anlegen
 *   mc_node_create 0 1 2                              # Node mit Ports 1 und 2 (dezimal!)
 *   mc_node_associate 1 0                             # Node in Gruppe 1 hängen
 *   table_add forwarding broadcast ff:ff:ff:ff:ff:ff =>   # Broadcast -> Gruppe
 *   table_add forwarding forward <mac-h1> => 1
 *   table_add forwarding forward <mac-h2> => 2
 * Hinweise: parameterlose Aktionen brauchen "=>" mit leerer Argumentliste;
 * bmv2 verwirft Replikate, deren Ausgangsport der Ingress-Port ist (kein Echo).
 */
#include <core.p4>
#include <v1model.p4>

typedef bit<48> macAddr_t;

header ethernet_h {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

struct headers {
    ethernet_h ethernet;
}

struct metadata {
}

parser ParserI(packet_in packet,
               out headers hdr,
               inout metadata meta,
               inout standard_metadata_t standard_metadata) {

    state start {
        packet.extract(hdr.ethernet);
        transition accept;
    }
}

control MyVerifyChecksum(inout headers hdr,
                         inout metadata meta) {
    apply { }
}

control IngressI(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {

    action forward(bit<9> port) {
        standard_metadata.egress_spec = port;
    }

    action broadcast() {
        // Multicast-Gruppe 1: repliziert zu allen Ports des Nodes (per CLI angelegt).
        // bmv2 verwirft Replikate auf dem Ingress-Port — der Absender bekommt sein
        // eigenes Paket nicht zurück.
        standard_metadata.mcast_grp = 1;
    }

    action drop() {
        mark_to_drop(standard_metadata);
    }

    table forwarding {
        key = {
            hdr.ethernet.dstAddr : exact;
        }
        actions = {
            forward;
            broadcast;
            drop;
        }
        default_action = drop();
        size = 1024;
    }

    apply {
        if (hdr.ethernet.isValid()) {
            forwarding.apply();
        }
    }
}

control EgressI(inout headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {
    apply { }
}

control MyComputeChecksum(inout headers hdr,
                          inout metadata meta) {
    apply { }
}

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
    }
}

V1Switch(ParserI(), MyVerifyChecksum(), IngressI(), EgressI(),
         MyComputeChecksum(), MyDeparser()) main;
