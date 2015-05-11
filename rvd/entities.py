'''This file contains dictionaries mapping the names of fields in different
document types to the names of attributes in each model.
'''

from flask_babel import lazy_gettext as ___

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
    ___('Name'): 'name',
    ___('Description'): 'description'
}

state_authority = {
    ___('Name'): 'name',
    ___('Description'): 'description'
}

action = {
    ___('State authorities approached'): 'state_bodies_apprached',
    ___('Complaint to state authority'): 'complaint_to_state_authority',
    ___('Response from state authority'): 'response_from_state_authority',
    ___('International authorities approached'): 'international_bodies_approached',
    ___('Complaint to international authority'): 'complaint_to_international_authority',
    ___('Response from international authority'): 'response_from_international_authority',
    ___('Events'): 'events'
}

organisation = {
    ___('Name'): 'name',
    ___('Description'): 'description',
    ___('Locations'): 'locations'
}

profession = {
    ___('Name'): 'name'
}

location = {
    ___('Name'): 'name',
    ___('Latitude'): 'latitude',
    ___('Latitude'): 'longitude'
}

actor = {
    ___('Name'): 'name',
    ___('Birth date'): 'birth_date',
    ___('Telephone number'): 'telephone',
    ___('Address'): 'address',
    ___('Gender'): 'gender',
    ___('Is an activist'): 'is_activist',
    ___('Activist info'): 'activist_info',
    ___('Organisations'): 'organisations',
    ___('Professions'): 'professions',
    ___('Locations'): 'locations'
}

release_type = {
    ___('Type code'): 'type_code'
}

rights_violation = {
    ___('Name'): 'name',
    ___('Description'): 'description'
}

source = {
    ___('Name'): 'name',
    ___('Organisations'): 'organisations'
}

prisons_type = {
    ___('Name'): 'name'
}

prison = {
    ___('Name'): 'name',
    ___('Locations'): 'locations',
    ___('Prison types'): 'prison_types'
}

event = {
    ___('Title'): 'title',
    ___('Description'): 'description',
    ___('Charges'): 'charges',
    ___('Consequencess'): 'consequences',
    ___('Detention date'): 'detention_date',
    ___('Release date'): 'release_date',
    ___('Report date'): 'report_date',
    ___('Psychological assistance provided'): 'psych_assist',
    ___('Material assistance provided'): 'material_assist',
    ___('Was an activist'): 'was_activist',
    ___('Victim is complainant'): 'victim_is_complainant',
    ___('Allows storage of case details'): 'allow_storage',
    ___('Allows publishing of case details'): 'allow_publishing',
    ___('Allows legal representation'): 'allow_representation',
    ___('Victims may be harmed if data is published'): 'data_is_sensitive',
    ___('Release types'): 'release_types',
    ___('Locations'): 'locations',
    ___('Prisons'): 'prisons',
    ___('Sources'): 'sources',
    ___('Witnesses'): 'witnesses',
    ___('Victims'): 'victims',
    ___('Perpetrators'): 'perpetrators',
    ___('Rights violations'): 'rights_violations'
}

report = {
    ___('Text'): 'text',
    ___('Events'): 'events'
}
