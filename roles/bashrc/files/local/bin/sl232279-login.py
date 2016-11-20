#!/usr/bin/env python
import httplib
import json
import pprint
import sys
import urllib
import urlparse
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument('-H', '--host', default='dal05', choices=('dal05', 'ams01', 'hkg02', 'sng01', 'lon02'), dest='host')
argParser.add_argument('verb', nargs='?', default='')
argParser.add_argument('path', nargs='?', default='')
argParser.add_argument('infile', nargs='?', type=argparse.FileType('r'))
args = argParser.parse_args()

print args

dal05 = httplib.HTTPSConnection(args.host + '.objectstorage.softlayer.net')
pp = pprint.PrettyPrinter(indent=4)

# Get authentication going
print 'Authenticating \t\t**********************'
headers = {
#        'X-Storage-User' : 'SLOS232279-1:SL232279',
#        'X-Storage-Pass' : '4b16c06c29feb8a28d25f976ab534cb7434e5f7ef6235b962faa6fa8b97c919a'
        'X-Storage-User' : 'SLOS193397-3:c0500thre',
        'X-Storage-Pass' : '5bd4064dd81472bcdc96753f4e760ac83cde3c48b89b7713209fec03b0695563'
        }
dal05.request('GET', '/auth/v1.0', None, headers)
authResponse = dal05.getresponse()
clusters = json.loads(authResponse.read())
basePath = urlparse.urlparse(authResponse.getheader('x-storage-url')).path

# Fetch container list
headers = {
    'X-Auth-Token' : authResponse.getheader('x-auth-token'),
    'Expect' : 'application/x-json'
}

if args.verb != '':
    print 'Executing user request \t**********************'
    print 'URL\t: %s' % (authResponse.getheader('x-storage-url'))
    print 'Headers\t:'
    pp.pprint(headers)
    print 'RESULTS \t\t*********************'
    if args.verb != 'PUT':
        dal05.request(args.verb, basePath + '/' + args.path, None, headers)
        getResponse = dal05.getresponse()
        print 'Response Code: %d' % (getResponse.status,)
        pp.pprint(getResponse.getheaders())
        print getResponse.read()
    else:
        inputFile = args.infile
        dal05.request('PUT', urllib.pathname2url(basePath + '/' + args.path), inputFile, headers)
        putResponse = dal05.getresponse()
        pp.pprint(putResponse.getheaders())
        print putResponse.read()
else:
    print 'URL\t: %s' % (authResponse.getheader('x-storage-url'))
    print 'Headers\t:'
    pp.pprint(headers)

