all: plugin.video.cinemargentino.zip

plugin.video.cinemargentino.zip: plugin.video.cinemargentino/addon.xml plugin.video.cinemargentino/default.py plugin.video.cinemargentino/icon.png plugin.video.cinemargentino/fanart.jpg
	zip plugin.video.cinemargentino.zip plugin.video.cinemargentino/addon.xml plugin.video.cinemargentino/default.py plugin.video.cinemargentino/icon.png plugin.video.cinemargentino/fanart.jpg

