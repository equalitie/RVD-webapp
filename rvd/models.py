from flask_babel import lazy_gettext as ___
import sqlalchemy as sa
from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from instance import config
from flask_login import UserMixin

engine = create_engine(
    'mysql://{}:{}@{}/{}?charset=utf8'.format(config.DB_USER, config.DB_PASS, config.DB_HOST, config.DB_NAME)
)
Base = declarative_base(engine)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


##################
## Action Model ##
##################

# Association tables

action_state = Table('action_state-authority', Base.metadata,
                     sa.Column('action_id', sa.BigInteger, ForeignKey('actions.id')),
                     sa.Column('state_authority_id', sa.BigInteger, ForeignKey('stateauthorities.id')))

action_international = Table('action_international-authority', Base.metadata,
                             sa.Column('action_id', sa.BigInteger, ForeignKey('actions.id')),
                             sa.Column('international_authority_id', sa.BigInteger,
                                       ForeignKey('internationalauthorities.id')))

action_event = Table('action_event', Base.metadata,
                     sa.Column('action_id', sa.BigInteger, ForeignKey('actions.id')),
                     sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')))


class Action(Base):
    __tablename__ = 'actions'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    complaint_to_state_authority = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Complaint to state authority'), 'label': ___('Complaint to state authority')})
    response_from_state_authority = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Response from state authority'), 'label': ___('Response from state authority')})
    complaint_to_international_authority = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Complaint to international authority'),
        'label': ___('Complaint to international authority')})
    response_from_international_authority = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Response from international authority')})
    state_bodies_approached = relationship('StateAuthority', secondary=action_state, backref='actions')
    international_bodies_approached = relationship(
        'InternationalAuthority', secondary=action_international, backref='actions')
    events = relationship('Event', secondary=action_event, backref='actions')


#################
## Actor Model ##
#################

# Association tables

actor_location = Table('actor_location', Base.metadata,
                       sa.Column('actor_id', sa.BigInteger, ForeignKey('actors.id')),
                       sa.Column('location_id', sa.BigInteger, ForeignKey('locations.id')))

actor_organisation = Table('actor_organisation', Base.metadata,
                           sa.Column('actor_id', sa.BigInteger, ForeignKey('actors.id')),
                           sa.Column('organisation_id', sa.BigInteger, ForeignKey('organisations.id')))

actor_profession = Table('actor_profession', Base.metadata,
                         sa.Column('actor_id', sa.BigInteger, ForeignKey('actors.id')),
                         sa.Column('profession_id', sa.BigInteger, ForeignKey('professions.id')))


class Actor(Base):
    __tablename__ = 'actors'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Name'), 'label': ___('Name')})
    birth_date = sa.Column(sa.Date, nullable=True, info={'description': ___('Date of birth'), 'label': ___('Date of birth')})
    # telephone = sa.Column(PhoneNumberType(), info={
    telephone = sa.Column(sa.Unicode(16), info={
        'description': ___('+1 819 987-6543'), 'label': ___('Phone number')})
    address = sa.Column(sa.Unicode(250), nullable=True, info={'description': ___('Address'), 'label': ___('Address')})
    organisations = relationship('Organisation', secondary=actor_organisation, backref='members')
    professions = relationship('Profession', secondary=actor_profession, backref='practitioners')
    locations = relationship('Location', secondary=actor_location, backref='locals')
    gender = sa.Column(sa.Text, nullable=True, info={'description': ___('Gender'), 'label': ___('Gender')})
    is_activist = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Is activist'), 'label': ___('Is activist')})
    activist_info = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Activist info'), 'label': ___('Activist info')})
    owner_id = sa.Column(sa.BigInteger, ForeignKey('users.id'), nullable=False, default=1)
    owner = relationship('User', backref='actor_owner')
    public = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Public'), 'label': ___('Public')
    }, default=0)


##################
## Report Model ##
##################

class Report(Base):
    __tablename__ = 'reports'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    text = sa.Column(sa.Text, nullable=False, info={
        'description': ___('Content of report'), 'label': ___('Content of report')})
    events = relationship('Event')

#################
## Event Model ##
#################

# Association tables

event_source = Table('event_source', Base.metadata,
                     sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                     sa.Column('source_id', sa.BigInteger, ForeignKey('sources.id')))

