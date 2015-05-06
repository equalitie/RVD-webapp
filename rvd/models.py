from flask_babel import lazy_gettext as ___
import sqlalchemy as sa
from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
engine = create_engine('mysql://user:password?@localhost/rvd', echo=True)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()


##################
## Action Model ##
##################

# Association tables

action_state = Table('action_state-authority', Base.metadata,
    sa.Column('action_id', sa.Integer, ForeignKey('actions.id')),
    sa.Column('state_authority_id', sa.Integer, ForeignKey('stateauthorities.id')))

action_international = Table('action_international-authority', Base.metadata,
    sa.Column('action_id', sa.Integer, ForeignKey('actions.id')),
    sa.Column('international_authority_id', sa.Integer, ForeignKey('internationalauthorities.id')))

action_event = Table('action_event', Base.metadata,
    sa.Column('action_id', sa.Integer, ForeignKey('actions.id')),
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')))

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
    sa.Column('actor_id', sa.Integer, ForeignKey('actors.id')),
    sa.Column('location_id', sa.Integer, ForeignKey('locations.id')))

actor_organisation = Table('actor_organisation', Base.metadata,
    sa.Column('actor_id', sa.Integer, ForeignKey('actors.id')),
    sa.Column('organisation_id', sa.Integer, ForeignKey('organisations.id')))

actor_profession = Table('actor_profession', Base.metadata,
    sa.Column('actor_id', sa.Integer, ForeignKey('actors.id')),
    sa.Column('profession_id', sa.Integer, ForeignKey('professions.id')))

class Actor(Base):
    __tablename__ = 'actors'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Name'), 'label': ___('Name')})
    birth_date = sa.Column(sa.Date, nullable=False, info={'description': ___('Name'), 'label': ___('Date of birth')})
    #telephone = sa.Column(PhoneNumberType(), info={
    telephone = sa.Column(sa.Unicode(16), info={
        'description': ___('+1 819 987-6543'), 'label': ___('Phone number')})
    address = sa.Column(sa.Unicode(250), nullable=False, info={'description': ___('Address'), 'label': ___('Address')})
    organisations = relationship('Organisation', secondary=actor_organisation, backref='members')
    professions = relationship('Profession', secondary=actor_profession, backref='practitioners')
    locations = relationship('Location', secondary=actor_location, backref='locals')
    gender = sa.Column(sa.Boolean, nullable=False, info={'description': ___('Gender'), 'label': ___('Gender')})
    is_activist = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Is activist'), 'label': ___('Is activist')})
    activist_info = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Activist info'), 'label': ___('Activist info')})


#################
## Event Model ##
#################

# Association tables

event_source = Table('event_source', Base.metadata,
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')),
    sa.Column('source_id', sa.Integer, ForeignKey('sources.id')))

event_releasetype = Table('event_release-type', Base.metadata,
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')),
    sa.Column('release_type_id', sa.Integer, ForeignKey('releasetypes.id')))

event_prison = Table('event_prison', Base.metadata,
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')),
    sa.Column('prison_id', sa.Integer, ForeignKey('prisons.id')))

event_location = Table('event_location', Base.metadata,
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')),
    sa.Column('location_id', sa.Integer, ForeignKey('locations.id')))

event_witness = Table('event_witness', Base.metadata,
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')),
    sa.Column('witness_id', sa.Integer, ForeignKey('actors.id')))

event_victim = Table('event_victim', Base.metadata,
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')),
    sa.Column('victim_id', sa.Integer, ForeignKey('actors.id')))

event_perp = Table('event_perpetrator', Base.metadata,
    sa.Column('event_id', sa.Integer, ForeignKey('events.id')),
    sa.Column('perpetrator_id', sa.Integer, ForeignKey('actors.id')))

#event_event = Table('event_event', Base.metadata,
#    sa.Column('event1_id', sa.Integer, ForeignKey('events.id')),
#    sa.Column('event2_id', sa.Integer, ForeignKey('events.id')))

class Event(Base):
    __tablename__ = 'events'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    title = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Title'), 'label': ___('Title')})
    description = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Description'), 'label': ___('Description')})
    charges = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Charges'), 'label': ___('Charges')})
    detention_date = sa.Column(sa.Date, nullable=False, info={
        'description': ___('Date of detention'), 'label': ___('Date of detention')})
    release_date = sa.Column(sa.Date, nullable=True, info={
        'description': ___('Date of release'), 'label': ___('Date of release')})
    report_date = sa.Column(sa.Date, nullable=False, info={
        'description': ___('Date of report'), 'label': ___('Date of report')})
    psych_assist = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Psychological assistance provided'),
        'label': ___('Psychological assistance provided')})
    material_assist = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Material assistance provided'),
        'label': ___('Material assistance provided')})
    consequences = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Consequences'), 'label': ___('Consequences')})
    was_activist= sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Was an activist'), 'label': ___('Was an activist')})
    victim_is_complainant = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Victim is complainant'), 'label': ___('Victim is complainant')})
    allow_storage = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Allows storage of information'),
        'label': ___('Allows storage of information')})
    allow_publishing = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Allows publishing of information'),
        'label': ___('Allows publishing of information')})
    allow_representation = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Allows legal representation'),
        'label': ___('Allows legal representation')})
    data_is_sensitive = sa.Column(sa.Boolean, nullable=False, info={
        'description': ___('Data is hyper sensitive'),
        'label': ___('Data is hyper sensitive')})
    release_types = relationship('ReleaseType', secondary=event_releasetype, backref='events')
    locations = relationship('Location', secondary=event_location, backref='events')
    prisons = relationship('Prison', secondary=event_prison, backref='events')
    sources = relationship('Source', secondary=event_source, backref='events')
    witnesses = relationship('Actor', secondary=event_witness, backref='witnessed')
    victims = relationship('Actor', secondary=event_victim, backref='victimized_during')
    perpetrators = relationship('Actor', secondary=event_perp, backref='perpetrated')
    #related = relationship('Event', secondary=event_event, backref='related_to')


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
    event_id = sa.Column(sa.Integer, ForeignKey('events.id'))
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
    sa.Column('organisation_id', sa.Integer, ForeignKey('organisations.id')),
    sa.Column('location_id', sa.Integer, ForeignKey('locations.id')))

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
    sa.Column('prison_id', sa.Integer, ForeignKey('prisons.id')),
    sa.Column('prison_type_id', sa.Integer, ForeignKey('prisontypes.id')))

prison_location = Table('prison_location', Base.metadata,
    sa.Column('prison_id', sa.Integer, ForeignKey('prisons.id')),
    sa.Column('location_id', sa.Integer, ForeignKey('locations.id')))

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
    type_code = sa.Column(sa.Integer, nullable=False, info={
        'description': ___('Type code'), 'label': ___('Type code')})


############################
## Rights Violation model ##
############################

class RightsViolation(Base):
    __tablename__ = 'rightsviolations'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    description = sa.Column(sa.Text, nullable=True, info={
        'description': ___('Description'), 'label': ___('Description')})
    event_id = sa.Column(sa.Integer, ForeignKey('events.id'))
    event = relationship('Event', backref=backref('rights_violations', order_by=id))


##################
## Source model ##
##################

class Source(Base):
    __tablename__ = 'sources'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={
        'description': ___('Name'), 'label': ___('Name')})
    organisation_id = sa.Column(sa.Integer, ForeignKey('organisations.id'))
    organisation = relationship('Organisation', backref=backref('sources', order_by=id))


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


## Create the database tables ##

Base.metadata.create_all(engine)
