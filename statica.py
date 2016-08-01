#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.08.01
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import db
import blogger
from utils import progbar

TOTAL = 156365006

def main():
	con = db.connect()
	cur = con.cursor()
	
	emo_mids = {}

	pbar = progbar.start(TOTAL)
	i = 0

	cur.execute("select mid, text from microblogs limit 1")
	for mid, text in cur:
		text, emos = blogger.extract(text)
		
		if len(emos) > 0:
			samples = blogger.prepare_sample(text, emos)
			for e, t in samples:
				if emo_mids.has_key(e):
					emo_mids[e] += 1
				else:
					emo_mids[e] = 1

		i += 1
		pbar.update(i)

	pbar.finish(i)

	cPickle.dump(emo_mids, open('../output/emo_mids.pkl', 'w'))

if __name__ == '__main__':
	main()
