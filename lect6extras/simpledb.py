#!/usr/bin/env python
# slightly modified code, taken from http://www.sqlalchemy.org/docs/ormtutorial.html

# Voodoo for connecting to a database - lots of rdbms are supported. Sqlite is not optimal, but it comes with python
from sqlalchemy import create_engine
engine = create_engine('sqlite:////Users/mholder/Desktop/programming/programming/lect6extras/test.db')


# sqlalchemy provides python classes for modelling DB tables.
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData()
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('fullname', String),
                    Column('password', String))
metadata.create_all(engine)


# Now we can create a Python class that has the data that is appropriate:
class User(object):
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)


# We want to set up an "obect relational map" between our python datamodel
#   (the class User) and the corresponding db table (users_table).

from sqlalchemy.orm import mapper
mapper(User, users_table)


# To preserve the integrity of a database, we interact with a DB through a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()



