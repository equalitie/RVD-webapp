# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext as ___

import re
import time
import datetime
import docx
import xlrd

import utils
from models import *
import entities

# Constants

# Identifiers for types of legacy documents

ORG1_DOCX = 1
ORG2_DOCX = 2
EXCEL_DOC = 4

# Special values

# Values compared to these should always be converted to lowercase first.
YES = ___('yes')
NO = ___('no')
MALE = ___('male')
FEMALE = ___('female')

# Entity names, as presented in the excel document template

ACTIONS = u'Actions'
ACTORS = u'Actors'
REPORTS = u'Reports'
EVENTS = u'Events'
INTERNATIONAL_AUTHORITIES = u'International Authorities'
LOCATIONS = u'Locations'
ORGANISATIONS = u'Organisations'
PRISONS = u'Prisons'
PRISON_TYPES = u'Prison Types'
PROFESSIONS = u'Professions'
RELEASE_TYPES = u'Release Types'
RIGHTS_VIOLATIONS = u'Rights Violations'
SOURCES = u'Sources'
STATE_AUTHORITIES = u'State Authorities'

# Private - Should not be called externally

def log_error(msg):
    print msg
    # Log to a file later?

def _parse_org1_docx_report(doc):
    report = ''
    for p in doc.paragraphs:
        para = p.text.strip()
        if len(para) > 0:
            report += para + '\n'
    return report

# Parse organisation 1's docx documents.
# Does not accept the excel_workbook argument (None, here)
def _parse_org1_docx_events(doc):
    events = []
    table = doc.tables[0]
    # First row contains table headers
    for i in range(1, len(table.rows)):
        row = table.row_cells(i)
        names = row[2].text.split(',')
        # Organisation names are provided in parentheses at the end of the list of names
        orgindex = names[-1].find('(')
        if orgindex >= 0:
            organisation = names[-1][orgindex + 1: names[-1].find(')')]
            names[-1] = names[-1][:orgindex]
        for name in names:
            parsed = {'actor': {}, 'location': {}, 'source': {}}
            parsed['actor']['name'] = name.strip()
            parsed['actor']['organisations'] = [organisation]
            parsed['report_date'] = time.strptime(row[0].text.strip(), '%d.%m.%y')
            parsed['report_date'] = utils.to_datetime(parsed['report_date'])
            parsed['location']['name'] = row[1].text.strip()
            # TODO
            # Think of how this field fits into the schema we have.
            # parsed['type'] = row[3].text.strip()
            parsed['source']['name'] = row[4].text.strip()
            events.append(parsed)
    return events

def _org1_events_to_model(events):
    '''Convert a collection of events into instances of the Event model'''
    for i in range(len(events)):
        event = events[i]
        actor = Actor(name=event['actor']['name'])
        del event['actor']
        source = Source(name=event['source']['name'])
        del event['source']
        geocoded = utils.geocodes(event['location']['name'], include_importance=True)
        del event['location']
        if geocoded is not None and len(geocoded) > 0:
          geocoded = utils.max_by(geocoded, lambda gc: gc['importance'])
          location = Location(name=geocoded['name'],
              latitude=geocoded['latitude'], longitude=geocoded['latitude'])
          events[i].location = location
        events[i] = Event(**event)
        events[i].actor = actor
    return events

def _org1_report_to_model(report, events):
    '''Convert a report text into an instance of the Report model'''
    report = Report(text=report)
    for i in range(len(events)):
        events[i].report_id = report
    report.events = events
    return report

def _parse_org1_docx(_file):
    doc = docx.Document(_file)
    report = _parse_org1_docx_report(doc)
    events = _parse_org1_docx_events(doc)
    events = _org1_events_to_model(events)
    report = _org1_report_to_model(report, events)
    return {
        'report': report,
        'events': events
    }


# Parse the report part of a document before the list of event descriptions
def _parse_org2_docx_report(doc):
    report = ''
    for p in doc.paragraphs:
        if re.match('\d+\)\s+(n|N)ombre', p.text) is not None:
            break
        report += p.text + '\n'
    return report


