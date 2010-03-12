from simpledb import *
import sys

u = session.query(User).filter_by(name=sys.argv[1].lower())
print u.first()
