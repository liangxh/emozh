#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.08.12
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import db
import blogger
from utils import progbar

def main():
	con = db.connect()
	cur = con.cursor()

	emos = open('../output/emo_top100.txt', 'r').read().decode('utf8').split('\n')

	limit = int(sys.argv[1])
	pbar = progbar.start(limit)
	i = 0

	cur.execute("SELECT text FROM microblogs WHERE comments_count > 0 AND comments)count < 100 LIMIT %d"%(limit))

	fobjs = dict([(emo, open('../data/%s.txt', 'w'%(emo))) for emo in emos ])

	for res in cur:
		blog = res[0]
		text, emos = blogger.extract(blog)

		n_emo = len(emos)
		if n_emo > 0 and n_emo < 6:
			samples = blogger.prepare_sample(text, emos)
			for e, t in samples:
				if not e in fobjs:
					continue

				fobjs[e].write(t + '\n')
		
		i += 1
		pbar.update(i)
	pbar.finish()

	for fobj in fobjs.items():
		fobj.close()

if __name__ == '__main__':
	main()
