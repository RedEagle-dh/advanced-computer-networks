/* ACN Lab L4 — Beispiel 1: Repeater
 *
 * Leitet jedes Paket an den jeweils anderen Port weiter (Port 1 <-> Port 2).
 * Zeigt die P4-Grundstruktur: Parser -> Ingress -> Deparser (v1model).
 * Keine Tabellen — das Programm verhält sich immer gleich.
 */
#include <core.p4>
#include <v1model.p4>

const bit<9> PORT1  = 1;
const bit<9> PORT2  = 2;

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

    apply {
        // jede Richtung wird gespiegelt: 1 -> 2, 2 -> 1
        standard_metadata.egress_spec =
            standard_metadata.ingress_port == PORT1 ? PORT2 : PORT1;
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