# Parse organisation 2's docx documents.
# Does not accept the excel_workbook argument (None, here)
def _parse_org2_docx_events(doc):
    events = []
    for i, p in enumerate(doc.paragraphs):
        if re.match('\d+\)\s+(n|N)ombre', p.text) is not None:
            parsed = {'actor': {}, 'location': {}, 'source': {}}
            parsed['actor']['name'] = ' '.join(doc.paragraphs[i].text.split(':')[1:]).strip()
            parsed['actor']['organisation'] = ' '.join(doc.paragraphs[i + 1].text.split(':')[1:]).strip()
            parsed['location']['name'] = ' '.join(doc.paragraphs[i + 2].text.split(':')[1:]).strip()
            # TODO
            # Decide if we want to include this extra field that does not follow
            # the schema description
            # parsed['notes'] = ' '.join(doc.paragraphs[i + 3].text.split(':')[1:]).strip()
            parsed['source']['name'] = ' '.join(doc.paragraphs[i + 4].text.split(':')[1:]).strip()
            parsed['detention_date'] = ' '.join(doc.paragraphs[i + 5].text.split(':')[1:]).strip()
            parsed['report_date'] = ' '.join(doc.paragraphs[i + 6].text.split(':')[1:]).strip()
            if parsed['detention_date']:
                parsed['detention_date'] = parsed['detention_date'].replace(' ', '').replace('.', '')
                try:
                    parsed['detention_date'] = time.strptime(parsed['detention_date'], '%d-%m-%Y')
                except:
                    parsed['detention_date'] = time.strptime(parsed['detention_date'], '%d-%m-%y')
                parsed['detention_date'] = utils.to_datetime(parsed['detention_date'])
            if parsed['report_date']:
                parsed['report_date'] = parsed['report_date'].replace(' ', '').replace('.', '')
                try:
                    parsed['report_date'] = time.strptime(parsed['report_date'], '%d-%m-%Y')
                except:
                    parsed['report_date'] = time.strptime(parsed['report_date'], '%d-%m-%y')
                parsed['report_date'] = utils.to_datetime(parsed['report_date'])
            events.append(parsed)
    return events

def _org2_events_to_model(events):
    '''Convert parsed event data to model instances'''
    for i in range(len(events)):
        event = events[i]
        actor = event['actor']
        organisation = actor['organisation']
        actor = Actor(name=actor['name'])
        organisation = Organisation(name=organisation)
        actor.organisations = [organisation]
        location = event['location']['name']
        geocodes = utils.geocodes(location, include_importance=True)
        location = utils.max_by(geocodes, lambda gc: gc['importance'])
        location = Location(name=location['name'],
            latitude=location['latitude'], longitude=location['longitude'])
        source = event['source']
        source = Source(name=source['name'])
        del event['actor']
        del event['location']
        del event['source']
        event['victims'] = [actor]
        event['locations'] = [location]
        event['sources']  = [source]
        events[i] = Event(**event)
    return events

def _org2_report_to_model(report, events):
    '''Convert parsed report data to a model instnace'''
    report = Report(text=report)
    for i in range(len(events)):
        events[i].report_id = report.id
    report.events = events
    return report

def _parse_org2_docx(_file):
    doc = docx.Document(_file)
    report = _parse_org2_docx_report(doc)
    events = _parse_org2_docx_events(doc)
    events = _org2_events_to_model(events)
    report = _org2_report_to_model(report, events)
    return {
        'report': report,
        'events': events
    }

