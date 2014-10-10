from parsedom import parseDOM
import urllib2
import re

try: import simplejson as json
except ImportError: import json


response = urllib2.urlopen('http://www.cinemargentino.com/category/type/fiction')
link_html = response.read()
ret = parseDOM(link_html, "a", attrs = { "class": "title" }, ret = "href")
print ret

for link in ret:
  response = urllib2.urlopen('http://www.cinemargentino.com' + link)
  link_html = response.read()

  ret = parseDOM(link_html, "iframe", attrs = { "id": "cinemargentinoplayer" }, ret = "src")

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

    if h264.get("hd"):
      video['isHD'] = "1"
      video['video_url'] = h264["hd"]["url"]
    else:
      video['video_url'] = h264["sd"]["url"]

    print h264.get("hd")
    print video['video_url']
    print video['Title']
