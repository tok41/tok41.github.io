#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'tok41'
SITENAME = u'41 LOG'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = u'ja'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/yoichi_t'),
          ('Github', 'https://github.com/tok41'),)

#Twitter
TWITTER_USERNAME = 'yoichi_t'

# 
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_FEEDS_ON_MENU = True

#
#DISQUS_SITENAME = '41log'


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images', 'pdfs']

# Theme
#THEME = './pelican-octopress-theme-master'
#THEME = './themes/pelican-themes/gum'
#THEME = './themes/pelican-themes/bootstrap2'
#THEME = './themes/nice-blog'
SIDEBAR_DISPLAY = ['about', 'categories', 'tags']
SIDEBAR_ABOUT = '主に覚えたての技術についてのメモを残すためのブログです。知らないこと覚えたてのことを書いていくので、おのずと初心者目線で書いていきます。'
THEME = './themes/pelican-elegant'

