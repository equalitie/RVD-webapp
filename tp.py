from rvd import parsers

d = parsers._parse_org1_docx('/Volumes/untitled/Data\ from\ CHIPress\ and\ CCDHRN/CCDHRN/2014.09\ CCDHRN.docx')
print 'Parsed REPORT'
print d['report']

print 'Parsed EVENTS'
for event in d['events']:
    print 'Actor name = ' + event.victims[0].name
    print 'Source name = ' + event.sources[0].name
    loc = event.locations[0]
    print 'Location = {0} lat = {1} lon = {2}'.format(loc.name, loc.latitude, loc.longitude)

print 'Done'
