all: plugin.video.cinemargentino.zip

plugin.video.cinemargentino.zip: plugin.video.cinemargentino/addon.xml plugin.video.cinemargentino/default.py
	zip plugin.video.cinemargentino.zip plugin.video.cinemargentino/addon.xml plugin.video.cinemargentino/default.py

