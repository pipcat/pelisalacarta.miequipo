# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para tashtv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[tashtv.py] find_url_play")

    pageurl = scrapertools.find_single_match (data, '<iframe src="(http://www.tashtv.net/[^"]+)')
    if pageurl == '':
        return ''

    data2 = scrapertools.cachePage(pageurl, headers=headers)
    if (DEBUG): logger.info("data2="+data2)

    headers.pop()
    headers.append(["Referer",pageurl])

    servers_module = __import__("serverssports.ucaster")
    server_module = getattr(servers_module,'ucaster')
    return server_module.find_url_play(data2, headers)