event_releasetype = Table('event_release-type', Base.metadata,
                          sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                          sa.Column('release_type_id', sa.BigInteger, ForeignKey('releasetypes.id')))

event_prison = Table('event_prison', Base.metadata,
                     sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                     sa.Column('prison_id', sa.BigInteger, ForeignKey('prisons.id')))

event_location = Table('event_location', Base.metadata,
                       sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                       sa.Column('location_id', sa.BigInteger, ForeignKey('locations.id')))

event_witness = Table('event_witness', Base.metadata,
                      sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                      sa.Column('witness_id', sa.BigInteger, ForeignKey('actors.id')))

event_victim = Table('event_victim', Base.metadata,
                     sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                     sa.Column('victim_id', sa.BigInteger, ForeignKey('actors.id')))

event_perp = Table('event_perpetrator', Base.metadata,
                   sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                   sa.Column('perpetrator_id', sa.BigInteger, ForeignKey('actors.id')))

event_type = Table('event_type', Base.metadata,
                         sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                         sa.Column('event_type_id', sa.BigInteger, ForeignKey('eventtypes.id')))

event_documents = Table('event_document', Base.metadata,
                         sa.Column('event_id', sa.BigInteger, ForeignKey('events.id')),
                         sa.Column('document_id', sa.BigInteger, ForeignKey('documents.id')))


# event_event = Table('event_event', Base.metadata,
#    sa.Column('event1_id', sa.BigInteger, ForeignKey('events.id')),
#    sa.Column('event2_id', sa.BigInteger, ForeignKey('events.id')))

class Event(Base):
    __tablename__ = 'events'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    title = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Title'), 'label': ___('Title')})
    description = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Description'), 'label': ___('Description')})
    charges = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Charges'), 'label': ___('Charges against victim')})
    event_start = sa.Column(sa.DateTime, nullable=True, info={
        'description': ___('YYYY-MM-DD 00:00:00'), 'label': ___('Event start')})
    event_end = sa.Column(sa.DateTime, nullable=True, info={
        'description': ___('YYYY-MM-DD 00:00:00'), 'label': ___('Event end')})
    report_date = sa.Column(sa.Date, nullable=True, info={
        'description': ___('Date of report'), 'label': ___('Date of report')})
    psych_assist = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Psychological assistance provided'),
        'label': ___('Psychological assistance provided')})
    material_assist = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Material assistance provided'),
        'label': ___('Material assistance provided')})
    consequences = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Consequences'), 'label': ___('Consequences')})
    was_activist = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Was an activist'), 'label': ___('Was an activist')})
    victim_is_complainant = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Victim is complainant'), 'label': ___('Victim is complainant')})
    allow_storage = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Allows storage of information'),
        'label': ___('Allows storage of information')})
    allow_publishing = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Allows publishing of information'),
        'label': ___('Allows publishing of information')})
    allow_representation = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Allows legal representation'),
        'label': ___('Allows legal representation')})
    data_is_sensitive = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Data is hyper sensitive'),
        'label': ___('Data is hyper sensitive')})
    report_id = sa.Column(sa.BigInteger, ForeignKey('reports.id'), info={'description': 'report id', 'label': 'report id'})
    report = relationship('Report', backref='event_report')
    release_types = relationship('ReleaseType', secondary=event_releasetype, backref='events')
    locations = relationship('Location', secondary=event_location)
    prisons = relationship('Prison', secondary=event_prison, backref='events')
    sources = relationship('Source', secondary=event_source)
    witnesses = relationship('Actor', secondary=event_witness)
    victims = relationship('Actor', secondary=event_victim)
    perpetrators = relationship('Actor', secondary=event_perp)
    event_types = relationship('EventType', secondary=event_type)
    documents = relationship('Document', secondary=event_documents, backref='events')
    owner_id = sa.Column(sa.BigInteger, ForeignKey('users.id'), nullable=False, default=1)
    owner = relationship('User', backref='event_owner')
    public = sa.Column(sa.Boolean, nullable=True, info={
        'description': ___('Public'), 'label': ___('Public')
    }, default=0)


##################
## EvidenceType ##
##################

