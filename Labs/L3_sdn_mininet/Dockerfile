# ACN Lab L3 — SDN/OpenFlow mit Mininet: BYOD-Container (ersetzt die learn-sdn-hub-VM)
#
# Ubuntu 24.04 + Mininet + Open vSwitch + os-ken (aktive Ryu-Gabelung von OpenStack;
# Ryu selbst ist seit 04/2024 ohne Commits). Läuft als containerlab-Knoten (privileged):
#
#   docker build -t acn-l3-mininet:2026.10 .
#   Smoke:  docker run --rm --privileged acn-l3-mininet:2026.10 mn --test pingall
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      mininet openvswitch-switch iproute2 iputils-ping net-tools tcpdump \
      iperf3 python3-pip less vim-tiny && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --break-system-packages os-ken tinyrpc && \
    mn --version && ovs-vsctl --version | head -1 && \
    echo 'service() { /usr/share/openvswitch/scripts/ovs-ctl start; }' >/etc/profile.d/ovs.sh

CMD ["sleep", "infinity"]

# Stolperfalle: os-ken-Wheels (4.2.2) enthalten KEIN os_ken/cmd (Manager) und kein
# app/wsgi — beide kommen hier portiert aus ryu 4.34 (Module umbenannt ryu -> os_ken).
# osken-manager ersetzt den klassischen ryu-manager; default_port 6633 wie im alten Lab.
COPY osken_patch/os_ken/cmd/ /usr/local/lib/python3.12/dist-packages/os_ken/cmd/
COPY osken_patch/osken-manager /usr/local/bin/osken-manager
RUN chmod +x /usr/local/bin/osken-manager && osken-manager --version
