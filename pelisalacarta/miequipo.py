# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para miequipo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "miequipo"
__title__ = "Mi equipo"
__language__ = "ES"

DEBUG = config.get_setting("debug")

# Nombre del equipo del que se buscan los enlaces
MIEQUIPO = config.get_setting("miequipoprefe")

# Detección de enlaces en los siguientes servidores de deportes, ubicados en /serverssports/
SPORTS_SERVERS = ['lshstream', 'liveall', '04stream', 'iguide', 'ucaster', 'tashtv', 'ezcast', 'ustream']

DEFAULT_HEADERS=[]
DEFAULT_HEADERS.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"])
DEFAULT_HEADERS.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
DEFAULT_HEADERS.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])
DEFAULT_HEADERS.append(["Accept-Encoding","gzip, deflate"])


def isGeneric():
    return True

def mainlist(item):
    logger.info("[miequipo.py] mainlist")
    itemlist = []
    
    itemlist.append( Item(channel=__channel__, action="lshunter"    , title="LSHunter.tv"       , url="http://www.drakulastream.eu" ))
    itemlist.append( Item(channel=__channel__, action="firstrow"    , title="FirstRowSports.eu" , url="http://www.ifeed2all.eu/type/football.html" ))
    itemlist.append( Item(channel=__channel__, action="rojadirecta" , title="RojaDirecta.me"    , url="http://www.rojadirecta.me" ))

    return itemlist


def lshunter(item):
    logger.info("[miequipo.py] lshunter")
    itemlist = []
     
    data = scrapertools.cachePage(item.url,headers=DEFAULT_HEADERS)
    if (DEBUG): logger.info("data="+data)

    patron = '<!-- main container of a slide -->(.*?)<!-- close main container of a slide -->'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): logger.info("MATCHES="+str(len(matches)))

    for match in matches:
        scrapedtitle = scrapertools.find_single_match(match,'<span class="lshevent">([^<]+)</span>')
        if MIEQUIPO in scrapedtitle:
            if (DEBUG): logger.info("match="+match)

            matches2 = re.compile('<tr class="sectiontable([^"]+)">(.*?)</tr>',re.DOTALL).findall(match)
            for section,inner in matches2:
                if (DEBUG): logger.info("inner="+inner)
                if section == 'header':
                    section_name = scrapertools.find_single_match(inner,'<td>([^<]+)</td>')
                else:
                    #server_name = scrapertools.find_single_match(inner,'<img title="([^"]+)"')
                    server_name = scrapertools.find_single_match(inner,'<td width="80"><a>([^:]+)')
                    #matches3 = re.compile('<a href=\'javascript:openWindow\("([^"]+)"',re.DOTALL).findall(inner)
                    matches3 = re.compile('<a href=\'javascript:openWindow\("([^"]+)"',re.DOTALL | re.IGNORECASE).findall(inner)
                    for n, scrapedurl in enumerate(matches3):
                        desglose = scrapertools.find_single_match(scrapedurl,'event_id=([^&]+)&tv_id=([^&]+)&tid=([^&]+)&channel=([^&]+)&')
                        if len(desglose) == 4:
                            event_id,tv_id,tid,chan = desglose
                        else:
                            event_id,tid,chan = scrapertools.find_single_match(scrapedurl,'event_id=([^&]+)&tid=([^&]+)&channel=([^&]+)&')
                            tv_id = '0'
                        url = 'http://live.drakulastream.eu/static/popups/%s%s%s%s.html' % (event_id,tv_id,tid,chan)
                        titulo = section_name + ' [' + server_name + '~' + str(n+1) + ']'
                        if (DEBUG): logger.info("LINK: "+section_name+" : "+server_name+" : "+scrapedurl+" :: "+url)
                        itemlist.append( Item(channel=__channel__, action="play" , title=titulo , url=url))

            break

    return itemlist


