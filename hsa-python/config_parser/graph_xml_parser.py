'''
Created on Jul 25, 2012

@author: Peyman Kazemian
'''

from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from HTMLParser import HTMLParser
from config_parser.cisco_router_parser import cisco_router

class graph_xml(object):
  
  def __init__(self):
    self.graph_xml_namespace = "http://graphml.graphdrawing.org/xmlns"
    self.undirected = True
    self.edges = {}
    self.links = {}
    self.nodes = {}
    self.port_name_translator = cisco_router.get_ethernet_port_name
    pass
  
  def _create_elem_tree(self,filename):
    f = open(filename,'r')
    h = HTMLParser()
    unescaped = h.unescape(f.read())
    f.close()
    tree = ElementTree()
    tree.parse(StringIO(unescaped))
    return tree
     
  def read_nodes_xml(self,filename):
    tree = self._create_elem_tree(filename)
    nodes = tree.findall("data/nodeDetails/node")
    for node in nodes:
      node_id = node.attrib["id"]
      node_name = node.find("name").text
      self.nodes[node_id] = node_name

  def read_graphs_xml(self,filename):
    tree = self._create_elem_tree(filename)
    graph = tree.find("data/{%s}graphml/{%s}graph"%(\
                       self.graph_xml_namespace,\
                       self.graph_xml_namespace))
    if graph.attrib.has_key("edgedefault"):
      if graph.attrib["edgedefault"] == "undirected":
        self.undirected = True
      else:
        self.undirected = False
    edges = tree.findall("data/{%s}graphml/{%s}graph/{%s}edge"%(\
                       self.graph_xml_namespace,\
                       self.graph_xml_namespace,\
                       self.graph_xml_namespace))
    for edge in edges:
      edge_id = edge.attrib["id"]
      src_id = edge.attrib["source"]
      target_id = edge.attrib["target"]
      self.edges[edge_id] = (src_id,target_id)
    
  def read_links_xml(self,filename):
    tree = self._create_elem_tree(filename)
    links = tree.findall("data/linkDetails/link")
    for link in links:
      link_id = link.attrib["id"]
      src_port = self.port_name_translator(link.find("srcPort/name").text)
      dst_port = self.port_name_translator(link.find("destPort/name").text)
      self.links[link_id] = (src_port,dst_port)
      
  def generate_topology_list(self):
    result = []
    for edge_id in self.edges.keys():
      (src_id,dst_id) = self.edges[edge_id]
      src_name = self.nodes[src_id]
      dst_name = self.nodes[dst_id]
      (src_port,dst_port) = self.links[edge_id]
      result.append((src_name,src_port,dst_name,dst_port))
    return result
