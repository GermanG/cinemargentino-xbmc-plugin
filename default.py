'''
    Cinemargentino XBMC Plugin
    Copyright (C) 2014 GermanG

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# This code is based on audio/video example, vimeo plugin and crackle2fg plugin, thanks!

import xbmcgui, xbmcplugin

import urllib2, urllib, re, sys, urlparse

import CommonFunctions as common
import StorageServer

try: import simplejson as json
except ImportError: import json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

# cache
cache = StorageServer.StorageServer("cinemargentino", 8)


def get_url(url, http_headers=None):
    if http_headers:
       request = urllib2.Request(url, headers=http_headers)
    else:
       request = urllib2.Request(url)
        
    return urllib2.urlopen(request).read()

# Remove HTML codes (stolen from crackle2fg code, thanks!)
def cleanHtml(dirty):
    clean = re.sub('&quot;', '\"', dirty)
    clean = re.sub('&#039;', '\'', clean)
    clean = re.sub('&#215;', 'x', clean)
    clean = re.sub('&#038;', '&', clean)
    clean = re.sub('&#8216;', '\'', clean)
    clean = re.sub('&#8217;', '\'', clean)
    clean = re.sub('&#8211;', '-', clean)
    clean = re.sub('&#8220;', '\"', clean)
    clean = re.sub('&#8221;', '\"', clean)
    clean = re.sub('&#8212;', '-', clean)
    clean = re.sub('&amp;', '&', clean)
    clean = re.sub("`", '', clean)
    clean = re.sub('<em>', '[I]', clean)
    clean = re.sub('</em>', '[/I]', clean)
    return clean

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = build_url({'mode': 'folder', 'foldername': 'fiction'})
    li = xbmcgui.ListItem('Fiction', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'documentary'})
    li = xbmcgui.ListItem('Documentary', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'shortfilms'})
    li = xbmcgui.ListItem('Short Films', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]

    link_html = cache.cacheFunction(get_url, 'http://www.cinemargentino.com/category/type/%s' % foldername )

    ret = common.parseDOM(link_html, "div", attrs = { "class": "movie_list_cell" })

    for entry in ret:

      thumb_t = common.parseDOM(entry, "a", attrs = { "class": "subtitle_marker"})
      thumbnail = common.parseDOM(thumb_t, "img", ret = "src")

      entry_info = common.parseDOM(entry, "div", attrs = { "class": "movie_list_cell_info" })

      link = common.parseDOM(entry_info, "a", attrs = { "class": "title" }, ret = "href")[0]
      title = common.parseDOM(entry_info, "a", attrs = { "class": "title" })[0]
      author = common.parseDOM(entry_info, "h3")[0]
      date = common.parseDOM(entry_info, "h4")[0].split('|')[1]
      duration = common.parseDOM(entry_info, "h4")[0].split('|')[2]

      folder = cleanHtml(title) + ' ( ' + cleanHtml(author) + ' | ' + date + ') ' + duration
      url = build_url({'mode': 'link', 'link': link})
      li = xbmcgui.ListItem(folder, iconImage='DefaultFolder.png', thumbnailImage=thumbnail[0])
      xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                  listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'link':
    link = urllib.unquote_plus(args['link'][0])
    link_html = cache.cacheFunction(get_url, 'http://www.cinemargentino.com' + link )

    ret = common.parseDOM(link_html, "iframe", attrs = { "id": "cinemargentinoplayer" }, ret = "src")

    m = re.search("([0-9]{4,})", ret[0])

    if m:
      request = get_url('http://player.vimeo.com/video/%s/config' % m.groups(1), {"Referer":"http://www.cinemargentino.com/"})

      collection = json.loads(request)
      h264 = collection["request"]["files"]["h264"]

      video = {}
      video['videoid'] = m.groups(1)
      video['Title'] = collection["video"]["title"]
      video['Duration'] = "0"
      video['thumbnail'] = ""
      video['Studio'] = ""
      video['request_signature'] = ""
      video['request_signature_expires'] = ""
      video['urls'] = h264
  
      li = xbmcgui.ListItem('SD | ' + video['Title'], iconImage='DefaultVideo.png')
      xbmcplugin.addDirectoryItem(handle=addon_handle, url=h264["sd"]["url"], listitem=li)

      if h264.get("hd"):
        li = xbmcgui.ListItem('HD | ' + video['Title'], iconImage='DefaultVideo.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=h264["hd"]["url"], listitem=li)

  
  
  
    xbmcplugin.endOfDirectory(addon_handle)
