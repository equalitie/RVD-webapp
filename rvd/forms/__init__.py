from rvd.models import Location as LocationModel, Organisation as OrganisationModel, Profession as ProfessionModel
from rvd.models import PrisonType as PrisonTypeModel, ReleaseType as ReleaseTypeModel
from rvd.models import Prison as PrisonModel, Source as SourceModel, event_witness, event_victim, event_perp
from rvd.models import Event as EventModel, UserOrganisation as UserOrganisationModel, Actor as ActorModel
from rvd.models import EventType as EventTypeModel
from rvd.models import session


def event_factory():
    return session.query(EventModel).all()


def organisation_factory():
    return session.query(OrganisationModel).all()


def profession_factory():
    return session.query(ProfessionModel).all()


def location_factory():
    return session.query(LocationModel).all()


def prison_type_factory():
    return session.query(PrisonTypeModel).all()


def release_type_factory():
    return session.query(ReleaseTypeModel).all()


def prison_factory():
    return session.query(PrisonModel).all()


def source_factory():
    return session.query(SourceModel).all()


def witnesses_factory():
    return session.query(ActorModel).filter(ActorModel.id.in_((x[1] for x in session.query(event_witness).all()))).all()


def victims_factory():
    return session.query(ActorModel).filter(ActorModel.id.in_((x[1] for x in session.query(event_victim).all()))).all()


def perpetrators_factory():
    return session.query(ActorModel).filter(ActorModel.id.in_((x[1] for x in session.query(event_perp).all()))).all()


def user_org_factory():
    return session.query(UserOrganisationModel).all()


def event_type_factory():
    return session.query(EventTypeModel).all()