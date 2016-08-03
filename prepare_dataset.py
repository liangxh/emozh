#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.08.03
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import commands
import cPickle

import time
import numpy as np
np.random.seed(int(time.time() * 1e6) % (1 << 32))

from utils import progbar

def wc_l(fname):
	return int(commands.getoutput('wc -l %s'%(fname)).split(' ')[0])

def main():
	key_wemb = sys.argv[1]
	ydim = int(sys.argv[2])
	size = int(sys.argv[3])
	key_dataset = key_wemb + '%dy%d'%(ydim, size)

	dir_root = '../'
	dir_tokid = dir_root + 'tokid/%s/'%(key_wemb)
	dir_dataset = dir_root + 'dataset/'

	fname_dataset = dir_dataset + '%s.pkl'%(key_dataset)

	fname_emo = dir_tokid + 'emo.txt'
	emos = open(fname_emo, 'r').read().decode('utf8').split('\n')[:-1]
	dataset = []

	pbar = progbar.start(ydim)
	i = 0
	for emo in emos[:ydim]:
		fname_input = dir_tokid + '%s.txt'%(emo)
		ids = range(wc_l(fname_input))
		np.random.shuffle(ids)
		dataset.append((emo, ids[:size]))

		i += 1
		pbar.update(i)

	pbar.finish()

	cPickle.dump(dataset, open(fname_dataset, 'w'))

if __name__ == '__main__':
	main()
