from simpledb import *


while True:
    n = raw_input("shortname (or 'q' to quit) ")
    standard_n = n.lower()
    if standard_n == 'q':
        break
    user_object = session.query(User).filter_by(name=standard_n).first()
    if user_object is None:
        print "New user with shortname", standard_n
        f = raw_input("Full name ")
        p = raw_input("Password (or 'q' to quit) ")
        if p.lower() == 'q':
            break
        if not p:
            print "Empty passwords fields are not allowed."
        else:
            new_user = User(standard_n, f, p)
            print "Adding %s to db..." % str(new_user)
            session.add(new_user)
            session.commit()
    else:
        print "Updating user:", str(user_object)
        p = raw_input("Password (or 'q' to quit) ")
        if p.lower() == 'q':
            break
        if not p:
            print "Empty passwords fields are not allowed."
        else:
            user_object.password = p
            session.commit()
