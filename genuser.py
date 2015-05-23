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

# Add a generic user
user = User(email=email, password=hashed, password_salt=salt, organisation=None, is_admin=True)
session.add(user)

# Add CIHPress as an organisation for a user to belong to
cih = session.query(UserOrganisation).filter_by(name='CIHPress').first()
if cih is None:
    cih = UserOrganisation(name='CIHPress')
    session.add(cih)

# Add CCDHRN as an organisation for a user to belong to
ccd = session.query(UserOrganisation).filter_by(name='CCDHRN').first()
if ccd is None:
    ccd = UserOrganisation(name='CCDHRN')
    session.add(ccd)

# Add users belonging to either organisation
u1e = 'user1@user1.com'
u2e = 'user2@user2.com'
u1 = User(email=u1e, password=hashed, password_salt=salt, organisation=cih, is_admin=True)
u2 = User(email=u2e, password=hashed, password_salt=salt, organisation=ccd, is_admin=True)
session.add(u1)
session.add(u2)

session.commit()

print 'Created admin ' + email + ' / ' + pwd
print 'Created CIHPress member ' + u1e + ' / ' + pwd
print 'Created CCDHRN member ' + u2e + ' / ' + pwd
