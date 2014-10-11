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

import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin

import urllib2
import re
import CommonFunctions as common

try: import simplejson as json
except ImportError: import json

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

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

    response = urllib2.urlopen('http://www.cinemargentino.com/category/type/%s' % foldername)
    link_html = response.read()
    ret = common.parseDOM(link_html, "a", attrs = { "class": "title" }, ret = "href")

    for link in ret:
      response = urllib2.urlopen('http://www.cinemargentino.com' + link)
      link_html = response.read()
      ret = common.parseDOM(link_html, "iframe", attrs = { "id": "cinemargentinoplayer" }, ret = "src")

      m = re.search("([0-9]{4,})", ret[0])

      if m:
        request = urllib2.Request('http://player.vimeo.com/video/%s/config' % m.groups(1), headers={"Referer":"http://www.cinemargentino.com/"})

        collection = json.loads(urllib2.urlopen(request).read())
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
    
        #if h264.get("hd"):
        #  video['isHD'] = "1"
        #  video['video_url'] = h264["hd"]["url"]
        #else:
        #  video['video_url'] = h264["sd"]["url"]
        video['video_url'] = h264["sd"]["url"]
  
        url=video['video_url']
    
  
        li = xbmcgui.ListItem(video['Title'], iconImage='DefaultVideo.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
  
    xbmcplugin.endOfDirectory(addon_handle)
