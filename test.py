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

import urllib2, urllib, re, sys, urlparse

from parsedom import parseDOM

try: import simplejson as json
except ImportError: import json

base_url = 'x'
#addon_handle = int(sys.argv[1])
#args = urlparse.parse_qs(sys.argv[2][1:])

def get_url(url, http_headers=None):
    if http_headers:
       request = urllib2.Request(url, headers=http_headers)
    else:
       request = urllib2.Request(url)
        
    return urllib2.urlopen(request).read()
    

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

# mode = args.get('mode', None)
mode = ['link']

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
    foldername = 'fiction'

    link_html = get_url('http://www.cinemargentino.com/category/type/%s' % foldername )

    #ret = parseDOM(link_html, "a", attrs = { "class": "title" }, ret = "href")
    ret = parseDOM(link_html, "div", attrs = { "class": "movie_list_cell" })

    for entry in ret:
      #link_html = get_url('http://www.cinemargentino.com' + link )

      print entry
      thumb_t = parseDOM(entry, "a", attrs = { "class": "subtitle_marker"})
      thumbnail = parseDOM(thumb_t, "img", ret = "src")
      print "==============================================================="
      print thumbnail
      print "==============================================================="
      entry_info = parseDOM(entry, "div", attrs = { "class": "movie_list_cell_info" })
      print entry_info
      link = parseDOM(entry_info, "a", attrs = { "class": "title" }, ret = "href")[0]
      title = parseDOM(entry_info, "a", attrs = { "class": "title" })[0]
      author = parseDOM(entry_info, "h3")[0]
      date = parseDOM(entry_info, "h4")[0].split('|')[1]
      duration = parseDOM(entry_info, "h4")[0].split('|')[2]
      print link
      folder = title + ' ( ' + author + ' | ' + date + ') ' + duration
      url = build_url({'mode': 'link', 'link' : link })

      m = 0

elif mode[0] == 'link':
      link='/films/914988457-como-estar-muerto-como-estar-muerto'
      link_html = get_url('http://www.cinemargentino.com' + link )
      ret = parseDOM(link_html, "iframe", attrs = { "id": "cinemargentinoplayer" }, ret = "src")
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
    
        #if h264.get("hd"):
        #  video['isHD'] = "1"
        #  video['video_url'] = h264["hd"]["url"]
        #else:
        #  video['video_url'] = h264["sd"]["url"]
        video['video_url'] = h264["sd"]["url"]
  
        url=video['video_url']
        print url
    
  
        #li = xbmcgui.ListItem(video['Title'], iconImage='DefaultVideo.png')
  