# Based on Bill's pseudocode
# https://gist.github.com/billdoran/8acb07dedc0e18775e38#file-example-algorithm
def _parse_excel_template(filename):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)
    for row_num in range(sheet.nrows):
        cur_event = None
        reading_event = False
        row = sheet.row(row_num)
        if row[0].value() == 'Event' and not reading_event:
            reading_event = True
            #row_num += 1 # Jump to the actual event data
            event = Event(**{
                'title': row[0].value(),
                'description': row[1].value(),
                'charges': row[2].value(),
                'consequences': row[3].value(),
                'detention_date': _excel_parse_date(row[4].value(), book),
                'release_date': _excel_parse_date(row[5].value(), book),
                'report_date': _excel_parse_date(row[6].value(), book),
                'psych_assist': row[7].value().lower() == YES,
                'material_assist': row[8].value().lower() == YES,
                'was_activist': row[9].value().lower() == YES,
                'victim_is_complainant': row[10].value().lower() == YES,
                'allow_storage': row[11].value().lower() == YES,
                'allow_publishing': row[12].value().lower() == YES,
                'allow_representation': row[13].value().lower() == YES,
                'data_is_sensitive': row[14].value().lower() == YES,
                'release_types': [session.query(ReleaseType).filter_by(type_code=int(row[15].value())).first()],
                'locations': [session.query(Location).filter_by(name=row[16].value()).first()],
                'prisons': [session.query(Prison).filter_by(name=row[17].value()).first()],
                'rights_violations': [session.query(RightsViolation).filter_by(name=row[18].value()).first()]
            })
            cur_event = event
            cur_event.victims = []
            cur_event.witnesses = []
            cur_event.perpetrators = []
            cur_event.actions = []
            cur_event.sources = []
        elif row[1].value() == 'Actors' and reading_event:
            _type = row[2].value()
            actor = Actor(**{
                'name': row[3].value(),
                'birth_date': _excel_parse_date(row[4].value(), book),
                'telephone': row[5].value(),
                'address': row[6].value(),
                'gender': row[7].value(),
                'is_activist': row[8].value().lower() == YES,
                'organisations': [session.query(Organisation).filter_by(name=row[9].value()).first()],
                'professions': [session.query(Profession).filter_by(name=row[10].value()).first()]
            })
            if _type == 'Witness':
                cur_event.witnesses.append(actor)
            elif _type == 'Victim':
                cur_event.victims.append(actor)
            elif _type == 'Perpetrator':
                cur_event.perpetrators.append(actor)
        elif row[1].value() == 'Actions' and reading_event:
            action = Action(**{
                'state_bodies_approached': [
                    session.query(StateAuthority).filter_by(name=row[2].value()).first()],
                'complaint_to_state_authority': row[3].value(),
                'response_from_state_authority': row[4].value(),
                'international_bodies_approached': [
                    session.query(InternationalAuthority).filter_by(name=row[5].value()).first()],
                'complaint_to_international_authority': row[6].value(),
                'response_from_international_authority': row[7].value()
            })
            cur_event.actions.append(action)
        elif row[1].value() == 'Sources' and reading_event:
            source = Source(**{
                'name': row[2].value(),
                'organisations': [session.query(Organisation).filter_by(name=row[3].value()).first()]
            })
            cur_event.sources.append(source)
        session.add_all(cur_event.witnesses)
        session.add_all(cur_event.victims)
        session.add_all(cur_event.perpetrators)
        session.add_all(cur_event.actions)
        session.add_all(cur_event.sources)
        session.add(cur_event)
    session.commit()

'''
# This function will do generic parsing of the content in an excel workbook
# but we will leave it to other handler functions to do entity-specific manipulation
def _parse_excel_template(filename):
    book = xlrd.open_workbook(filename)
    # We assume everything is on the same sheet
    sheet = book.sheet_by_index(0)
    entities = {}
    current_entity_fields = []
    current_entity_name = ''
    for row_num in range(sheet.nrows):
        # When we encounter a row like ['Event', 'Title', 'Description', ...]
        # We are looking at the outline of a new entity type (in example, it's 'Event')
        if sheet.row(row_num)[0].value != '':
            entity_name = sheet.row(row_num)[0].value
            entities[entity_name] = []
            current_entity_name = entity_name
            current_entity_fields = [col.value for col in sheet.row_slice(row_num, 1)]
            continue
        values = [col.value for col in sheet.row_slice(row_num, 1)]
        new_instance = {}
        for i in range(len(current_entity_fields)):
            field_name = current_entity_fields[i]
            new_instance[field_name] = values[i]
        if '' in new_instance:
            del new_instance['']
        entities[current_entity_name].append(new_instance)
    entities['finished'] = [] 
    # Call on each entity's respective model instance builder.
    entity_names = entities.keys()
    for entity_name in entity_names:
        print entities['finished'], entity_name
        if entity_name not in entities['finished']:
            handler = _post_collection_handlers.get(entity_name, _id)
            entities = handler(entities, book)
            entities['finished'].append(entity_name)
    del entities['finished']
    return entities
'''

