#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.08.02
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import commands

import blogger
from utils import progbar

def wc_l(fname):
	return int(commands.getoutput("wc -l %s"%(fname)).split(' ')[0])

def main():
	dir_root = '../'
	dir_output = dir_root + 'corpus/'
	dir_input = dir_root + 'corpus_raw/'

	fname_emo = dir_input + 'emo.txt'
	emos = open(fname_emo, 'r').read().decode('utf8').split('\n')[:-1]

	if not os.path.isdir(dir_output):
		os.mkdir(dir_output)

	for emo in emos:
		fname_input = dir_input + '%s.txt'%(emo)
		fname_output = dir_output + '%s.txt'%(emo)

		print >> sys.stderr, 'main: [info] processing %s'%(fname_input)

		fobj_output = open(fname_output, 'w')

		print fname_input
		pbar = progbar.start(wc_l(fname_input))
		i = 0

		sents = set()

		with open(fname_input, 'r') as fobj_input:
			for line in fobj_input:
				line = line.decode('utf8')
				
				if blogger.contain_zh(line) and not line in sents:
					fobj_output.write(line)
					sents.add(line)
			
				i += 1
				pbar.update(i)

		pbar.finish()

if __name__ == '__main__':
	main()
