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
        self.crawl('http://store.steampowered.com/search/?page=1', callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        #TODO - agecheck bypass
        #if re.match("http://store.steampowered.com/app/\d+/agecheck\w+", response.url):
        #Collecting simple data
        return {
            "url": response.url,
            "Title": response.doc('title').text(),
            "Developer": response.doc('#developers_list > a').text(),
            "Score": response.doc('.high').text(),
            "Overall Reviews": response.doc('#review_histogram_rollup_section .positive').text(),
            "Price": response.doc('.price').text()
        }

    #iterates over steam's main page (no tags)
    #that will take a while...
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://store.steampowered.com/app/\d+/\w+", each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        #next index page
        index = int(response.url[-1]) + 1
        response.url  = response.url[:-1] + str(index)
        self.crawl(response.url, callback=self.index_page)