def _parse_error(stream):
    return {'error': 'No parser exists for the provided filetype.'}


def _id(x, *args, **kwargs):
    return x


def _excel_parse_date(datefloat, workbook):
    return datetime.datetime(*xlrd.xldate_as_tuple(datefloat, workbook.datemode))

# Given a list of strings of integers that should be indices into an array,
# produce a list of converted integers. A string error message will be left
# in the place of a value that could not be parsed. Indeces are 1-indexed.
def _make_indices(indices, array_len):
    for i in range(len(indices)):
        try:
            v = int(indices[i])
        except ValueError:
            indices[i] = '{0} not a valid integer.'.format(indices[i])
            continue
        if v < 1 or v > array_len:
            indices[i] = 'Index ({0}) must be between 1 and {1} inclusive'.format(
                v, array_len)
        else:
            indices[i] = v - 1
    return indices

# Using a list of indices (or error strings) as generated by _make_indices,
# take items from a given array with the specified indices in order.
def _take(array, indices):
    pulled = []
    for index in indices:
        if isinstance(index, int):
            pulled.append(array[index])
        else: # index is an error string
            log_error(index)
    return pulled

# A convenience function to convert a string listing indices (e.g. "1, 2, 4")
# into the integer equivalent, 0-indexed, array ([0, 1, 3]) and then
# Extract elements from the provided array being indexed into and outputting
# any errors that occur.
def _from_indices(ind_list, other_entities):
    # If a single index value is provided, it will be converted to a float.
    # So it is necessary to convert it back to a string-int.
    if isinstance(ind_list, float):
        ind_list = str(int(ind_list))
    indices = _make_indices(ind_list.split(','), len(other_entities))
    values = _take(other_entities, indices)
    return values

#################################
## Model building transformers ##
#################################

# Each of the following handlers converts parsed fields into model instances.
# Each handler takes as input the dictionary of parsed fields and returns
# a modified dictionary containing model instances.
# The 'finished' field is a list of entity names that have already been
# converted. It is used by handlers to do work on entities they are related to.
# 
# !!! IMPORTANT !!!
# All handlers are *required* to maintain the order of entities in value fields.

def p_dict(d, level=0):
    keys = sorted(d.keys())
    for key in keys:
        if isinstance(d[key], dict):
            print ('\t' * level) + key + ' =>'
            p_dict(d[key], level + 1)
        else:
            print ('\t' * level) + '{0} => {1}'.format(key, d[key])

# Handles building entities upon which others depend.
def _pre_handle(parsed, wb, *entity_names):
    print 'Calling _pre_handle to handle ' + ' and '.join(entity_names)
    print 'Parsed["finished"] = ' + str(parsed['finished'])
    for entity in entity_names:
        if entity not in parsed['finished']:
            print 'Unfound ' + entity
            parsed = _post_collection_handlers[entity](parsed, wb)
            parsed['finished'].append(entity)
    print '_-_-_ End of pre handle _-_-_'
    #p_dict(parsed)
    return parsed

def _action_h(parsed, wb):
    print '### action_h'
    parsed = _pre_handle(parsed, wb, STATE_AUTHORITIES, INTERNATIONAL_AUTHORITIES, EVENTS)
    for i in range(len(parsed[ACTIONS])):
        action = entities.translate_fields(parsed[ACTIONS][i], entities.action)
        action['state_bodies_approached'] = _from_indices(
            action['state_bodies_approached'], parsed[STATE_AUTHORITIES])
        action['international_bodies_approached'] = _from_indices(
            action['international_bodies_approached'], parsed[INTERNATIONAL_AUTHORITIES])
        action['events'] = _from_indices(action['events'], parsed[EVENTS])
        parsed[ACTIONS][i] = Action(**action)
    return parsed

