#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.08.01
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import cPickle

import db
import blogger
from utils import progbar

TOTAL = 156365006

def main():
	con = db.connect()
	cur = con.cursor()
	
	emo_mids = {}

	limit = 25000000
	pbar = progbar.start(limit)
	i = 0

	cur.execute("SELECT mid, text FROM microblogs WHERE comments_count > 0 AND comments_count < 100 LIMIT %d"%(limit))
	for mid, text in cur:
		text, emos = blogger.extract(text)
		
		if len(emos) > 0 and len(emos) < 6:
			samples = blogger.prepare_sample(text, emos)
			for e, t in samples:
				if emo_mids.has_key(e):
					emo_mids[e].append(mid)
				else:
					emo_mids[e] = [mid, ]

		i += 1
		pbar.update(i)

	pbar.finish()

	cPickle.dump(emo_mids, open('../output/emo_mids.pkl', 'w'))

if __name__ == '__main__':
	main()
