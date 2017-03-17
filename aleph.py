import requests

req = requests.get('https://aleph.openoil.net/aleph_api/1/query', params={'apikey': 'oo_69gdmctw5mejvs8jl', 'archive_url':c})

for result in req.json()['results']:
    print(result['title'])