def _actor_h(parsed, wb):
    print '### actor_h'
    parsed = _pre_handle(parsed, wb, ORGANISATIONS, PROFESSIONS, LOCATIONS)
    for i in range(len(parsed[ACTORS])):
        actor = entities.translate_fields(parsed[ACTORS][i], entities.actor)
        actor['organisations'] = _from_indices(actor['organisations'], parsed[ORGANISATIONS])
        actor['professions'] = _from_indices(actor['professions'], parsed[PROFESSIONS])
        actor['locations'] = _from_indices(actor['locations'], parsed[LOCATIONS])
        actor['birth_date'] = _excel_parse_date(actor['birth_date'], wb)
        actor['gender'] = actor['gender'].lower() == MALE # Not trying to be sexist, just efficient.
        actor['is_activist'] = actor['is_activist'].lower() == YES
        parsed[ACTORS][i] = Actor(**actor)
    return parsed

def _event_h(parsed, wb):
    print '### event_h'
    parsed = _pre_handle(parsed, wb,
        RELEASE_TYPES, LOCATIONS, PRISONS, SOURCES, ACTORS, RIGHTS_VIOLATIONS)
    for i in range(len(parsed[EVENTS])):
        event = entities.translate_fields(parsed[EVENTS][i], entities.event)
        event['release_types'] = _from_indices(event['release_types'], parsed[RELEASE_TYPES])
        event['locations'] = _from_indices(event['locations'], parsed[LOCATIONS])
        event['prisons'] = _from_indices(event['prisons'], parsed[PRISONS])
        event['sources'] = _from_indices(event['sources'], parsed[SOURCES])
        event['witnesses'] = _from_indices(event['witnesses'], parsed[ACTORS])
        event['victims'] = _from_indices(event['victims'], parsed[ACTORS])
        event['perpetrators'] = _from_indices(event['perpetrators'], parsed[ACTORS])
        event['rights_violations'] = _from_indices(
            event['rights_violations'], parsed[RIGHTS_VIOLATIONS])
        event['detention_date'] = _excel_parse_date(event['detention_date'], wb)
        event['release_date'] = _excel_parse_date(event['release_date'], wb)
        event['report_date'] = _excel_parse_date(event['report_date'], wb)
        event['psych_assist'] = event['psych_assist'].lower() == YES
        event['material_assist'] = event['material_assist'].lower() == YES
        event['was_activist'] = event['was_activist'].lower() == YES
        event['victim_is_complainant'] = event['victim_is_complainant'].lower() == YES
        event['allow_storage'] = event['allow_storage'].lower() == YES
        event['allow_publishing'] = event['allow_publishing'].lower() == YES
        event['allow_representation'] = event['allow_representation'].lower() == YES
        event['data_is_sensitive'] = event['data_is_sensitive'].lower() == YES
        parsed[EVENTS][i] = Event(**event)
    return parsed

def _report_h(parsed, wb):
    print '### report_h'
    parsed = _pre_handle(parsed, wb, EVENTS)
    for i in range(len(parsed[REPORTS])):
        report = entities.translate_fields(parsed[REPORTS][i], entities.report)
        report['events'] = _from_indices(report['events'], parsed[EVENTS])
        parsed[REPORTS][i] = Report(**report)
    return parsed 

def _inter_auth_h(parsed, wb):
    print '### inter_auth_h'
    for i in range(len(parsed[INTERNATIONAL_AUTHORITIES])):
        ia = entities.translate_fields(
            parsed[INTERNATIONAL_AUTHORITIES][i], entities.international_authority)
        parsed[INTERNATIONAL_AUTHORITIES][i] = InternationalAuthority(**ia)
    return parsed

def _state_auth_h(parsed, wb):
    print '### state_auth_h'
    for i in range(len(parsed[STATE_AUTHORITIES])):
        sa = entities.translate_fields(parsed[STATE_AUTHORITIES][i], entities.state_authority)
        parsed[STATE_AUTHORITIES][i] = StateAuthority(**sa)
    return parsed

