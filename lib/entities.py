'''This file contains dictionaries mapping the names of fields in different
document types to the names of attributes in each model.
'''

import datetime

import xlrd

def translate_fields(parsed, mapping):
    '''Use a field map to translate parsed fields into names corresponding to a model's
attributes.'''
    translated = {}
    # Handle the literal translation
    for key in parsed:
        if key in mapping:
            translated[mapping[key]] = parsed[key]
    # Insert default values
    if '_defaults' not in mapping:
        return translated
    for key in mapping['_defaults']:
        translated[key] = mapping['_defaults'][key]
    return translated

def excel_parse_date(datefloat):
    return datetime.datetime(*xlrd.xldate_as_tuple(datefloat, excel_workbook.datemode))

# StateAuthority model
# Fields: name, description, event
# event is a reference to Event
excel_state_authority = {
    'Name': 'name',
    'Description': 'description',
    '_defaults': {
        'event': None
    }
}

# Source model
# Fields: name, organisations
excel_source = {
    'Name': 'name',
    'Organisations': 'organisations'
}

# RightsViolation model
# Fields: name, description, event
# event is a reference to Event
excel_rights_violation = {
    'Name': 'name',
    'Description': 'description',
    '_defaults': {
        'event': None
    }
}

# ReleaseType model
# Fields: type_code
excel_release_type = {
    'Type of release': 'type_code'
}

# Profession model
# Fields: name, actor
# actor is a reference to Actor
excel_profession = {
    'Name': 'name'
}

# PrisonType model
# Fields: name, prisons
# prisons is a reference to [Prison]
excel_prison_type = {
    'Name': 'name',
    '_defaults': {
        'prisons': []
    }
}

# Prison model
# Fields: name, location, prison_type
# location is a reference to Location
# prison_type is a reference to PrisonType
excel_prison = {
    'Name': 'name',
    'Location': 'location', # Copy the location for extra handling later
    '_defaults': {
        'prison_type': None
    }
}

# Organisation model
# Fields: name, description, locations
# locations is a reference to [Location]
excel_organisation = {
    'Name': 'name',
    'Locations': 'locations' # Copy the locations for extra handling later
}

# Media model
# Fields: name, description, meta_tags, media_location,
#         created, edition, location
# location is a reference to Location
excel_media = {
    'Name': 'name',
    'Description': 'description',
    'Media tags': 'media_tags',
    'Media location': 'media_location',
    'Creation date': 'created',
    'Edition date': 'edition',
    'Location': 'location'
}

# Location model
# Fields: name, latitude, longitude
excel_location = {
    'Name': 'name',
    'Latitude': 'latitude',
    'Longitude': 'longitude'
}

# international.Authority model
# Fields: name, description, event
# event is a reference to Event
excel_international_authority = {
    'Name': 'name',
    'Description': 'description',
    '_defaults': {
        'event': None
    }
}

# EvidenceType model
# Fields: name, description, event
# event is a reference to Event
excel_evidence_type = {
    'Name': 'name',
    'Description': 'description',
    '_defaults': {
        'event': None
    }
}

# ActorRelationType model
# Fields: name, event
# event is a reference to Event
excel_actor_relation_type = {
    'Name': 'name',
    '_defaults': {
        'event': None
    }
}

# Action model
# Fields: complaint_to_state_authority, state_body_approached, response_from_state_authority,
#         complaint_to_international_authority, international_body_approached,
#         response_from_international_authority, event
# state_body_approached is a reference to state.Authority
# international_body_approached is a reference to international.Authority
# event is a reference to Event
excel_action = {
    'Complaint to state or court authorities': 'complaint_to_state_authority',
    'Response from state body': 'response_from_state_authority',
    'Complaint to international body': 'complaint_to_international_authority',
    'Response from international body': 'response_from_international_authority',
    'State body approached': 'state_body_approached',
    'International body approached': 'international_body_approached',
    '_defaults': {
        'event': None
    }
}

# Actor model
# Fields: name, age, birth_date, telephone, address, organisation, location,
#         gender, profession, is_activist, activist_info
# organisation is a reference to Organisation
# location is a reference to Location
# profession is a reference to Profession
excel_actor = {
    'Name': 'name',
    'Age': 'age',
    'Date of birth': 'birth_date',
    'Telephone': 'telephone',
    'Address': 'address',
    'Gender': 'gender',
    'Activist': 'is_activist',
    'Activist details': 'activist_info',
    'Location': 'location',
    'Profession': 'profession',
    'Organisation': 'organisation'
}

# Event model
# Fields: title, description, charges, detention_date, release_date, report_date,
#         release_type, location, prisons, actor, sources, media, psych_assist,
#         material_assist, action_taken_by, related, consequences, was_activist,
#         witnesses, victim_is_complaintant, source_victim_relation,
#         source_witness_relations, allow_storage, allow_publishing,
#         data_is_sensitive, allow_representation
# release_type is a reference to ReleaseType
# location is a reference to Location
# prisons is a reference to [Prison]
# actor is a reference to Actor
# sources is a reference to [Source]
# media is a reference to Media
# action_taken_by is a reference to Actor
# related is a reference to [Event]
# witnesses is a reference to [Actor]
# source_victim_relation is a reference to ActorRelationType
# source_witness_relations is a reference to [ActorRelationType]
excel_event = {
    'Title': 'title',
    'Description': 'description',
    'Charges': 'charges',
    'Date of detention': 'detention_date',
    'Date of release': 'release_date',
    'Date of report': 'report_date',
    'Type of release': 'release_type',
    'Psychological assistance provided': 'psych_assist',
    'Material assistance provided': 'material_assist',
    'Consequences': 'consequences',
    'Was an activist': 'was_activist',
    'Victim is complainant': 'victim_is_complainant',
    'Consent to store data in a secure database': 'allow_storage',
    'Consent to publish event details online': 'allow_publishing',
    'Might the victim suffer if data is published': 'data_is_sensitive',
    'Consent to legal representation before relevant authorities': 'allow_representation',
    'Location': 'location',
    '_defaults': {
        'release_type': None,
        'prisons': [],
        'actor': None,
        'sources': [],
        'media': None,
        'action_taken_by': None,
        'related': [],
        'witnesses': [],
        'source_victim_relation': None,
        'source_witness_relations': []
    }
}
