#! /usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Author: Xihao Liang
Created: 2016.08.01
Description: a tool used to analyse emoticons on Weibo
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
import json

FNAME_EMO = '../data/emoticon.json'

def init_data():
	js = json.load(open(FNAME_EMO, 'r'))['data']

	emo_pairs = []
	emo_pairs.append(('usual', js['usual']['norm']))
	emo_pairs.extend(js['more'].items())

	collections = {}
	phrases = set()

	for name, infos in emo_pairs:
		ps = [info['phrase'][1:-1] for info in infos]

		collections[name] = ps
		phrases |= set(ps)

	pattern = re.compile(r'(\[(?:' + '|'.join(['(?:%s)'%(p) for p in set(phrases)])+ ')\])')

	return collections, pattern

collections, emotica = init_data()

if __name__ == '__main__':
	import zhprocessor

	t = u'你好泪 [泪] 我是 [泪] 梁錫豪'
	emos = emotica.findall(t)

	print '/'.join(emos)

