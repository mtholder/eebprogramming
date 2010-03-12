from simpledb import *


ed_user = User('ed', 'Ed Wiley', 'fi5he5')

session.add(ed_user)
session.commit()
