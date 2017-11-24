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
        #Collecting simple data
        return {
            "url": response.url,
            "Title": response.doc('title').text(),
            "Developer": response.doc('#developers_list > a').text(),
            "Score": response.doc('.high').text(),
            "Overall Reviews": response.doc('#review_histogram_rollup_section .positive').text(),
            "Price": response.doc('.price').text()
        }


    def filter_page(self, response):
        #Agecheck1 - click the button
        if re.match("http://store.steampowered.com/app/\d+/age\w+", response.url):
            self.crawl(response.url,
                               fetch_type='js', js_script="""function() {
                               HideAgeGate();
                   }
                   """,callback=self.detail_page)
        #Agecheck2 - Select birthday
        if re.match("http://store.steampowered.com/agecheck/app/\d+", response.url):
            self.crawl(response.url,
                               fetch_type='js', js_script="""function() {
                               $J('#ageYear').val(1980);
                                $J('#agecheck_form').submit();
                   }
                   """,callback=self.detail_page)
        #Normal access
        else:
            self.crawl(response.url, callback=self.detail_page)
            
    #iterates over steam's main page (no tags)
    #that will take a while...
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://store.steampowered.com/app/\d+/\w+", each.attr.href):
                self.crawl(each.attr.href, callback=self.filter_page)
        #next index page
        index = int(response.url[-1]) + 1
        response.url  = response.url[:-1] + str(index)
        self.crawl(response.url, callback=self.index_page)
