# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 19:50:28 2019

@author: Dorian
"""

#What does SUBJ look like?
# il faut savoir s'il a un predicat "image"

import urllib.request as url

if __name__ == "__main__":
    url.urlretrieve("http://commons.wikimedia.org/wiki/Special:FilePath/Okonjima%20Lioness.jpg", "00000001.jpg")