# ACN Lab L4 — P4-Node-Image: Compiler + bmv2-Runtime in einem Image
#
# Basis sind die offiziell gepflegten p4lang-Images (Stand 2026-10):
#   p4lang/p4c:latest              -> p4c 1.2.5.18 (statisch gelinkt, monatliche Tags)
#   p4lang/behavioral-model:latest -> simple_switch/simple_switch_CLI/simple_switch_grpc
#                                     (bmv2 1.15.7, Ubuntu 24.04 — identische Basis wie p4c-Image)
# Der alte prona/p4-container (4,3 GB, p4c 1.2.3.6, OVS + learn-sdn-hub-Ballast) wird
# nicht weiter gepflegt (upstream: letzter Commit 11/2022) — dieses Image ersetzt ihn.
#
# Build:     docker build -t acn-l4-p4:2026.10 .
# Kontrolle: docker run --rm acn-l4-p4:2026.10 sh -c 'p4c --version && simple_switch --version'

FROM p4lang/behavioral-model:latest AS bmv2
FROM p4lang/p4c:latest

COPY --from=bmv2 /usr/local/bin/simple_switch      /usr/local/bin/
COPY --from=bmv2 /usr/local/bin/simple_switch_CLI  /usr/local/bin/
COPY --from=bmv2 /usr/local/bin/simple_switch_grpc /usr/local/bin/
# Runtime-Libs der bmv2-Binaries (nanomsg, thrift, pi/p4runtime, sysrepo, yang);
# p4c ist statisch gelinkt, /usr/local/lib kollidiert daher nicht
COPY --from=bmv2 /usr/local/lib/                   /usr/local/lib/

RUN ldconfig && \
    p4c --version && simple_switch --version && simple_switch_CLI --help >/dev/null

# Ausbaustufe (Beispiel 3): P4Runtime-Shell für die controller-gestützte Variante
# (Aufruf: python3 -m p4runtime_sh; Modul p4runtime_sh, Paket p4runtime-shell 0.0.6)
RUN pip install --break-system-packages p4runtime-shell && \
    python3 -c "import p4runtime_sh; print('p4runtime-shell OK')"

# containerlab linux-Knoten brauchen einen dauerhaft laufenden PID 1
CMD ["sleep", "infinity"]
