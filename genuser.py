'''A utility script for automatically generating an admin user to be inserted into
the database after the DB has been wiped clean.
Registers the email "demo@demo.com" with password "demo".
'''

from rvd.models import *
import bcrypt

email = 'demo@demo.com'
pwd = 'demo'
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(pwd, salt)

user = User(id=1, email=email, password=hashed, password_salt=salt, organisation=None, is_admin=True)
session.add(user)
session.commit()

print 'Created admin ' + email + ' / ' + pwd
