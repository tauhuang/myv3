# -*- coding: UTF-8 -8-


from job import disk, dpstat, osserver, t100
from tclient.config import BASE_URL
from tclient.util import merge_dicts
from tclient.feedback import HTTPPoster


def send():
    url = BASE_URL + '/uploaddata'
    data = merge_dicts(disk.get_data(),
                       dpstat.get_data(),
                       osserver.get_data(),
                       t100.get_data())

    poster = HTTPPoster(json=data, url=url)
    poster.post()