from loadpackage import *
from tclient.feedback import HTTPPoster, Data


json_data = Data(status='failed', reason='download', log_id='123', erp_lic='TDAAAADV')
print json_data.json
http_poster = HTTPPoster(json=json_data.json)
print http_poster.json
http_poster.post()
