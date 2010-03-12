from simpledb import *


while True:
    n = raw_input("shortname (or 'q' to quit) ")
    if n.lower() == 'q':
        break
    f = raw_input("Full name ")
    p = raw_input("Password (or 'q' to quit) ")
    if p.lower() == 'q':
        break
    if not p:
        print "Empty passwords fields are not allowed."
    else:
        new_user = User(n.lower(), f, p)
        print "Adding %s to db..." % str(new_user)
        session.add(new_user)
        session.commit()
