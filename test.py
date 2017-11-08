#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-08 11:30:41
# Project: imbd

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.imdb.com/search/title?count=100&title_type=feature,tv_series,tv_movie&ref_=nv_ch_mm_1', callback=self.index_page)

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
            if re.match("http://www.imdb.com/title/tt\d+/$", each.attr.href):
                self.crawl(each.attr.href, callback = self.detail_page)
        self.crawl(response.doc('.next-page').attr.href, callback = self.index_page)