class EvidenceType(Base):
    __tablename__ = 'evidencetypes'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    description = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Description'), 'label': ___('Description')})
    event_id = sa.Column(sa.BigInteger, ForeignKey('events.id'))
    event = relationship('Event', backref=backref('evidence_types', order_by=id))


###################################
## International Authority model ##
###################################

class InternationalAuthority(Base):
    __tablename__ = 'internationalauthorities'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    description = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Description'), 'label': ___('Description')})


####################
## Location model ##
####################

class Location(Base):
    __tablename__ = 'locations'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    longitude = sa.Column(sa.Float, nullable=False, info={
        'description': ___('Longitude'), 'label': ___('Longitude')})
    latitude = sa.Column(sa.Float, nullable=False, info={
        'description': ___('Latitude'), 'label': ___('Latitude')})


########################
## Organisation model ##
########################

# Association tables

org_location = Table('organisation_location', Base.metadata,
                     sa.Column('organisation_id', sa.BigInteger, ForeignKey('organisations.id')),
                     sa.Column('location_id', sa.BigInteger, ForeignKey('locations.id')))


class Organisation(Base):
    __tablename__ = 'organisations'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Name'), 'label': ___('Name')})
    description = sa.Column(sa.Text, nullable=True,
                            info={'description': ___('Description'), 'label': ___('Description')})
    locations = relationship('Location', secondary=org_location, backref='organisations')


##################
## Prison model ##
##################

# Association tables

prison_ptype = Table('prison_prison-type', Base.metadata,
                     sa.Column('prison_id', sa.BigInteger, ForeignKey('prisons.id')),
                     sa.Column('prison_type_id', sa.BigInteger, ForeignKey('prisontypes.id')))

prison_location = Table('prison_location', Base.metadata,
                        sa.Column('prison_id', sa.BigInteger, ForeignKey('prisons.id')),
                        sa.Column('location_id', sa.BigInteger, ForeignKey('locations.id')))


class Prison(Base):
    __tablename__ = 'prisons'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    locations = relationship('Location', secondary=prison_location, backref='prisons')
    prison_types = relationship('PrisonType', secondary=prison_ptype, backref='prisons')


#######################
## Prison Type model ##
#######################

class PrisonType(Base):
    __tablename__ = 'prisontypes'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})


######################
## Profession model ##
######################

class Profession(Base):
    __tablename__ = 'professions'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Name'), 'label': ___('Name')})


########################
## Release Type model ##
########################

class ReleaseType(Base):
    __tablename__ = 'releasetypes'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    type_code = sa.Column(sa.BigInteger, nullable=False, info={
        'description': ___('Type code'), 'label': ___('Type code')})


############################
## Rights Violation model ##
############################

class EventType(Base):
    __tablename__ = 'eventtypes'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    description = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Description'), 'label': ___('Description')})

############################
## Rights Violation model ##
############################

class Document(Base):
    __tablename__ = 'documents'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    filename = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('filename'), 'label': ___('Filename')})


##################
## Source model ##
##################

source_org = Table('source_organisation', Base.metadata,
                   sa.Column('source_id', sa.BigInteger, ForeignKey('sources.id')),
                   sa.Column('organisation_id', sa.BigInteger, ForeignKey('organisations.id')))

class Source(Base):
    __tablename__ = 'sources'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    organisations = relationship('Organisation', secondary=source_org, backref='sources')


###########################
## State Authority model ##
###########################

class StateAuthority(Base):
    __tablename__ = 'stateauthorities'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    description = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Description'), 'label': ___('Description')})


#############################
## User Organisation model ##
#############################

class UserOrganisation(Base):
    __tablename__ = 'user_organisations'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Name'), 'label': ___('Name')})


###########
## Users ##
###########
class User(Base, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    email = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Email'), 'label': ___('Email')})
    password = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Password'), 'label': ___('Password')})
    password_salt = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Password salt'), 'label': ___('Password salt')})
    organisation = relationship('UserOrganisation', backref=backref('members', order_by=id))
    organisation_id = sa.Column(sa.BigInteger, ForeignKey('user_organisations.id'), nullable=True)
    is_admin = sa.Column(sa.Boolean, nullable=False, info={'description': ___('Is admin'), 'label': ___('Is admin')})

## Create the database tables ##

Base.metadata.create_all(engine)
