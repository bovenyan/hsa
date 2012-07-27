'''
    Copyright 2012, Stanford University. This file is licensed under GPL v2 plus
    a special exception, as described in included LICENSE_EXCEPTION.txt.
    
Created on Jul 25, 2012

@author: Peyman Kazemian
'''
from examples.emulated_tf import emulated_tf
from headerspace.tf import TF

def load_network(settings):
  n = net_loader(settings)
  ntf = n.load_ntf()
  ttf = n.load_ttf()
  (name_to_id,id_to_name) = n.load_port_map()
  return (ntf,ttf,name_to_id,id_to_name)


class net_loader(object):

  def __init__(self,settings):
    '''
    @settings has the following key value pairs
    @required rtr_names: list of router names
    @required num_layers
    @required fwd_engine_layer
    @required input_path: path of tf files 
    @required switch_id_multipliert 
    @required port_type_multiplier
    @required out_port_type_const
    @optional remove_duplicates: True of False - if duplicates sshould be 
    removed after each step. (def: False)
    '''
    self.settings = settings

  def load_ntf(self):
    '''
    load transfer functions into a emulated transfer function with @layer layers.
    '''
    if "remove_duplicates" in self.settings.keys() and \
      self.settings["remove_duplicates"]:
      emul_tf = emulated_tf(self.settings["num_layers"],True)
    else:
      emul_tf = emulated_tf(self.settings["num_layers"],False)
      
    emul_tf.set_fwd_engine_stage(self.settings["fwd_engine_layer"])
    
    emul_tf.set_multipliers(self.settings["switch_id_multiplier"], \
                            self.settings["port_type_multiplier"], \
                            self.settings["out_port_type_const"])
    
    for rtr_name in self.settings["rtr_names"]:
      f = TF(1)
      f.load_object_from_file("%s/%s.tf"%(self.settings["input_path"],
                                          rtr_name))
      if "hash_table" in self.settings.keys():
        f.activate_hash_table(self.settings["hash_table"])
      emul_tf.append_tf(f)
    emul_tf.length = f.length
    return emul_tf
  
  def load_ttf(self):
    '''
    loads topology transfer function
    '''
    f = TF(1)
    f.load_object_from_file("%s/topology.tf"%self.settings["input_path"])
    return f
  
  def load_port_map(self):
    '''
    load the map from port ID to name of box-port name.
    '''
    f = open("%s/port_map.txt"%self.settings["input_path"],'r')
    id_to_name = {}
    map = {}
    rtr = ""
    for line in f:
      if line.startswith("$"):
        rtr = line[1:].strip()
        map[rtr] = {}
      elif line != "":
        tokens = line.strip().split(":")
        map[rtr][tokens[0]] = int(tokens[1])
        id_to_name[tokens[1]] = "%s-%s"%(rtr,tokens[0])
        if "out_port_type_const" in self.settings.keys() and \
          self.settings["out_port_type_const"] > 0:
          out_port = int(tokens[1]) + self.settings["port_type_multiplier"]\
          * self.settings["out_port_type_const"]
          id_to_name["%s"%out_port] = "%s-%s"%(rtr,tokens[0])
    return (map,id_to_name)