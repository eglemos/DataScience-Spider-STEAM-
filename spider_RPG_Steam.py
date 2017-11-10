#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-09 11:12:50
# Project: steam_project



from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }
    #starting URL: RPG section from steam site.
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://store.steampowered.com/search/?tags=122', callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    #iterates over the RPG section from steam site.
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://cdn.akamai.steamstatic.com/steam/apps/\d+/$", each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
	#takes the last byte from the url string and adds 1. The result is the next page.        
	index = int(response.url[-1]) + 1
        response.url  = response.url[:-1] + str(index)
	#recursive
        self.crawl(response.url, callback=self.index_page)
