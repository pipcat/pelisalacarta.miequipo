# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para ustream
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

DEBUG = config.get_setting("debug")

def find_url_play(data, headers):
    logger.info("[ustream.py] find_url_play")

    cid = scrapertools.find_single_match (data, "ustream.vars.contentId=['\"]([^'\"]+)")
    #cid = scrapertools.find_single_match (data, "ustream.vars.channelId=['\"]([^'\"]+)")
    if cid == '':
        return ''

    url = 'http://iphone-streaming.ustream.tv/uhls/%s/streams/live/iphone/playlist.m3u8' % cid

    return url
