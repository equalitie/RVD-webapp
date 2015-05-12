'''This file contains dictionaries mapping the names of fields in different
document types to the names of attributes in each model.
'''

import datetime

def translate_fields(parsed, mapping):
    '''Use a field map to translate parsed fields into names corresponding to a model's
attributes.'''
    translated = {}
    for key in parsed:
        if key in mapping:
            translated[mapping[key]] = parsed[key]
    return translated

def excel_parse_date(datefloat):
    return datetime.datetime(*xlrd.xldate_as_tuple(datefloat, excel_workbook.datemode))

international_authority = {
    u'Name': 'name',
    u'Description': 'description'
}

state_authority = {
    u'Name': 'name',
    u'Description': 'description'
}

action = {
    u'State authorities approached': 'state_bodies_approached',
    u'Complaint to state authority': 'complaint_to_state_authority',
    u'Response from state authority': 'response_from_state_authority',
    u'International authorities approached': 'international_bodies_approached',
    u'Complaint to international authority': 'complaint_to_international_authority',
    u'Response from international authority': 'response_from_international_authority',
    u'Events': 'events'
}

organisation = {
    u'Name': 'name',
    u'Description': 'description',
    u'Locations': 'locations'
}

profession = {
    u'Name': 'name'
}

location = {
    u'Name': 'name',
    u'Latitude': 'latitude',
    u'Longitude': 'longitude'
}

actor = {
    u'Name': 'name',
    u'Birth date': 'birth_date',
    u'Telephone number': 'telephone',
    u'Address': 'address',
    u'Gender': 'gender',
    u'Is an activist': 'is_activist',
    u'Activist info': 'activist_info',
    u'Organisations': 'organisations',
    u'Professions': 'professions',
    u'Locations': 'locations'
}

release_type = {
    u'Type code': 'type_code'
}

rights_violation = {
    u'Name': 'name',
    u'Description': 'description'
}

source = {
    u'Name': 'name',
    u'Organisations': 'organisations'
}

prison_type = {
    u'Name': 'name'
}

prison = {
    u'Name': 'name',
    u'Locations': 'locations',
    u'Prison types': 'prison_types'
}

event = {
    u'Title': 'title',
    u'Description': 'description',
    u'Charges': 'charges',
    u'Consequencess': 'consequences',
    u'Detention date': 'detention_date',
    u'Release date': 'release_date',
    u'Report date': 'report_date',
    u'Psychological assistance provided': 'psych_assist',
    u'Material assistance provided': 'material_assist',
    u'Was an activist': 'was_activist',
    u'Victim is complainant': 'victim_is_complainant',
    u'Allows storage of case details': 'allow_storage',
    u'Allows publishing of case details': 'allow_publishing',
    u'Allows legal representation': 'allow_representation',
    u'Victims may be harmed if data is published': 'data_is_sensitive',
    u'Release types': 'release_types',
    u'Locations': 'locations',
    u'Prisons': 'prisons',
    u'Sources': 'sources',
    u'Witnesses': 'witnesses',
    u'Victims': 'victims',
    u'Perpetrators': 'perpetrators',
    u'Rights violations': 'rights_violations'
}

report = {
    u'Text': 'text',
    u'Events': 'events'
}
