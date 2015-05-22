from rvd import parsers

d = parsers._parse_excel_template('testdata/template-es.xlsx')

'''
d = parsers._parse_org2_docx('Organization 2 doc name goes here')
print 'Parsed REPORT'
print d['report']

print 'Parsed EVENTS'
for event in d['events']:
    print 'Actor name = ' + event.victims[0].name
    print 'Actor org  = ' + event.victims[0].organisations[0].name
    print 'Source name = ' + event.sources[0].name
    try:
        loc = event.locations[0]
        print 'Location = '
        print loc.name
    except IndexError: pass

print 'Done'
'''
