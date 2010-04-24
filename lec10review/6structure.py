#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent.parse.pdb import PDBParser
from cogent.format.pdb import PDBWriter
import tempfile, os
pdb_file = open('data/4TSV.pdb')
new_structure = PDBParser(pdb_file)
open_handle, file_name = tempfile.mkstemp()
os.close(open_handle)
new_pdb_file = open(file_name,'wb')
PDBWriter(new_pdb_file, new_structure)
print structure.id 
print structure.getId() 
print structure.getFull_id() 
print structure.header.keys()
print structure.header['id'] 
print structure.header['expdta'] 
structure.items()
structure.values()
structure.keys()
first_model = structure.values()[0]
first_model_id = first_model.getId()
structure.getChildren()
children_list = structure.getChildren([first_model_id])
some_model = structure.values()[0]
some_chain = some_model.values()[0]
for residue in some_chain.values():
    residue.setName('UNK')
print sorted(structure.table.keys()) 
print structure.table['C']
            
