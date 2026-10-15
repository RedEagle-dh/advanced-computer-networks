from os_ken.base import app_manager 
from os_ken.ofproto import ofproto_v1_0
from os_ken.lib import dpid as dpid_lib
from os_ken.controller import dpset
import threading


class OpenFlowApp(app_manager.OSKenApp):
  
  OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
  
  _DATAPATH_ID = '0000000000000001'
  
  _CONTEXTS = {
    'dpset': dpset.DPSet,
  }  
  
  def __init__(self, *args, **kwargs):
    super(OpenFlowApp, self).__init__(*args, **kwargs)

    self._dpset = kwargs['dpset']

    threading.Timer(10.0, self._add_flows).start()

  def _add_flows(self):

    ofp_datapath = self._dpset.get(dpid_lib.str_to_dpid(self._DATAPATH_ID)) 
    ofp_protocol = ofp_datapath.ofproto
    ofp_parser = ofp_datapath.ofproto_parser

    self.logger.info("add flows: [dp=%s]", dpid_lib.dpid_to_str(ofp_datapath.id))

    # Flow 1: all from port 1
    flow1_match = ofp_parser.OFPMatch(in_port=1)
    flow1_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow1_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow1_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow1_actions)
    
    ofp_datapath.send_msg(flow1_mod)

    # Flow 2: all from port 2
    flow2_match = ofp_parser.OFPMatch(in_port=2)
    #flow2_actions = [ofp_parser.OFPActionOutput(port=1)]
    #flow2_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow2_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow2_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow1_actions)
    
    ofp_datapath.send_msg(flow2_mod)
