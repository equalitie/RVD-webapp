# -*- coding: utf-8 -*-

import json
import time
import urllib2
import datetime

class JSObject(dict):
    '''A Javascript-style object that allows for dot and square-bracket accessing.'''

    def __init__(self, dictionary, **kwargs):
        self.__dict__.update(dictionary)
        self.__dict__.update(kwargs)
        self._keys = dictionary.keys() + kwargs.keys()

    def __getattr__(self, key):
        return self.__dict__[key]

    def __setattr__(self, key, val):
        self.__dict__[key] = val
        self._keys.append(key)
        return val

    def __str__(self):
        keys = [key + ': ' + str(self.__dict__[key]) for key in self._keys if key != '_keys']
        return '{' + ', '.join(keys) + '}'

    def __repr__(self):
        return self.__str__()

    def keys(self):
        try:
            keyindex = self._keys.index('_keys')
            self._keys.pop(keyindex)
            return self._keys
        except ValueError:
            return self._keys


def max_by(coll, accessor_fn):
    '''Obtains the item in a collection, x, wherein accessor_fn(x) is a maximum for all
values in the collection.'''

    if len(coll) == 0:
        return None
    elif len(coll) == 1:
        return coll[0]
    max_item, max_value = coll[0], accessor_fn(coll[0])
    for item in coll[1:]:
        value = accessor_fn(item)
        if value > max_value:
            max_item = item
            max_value = value
    return max_item


def geocodes(location_name, include_importance=False):
    '''Obtain the geographical coordinates of a place based on the name.
Returns an array of dictionaries containing latitude, longitude, and name of the location.'''

    nominatim_url = 'https://nominatim.openstreetmap.org/search?format=json&q='
    req = urllib2.urlopen(nominatim_url + location_name.replace(' ', '+')).read()
    data = json.loads(req)
    # Build array of dictionaries in a way that is compatible with older Python versions
    geocodings = []
    for match in data:
        new_entry = {
            'name': match['display_name'],
            'longitude': match['lon'],
            'latitude': match['lat']
        }
        if include_importance:
            new_entry['importance'] = match['importance']
        geocodings.append(new_entry)
    return geocodings


def to_datetime(time_struct):
    '''Convert a time_struct to a datetime object.'''
    return datetime.datetime.fromtimestamp(time.mktime(time_struct))