def firstrow(item):
    logger.info("[miequipo.py] firstrow")
    itemlist = []

    data = scrapertools.cachePage(item.url,headers=DEFAULT_HEADERS)
    if (DEBUG): logger.info("data="+data)

    patron = '<h3>\s*<a> <img[^<]+<span[^<]+<span[^<]+</span> </span>([^<]+)</a> </h3> <div>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): logger.info("MATCHES="+str(len(matches)))

    for scrapedtitle,inner in matches:
        if (DEBUG): logger.info("scrapedtitle="+scrapedtitle)
        if MIEQUIPO in scrapedtitle:
            if (DEBUG): logger.info("inner="+inner)
            patron2 = "href='([^']+)'>([^<]+)</a>"
            matches2 = re.compile(patron2,re.DOTALL).findall(inner)
            for enlace,nombre in matches2:
                url = urlparse.urljoin(item.url, enlace)
                itemlist.append( Item(channel=__channel__, action="play" , title=nombre , url=url))
                if (DEBUG): logger.info("innerurl="+url)

    return itemlist


def rojadirecta(item):
    logger.info("[miequipo.py] rojadirecta")
    itemlist = []

    data = scrapertools.cachePage(item.url,headers=DEFAULT_HEADERS)
    if (DEBUG): logger.info("data="+data)

    patron = '<span itemprop="name">([^<]+)</span></b></div><!--[^<]+<span class="submenu" id="([^"]+)">'    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if (DEBUG): logger.info("MATCHES="+str(len(matches)))
    for scrapedtitle,scrapedid in matches:
        if (DEBUG): logger.info("scrapedtitle="+scrapedtitle)
        if MIEQUIPO in scrapedtitle:
            idtab = scrapedid.replace('sub','taboastreams')
            inner = scrapertools.find_single_match(data,'<table class="taboastreams" id="'+idtab+'"[^<]+<tbody>(.*?)</tbody>')
            if (DEBUG): logger.info("inner="+inner)

            patron2 = '<tr>\s*<td>NO</td>\s*<td>(?!bwin|bet365)([^<]*)</td>\s*<td>([^<]*)</td>\s*<td>([^<]*).*?</td>\s*<td>(.*?)</td>\s*<td>(?:<b>)?<a[^>]*href="([^"]+)"'
            matches2 = re.compile(patron2,re.DOTALL).findall(inner)
            for nombre,idioma,tipo,calidad,enlace in matches2:
                titulo = nombre + ' - ' + idioma + ' - ' + calidad.replace('<!--9000-->','').replace(' (<span class="es">e</span>stable)','') + ' kbps - ' + tipo
                url = enlace.replace('#www.rojadirecta.me','').replace('goto/','http://')
                itemlist.append( Item(channel=__channel__, action="play" , title=titulo , url=url))

    return itemlist


def play(item):
    logger.info("[miequipo.py] play")
    itemlist = []
    url = ''

    data = scrapertools.cachePage(item.url,headers=DEFAULT_HEADERS)
    if (DEBUG): logger.info("data="+data)

    # unescape de posible código javascript "oculto"
    patronjs = "unescape\s*\(\s*['\"]([^'\"]+)"
    matches = re.compile(patronjs,re.DOTALL).findall(data)
    for ofuscado in matches:
        data = data.replace(ofuscado, urllib.unquote(ofuscado))
    #if (DEBUG): logger.info("datanoofus="+data)

    headers = DEFAULT_HEADERS[:]
    headers.append(["Referer",item.url])

    # Ejecuta find_url_play en cada servidor hasta encontrar una url
    for serverid in SPORTS_SERVERS:
        try:
            servers_module = __import__("serverssports."+serverid)
            server_module = getattr(servers_module,serverid)
            url = server_module.find_url_play(data, headers)
            if url != '':
                break
        except ImportError:
            logger.info("No existe conector para "+serverid)
        except:
            logger.info("Error en el conector "+serverid)
            import traceback,sys
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)


    if url != '':
        itemlist.append( Item(channel=__channel__, title=item.title , url=url, server='directo'))
    else:
        logger.info("NO DETECTADO SERVIDOR")

    return itemlist

