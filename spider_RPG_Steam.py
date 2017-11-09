#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-09 11:12:50
# Project: steam_project

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://store.steampowered.com/search/?tags=122&page=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://cdn.akamai.steamstatic.com/steam/apps/\d+/$", each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        index = int(response.url[-1]) + 1
        response.url  = response.url[:-1] + str(index)
        self.crawl(response.url, callback=self.detail_page)