def _organisation_h(parsed, wb):
    print '### organisation_h'
    parsed = _pre_handle(parsed, wb, LOCATIONS)
    for i in range(len(parsed[ORGANISATIONS])):
        organisation = entities.translate_fields(parsed[ORGANISATIONS][i], entities.organisation)
        organisation['locations'] = _from_indices(organisation['locations'], parsed[LOCATIONS])
        parsed[ORGANISATIONS][i] = Organisation(**organisation)
    return parsed

def _profession_h(parsed, wb):
    print '### profession_h'
    for i in range(len(parsed[PROFESSIONS])):
        profession = entities.translate_fields(parsed[PROFESSIONS][i], entities.profession)
        parsed[PROFESSIONS][i] = Profession(**profession)
    return parsed

def _location_h(parsed, wb):
    print '### location_h'
    for i in range(len(parsed[LOCATIONS])):
        location = entities.translate_fields(parsed[LOCATIONS][i], entities.location)
        parsed[LOCATIONS][i] = Location(**location)
    return parsed

def _rights_violation_h(parsed, wb):
    print '### rights_violation_h'
    for i in range(len(parsed[RIGHTS_VIOLATIONS])):
        rv = entities.translate_fields(parsed[RIGHTS_VIOLATIONS][i], entities.rights_violation)
        parsed[RIGHTS_VIOLATIONS][i] = RightsViolation(**rv)
    return parsed

def _release_type_h(parsed, wb):
    print '### release_type_h'
    for i in range(len(parsed[RELEASE_TYPES])):
        rt = entities.translate_fields(parsed[RELEASE_TYPES][i], entities.release_type)
        parsed[RELEASE_TYPES][i] = ReleaseType(**rt)
    return parsed

def _source_h(parsed, wb):
    print '### source_h'
    parsed = _pre_handle(parsed, wb, ORGANISATIONS)
    for i in range(len(parsed[SOURCES])):
        source = entities.translate_fields(parsed[SOURCES][i], entities.source)
        source['organisations'] = _from_indices(source['organisations'], parsed[ORGANISATIONS])
        parsed[SOURCES][i] = Source(**source)
    return parsed

def _prison_type_h(parsed, wb):
    print '### prison_type_h'
    for i in range(len(parsed[PRISON_TYPES])):
        pt = entities.translate_fields(parsed[PRISON_TYPES][i], entities.prison_type)
        parsed[PRISON_TYPES][i] = PrisonType(**pt)
    return parsed

def _prison_h(parsed, wb):
    print '### prison_h'
    parsed = _pre_handle(parsed, wb, LOCATIONS, PRISON_TYPES)
    for i in range(len(parsed[PRISONS])):
        prison = entities.translate_fields(parsed[PRISONS][i], entities.prison)
        prison['locations'] = _from_indices(prison['locations'], parsed[LOCATIONS])
        prison['prison_types'] = _from_indices(prison['prison_types'], parsed[PRISON_TYPES])
        parsed[PRISONS][i] = Prison(**prison)
    return parsed

# Mapping of entitiy names, as listed in the document template,
# to handler functions that will convert parsed data into usable
# model instances.
_post_collection_handlers = {
    ACTIONS: _action_h,
    ACTORS: _actor_h,
    EVENTS: _event_h,
    REPORTS: _report_h,
    INTERNATIONAL_AUTHORITIES: _inter_auth_h,
    STATE_AUTHORITIES: _state_auth_h,
    ORGANISATIONS: _organisation_h,
    PROFESSIONS: _profession_h,
    LOCATIONS: _location_h,
    RELEASE_TYPES: _release_type_h,
    RIGHTS_VIOLATIONS: _rights_violation_h,
    SOURCES: _source_h,
    PRISON_TYPES: _prison_type_h,
    PRISONS: _prison_h
}

# Options for existing parsers.
_parsers = {
    ORG1_DOCX: _parse_org1_docx,
    ORG2_DOCX: _parse_org2_docx,
    EXCEL_DOC: _parse_excel_template
}


# Public

def parse(stream, filetype):
    '''Parse the contents of a report file with one of the accepted filetypes into a dict'''
    parse = _parsers.get(filetype, _parse_error)
    return parse(stream)
