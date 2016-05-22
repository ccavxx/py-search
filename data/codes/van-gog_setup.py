#!/usr/bin/env python# -*- coding: utf-8 -*-"""Copyright (c) 2015, Ivan Lalashkov.Permission is hereby granted, free of charge, to any person obtaining a copyof this software and associated documentation files (the "Software"), to dealin the Software without restriction, including without limitation the rightsto use, copy, modify, merge, publish, distribute, sublicense, and/or sellcopies of the Software, and to permit persons to whom the Software isfurnished to do so, subject to the following conditions:The above copyright notice and this permission notice shall be included inall copies or substantial portions of the Software.THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS ORIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THEAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHERLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS INTHE SOFTWARE."""#from distutils.core import setupfrom setuptools import setupimport codecsimport os
def read(fname): return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
NAME = 'rutracker.py'VERSION = '1.0.0'DESCRIPTION = 'Command-line tool that downloads torrent files from Rutracker.org.'AUTHOR = 'Ivan Lalashkov'AUTHOR_EMAIL = 'lalashkov.ivan@gmail.com'URL = 'https://github.com/van-gog/rutracker.py'
setup( name=NAME, version=VERSION, description=DESCRIPTION, author=AUTHOR, author_email=AUTHOR_EMAIL, license='MIT', url=URL, py_modules=['rutracker'], entry_points={ 'console_scripts': [ 'rutracker=rutracker:main'        ]    })