from mininet.topo import Topo
from mininet.node import Node
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCIntf
from mininet.node import RemoteController


class CustomTopo(Topo):

  __LINK_BANDWIDTH = 1

  def __init__(self):
      Topo.__init__(self)

  def build(self):

    sw = self.addSwitch('ofp-sw1', dpid='0000000000000001')
        
    h1 = self.addHost('h1', ip='10.0.0.1/24', mac='ba:de:af:fe:00:01')
    
    h2 = self.addHost('h2', ip='10.0.0.2/24', mac='ba:de:af:fe:00:02')
    
    for node1, node2 in [(h1, sw), (h2, sw)]: 
      self.addLink(node1, node2,
                   cls1=TCIntf, cls2=TCIntf,
                   intfName1=node1 + '-' + node2,
                   intfName2=node2 + '-' + node1,
                   params1={'bw': self.__LINK_BANDWIDTH},
                   params2={'bw': self.__LINK_BANDWIDTH})


def run():
  topo = CustomTopo()
  net = Mininet(topo=topo,
                controller=RemoteController('ofp-c1',
                                            ip='127.0.0.1',
                                            port=6633))
  net.start()
  CLI(net)    
  net.stop()


if __name__ == '__main__':
  run()
