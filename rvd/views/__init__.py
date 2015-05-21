from rvd.models import Action, Actor
from sqlalchemy.inspection import inspect


def get_attr(a):
    if isinstance(a, Action):
        items = [u"{}: {}".format(k, v) for k, v in a.__dict__.iteritems() if k[0:4] != '_sa_']
        return ", ".join(items)
    if hasattr(a, 'name'):
        return a.name
    if hasattr(a, 'type_code'):
        return str(a.type_code)
    if hasattr(a, 'id'):
        return str(a.id)
    if hasattr(a, 'email'):
        return str(a.email)


def get_name_from_id(needle, things):
    for thing in things:
        if int(thing.id) == int(needle):
            return thing


def flatten_instance(obj, what):
    fields = {'id': obj.id}
    for c in obj.__table__.columns:
        fields[c.info.get('label')] = getattr(obj, c.key)
    for r in inspect(what).relationships:
        associated_data = getattr(obj, r.key)
        try:
            fields[r.key] = ", ".join([get_attr(a) for a in associated_data]) if associated_data else None
        except TypeError:
            fields[r.key] = get_attr(associated_data)
    return fields