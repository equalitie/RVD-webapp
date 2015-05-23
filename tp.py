from rvd import parsers
#d = parsers._parse_excel_template('testdata/template-es.xlsx')

d = parsers._parse_org1_docx('/home/ghost/Downloads/2014.09 CCDHRN.docx')
print 'Parsed REPORT'
print d['report']

print 'Parsed EVENTS'
for event in d['events']:
    print 'Actor name = ' + event.victims[0].name
    print 'Source name = ' + event.sources[0].name
    try:
        loc = event.locations[0]
        print 'Location = '
        print loc.name
    except IndexError: pass

print 'Done'
