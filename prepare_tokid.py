#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.08.03
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import cPickle
import commands

from wordindexer import WordIndexer
from utils import progbar

def wc_l(fname):
	return int(commands.getoutput('wc -l %s'%(fname)).split(' ')[0])

def main():
	key_wemb = sys.argv[1]

	dir_root = '../'
	dir_corpus = dir_root + 'corpus/'
	dir_token = dir_root + 'token/'
	dir_tokid = dir_root + 'tokid/%s/'%(key_wemb)

	fname_wemb = dir_root + 'wemb/%s.txt'%(key_wemb)
	windexer = WordIndexer.load(fname_wemb)

	if not os.path.isdir(dir_tokid):
		os.mkdir(dir_tokid)

	fname_emo = dir_corpus + 'emo.txt'
	emos = open(fname_emo, 'r').read().decode('utf8').split('\n')[:-1]

	for emo in emos:
		fname_input = dir_token + '%s.txt'%(emo)
		fname_output = dir_tokid + '%s.txt'%(emo)
		
		print >> sys.stderr, 'main: [info] processing %s'%(fname_input)
		
		pbar = progbar.start(wc_l(fname_input))
		i = 0

		fobj_output = open(fname_output, 'w')
		with open(fname_input, 'r') as fobj_input:
			for line in fobj_input:
				toks = line[:-1].decode('utf8').split(' ')
				tids = windexer.seq2idx(toks)

				if len(tids) > 0:
					fobj_output.write(' '.join(map(str, tids)) + '\n')

				i += 1
				pbar.update(i)

		pbar.finish()	

if __name__ == '__main__':
	main()
