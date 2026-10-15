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

    # Flow 1: ARP Request H1 -> H2
    flow1_match = ofp_parser.OFPMatch(in_port=0,
                                      dl_type=0x0000,
                                      dl_src='aa:bb:cc:dd:ee:ff',
                                      dl_dst='ff:ee:dd:cc:bb:aa',
                                      nw_src='1.2.3.4',
                                      nw_dst='4.3.2.1')

    flow1_actions = [ofp_parser.OFPActionOutput(port=0)]
    # flow1_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow1_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow1_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow1_actions)
    
    ofp_datapath.send_msg(flow1_mod)

    # Flow 2: ARP Reply H1 -> H2
    flow2_match = ofp_parser.OFPMatch(in_port=0,
                                      dl_type=0x0000,
                                      dl_src='aa:bb:cc:dd:ee:ff',
                                      dl_dst='ff:ee:dd:cc:bb:aa',
                                      nw_src='1.2.3.4',
                                      nw_dst='4.3.2.1')

    flow2_actions = [ofp_parser.OFPActionOutput(port=0)]
    # flow2_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow2_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow2_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow2_actions)

    ofp_datapath.send_msg(flow2_mod)
    
    # Flow 3: IP H1 -> H2
    flow3_match = ofp_parser.OFPMatch(in_port=0,
                                      dl_type=0x0000,
                                      dl_src='aa:bb:cc:dd:ee:ff',
                                      dl_dst='ff:ee:dd:cc:bb:aa',
                                      nw_src='1.2.3.4',
                                      nw_dst='4.3.2.1')

    flow3_actions = [ofp_parser.OFPActionOutput(port=0)]
    # flow3_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]

    flow3_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow3_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow3_actions)

    ofp_datapath.send_msg(flow3_mod)

    # Flow 4: ARP Request H2 -> H1
    flow4_match = ofp_parser.OFPMatch(in_port=0,
                                      dl_type=0x0000,
                                      dl_src='ff:ee:dd:cc:bb:aa',
                                      dl_dst='aa:bb:cc:dd:ee:ff',
                                      nw_src='4.3.2.1',
                                      nw_dst='1.2.3.4')    

    flow4_actions = [ofp_parser.OFPActionOutput(port=0)]
    # flow4_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]    

    flow4_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow4_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow4_actions)

    ofp_datapath.send_msg(flow4_mod)
    
    # Flow 5: ARP Reply H2 -> H1
    flow5_match = ofp_parser.OFPMatch(in_port=0,
                                      dl_type=0x0000,
                                      dl_src='ff:ee:dd:cc:bb:aa',
                                      dl_dst='aa:bb:cc:dd:ee:ff',
                                      nw_src='4.3.2.1',
                                      nw_dst='1.2.3.4')   

    flow5_actions = [ofp_parser.OFPActionOutput(port=0)]
    # flow5_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]    

    flow5_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow5_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow5_actions)    

    ofp_datapath.send_msg(flow5_mod)
    
    # Flow 6: IP H2 -> H1
    flow6_match = ofp_parser.OFPMatch(in_port=0,
                                      dl_type=0x0000,
                                      dl_src='ff:ee:dd:cc:bb:aa',
                                      dl_dst='aa:bb:cc:dd:ee:ff',
                                      nw_src='4.3.2.1',
                                      nw_dst='1.2.3.4')
    
    flow6_actions = [ofp_parser.OFPActionOutput(port=0)]
    # flow6_actions = [ofp_parser.OFPActionOutput(ofp_protocol.OFPP_FLOOD)]    

    flow6_mod = ofp_parser.OFPFlowMod(datapath=ofp_datapath,
                                      match=flow6_match,
                                      command=ofp_protocol.OFPFC_ADD,
                                      actions=flow6_actions)
    
    ofp_datapath.send_msg(flow6_mod)