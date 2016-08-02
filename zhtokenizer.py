#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.02.09
Description: functions for cutting sentences into unigrams or tokens, specifically for chinese based text
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re

import jieba
from jieba import posseg

jieba.initialize()

"""
def segment(text, pos_tagging = False):
	if pos_tagging:
		return posseg.cut(text)
	else:
		return jieba.cut(text)
"""

def unigramize(text):
	'''
	turn 'hi, 你好' into ['hi', '你', '好']
	'''
	text = text.decode('utf8').lower()
	grams = []
		
	buf = ''
	for t in text:
		if t >= 'a' and t <= 'z':
			# merge the english words
			buf += t
			continue

		if not buf == '':
			grams.append(buf)
			buf = ''
			
		if not t == ' ':
			grams.append(t)

	return grams

def tokenize(text):
	toks = [t.word for t in posseg.cut(text) if t.word is not ' ']
	
	return toks

if __name__ == '__main__':
	text = '还我八号风球！！！！hello八号风球挂了一个晚上，偏偏要上班的时候没有了！！！今天还要上班！！！噩耗！！！[泪][泪][泪]'

	grams = unigramize(text)
	print '/'.join(grams)
	print 
	
	tokens = tokenize(text)
	print '/'.join(tokens)
	print

