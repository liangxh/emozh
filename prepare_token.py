#! /usr/bin/env python
#-*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.08.02
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import commands

import zhtokenizer
from utils import progbar

def wc_l(fname):
	return int(commands.getoutput("wc -l %s"%(fname)).split(' ')[0])

def main():
	dir_root = '../'
	
	dir_data = dir_root + 'data/'
	dir_corpus = dir_root + 'corpus/'
	dir_token = dir_root + 'token/'

	fname_emo = dir_data + 'emo.txt'

	emos = open(fname_emo, 'r').read().decode('utf8').split('\n')[:-1]

	if not os.path.isdir(dir_token):
		os.mkdir(dir_token)
	
	for emo in emos:
		fname_output = dir_token + '%s.txt'%(emo)
		fname_input = dir_corpus + '%s.txt'%(emo)

		fobj_out = open(fname_output, 'w')
		with open(fname_input, 'r') as fobj_in:
			print >> sys.stderr, 'main: [info] processing %s'%(fname_input)

			pbar = progbar.start(wc_l(fname_input))
			i = 0

			for line in fobj_in:
				line = line[:-1].decode('utf8')
				toks = zhtokenizer.tokenize(line)
				fobj_out.write(' '.join(toks) + '\n')

				i += 1
				pbar.update(i)

			pbar.finish()

		fobj_out.close()	

if __name__ == '__main__':
	main()
