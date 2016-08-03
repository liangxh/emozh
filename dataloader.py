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

import time
import numpy as np
np.random.seed(int(time.time() * 1e6) % (1 << 32) )

from utils import progbar

def load(fname_dataset, dir_tokid, valid = 0.2, test = 0.1):
	emo_ids = cPickle.load(open(fname_dataset, 'r'))

	dataset = [[[], []] for i in range(3)]

	def add_samples(idxs, lines, y, split_id):
		for idx in idxs:
			tids = map(int, lines[idx][:-1].split(' '))

			dataset[split_id][0].append(tids)
			dataset[split_id][1].append(y)
	
	print >> sys.stderr, 'load: [info] loading data...'
	pbar = progbar.start(len(emo_ids))
	
	for i, item in enumerate(emo_ids):
		emo, ids = item 

		n_total = len(ids)
		n_valid = int(valid * n_total)
		n_test = int(test * n_total)
		n_train = n_total - n_valid - n_test 

		fname_tokid = dir_tokid + '%s.txt'%(emo)
		# tids = load_tokid(fname_tokid)
		lines = open(fname_tokid, 'r').readlines()

		add_samples(ids[:n_train], lines, i, 0)
		add_samples(ids[n_train:(-n_test)], lines, i, 1)
		add_samples(ids[-n_test:], lines, i, 2)

		pbar.update(i + 1)
	pbar.finish()

	def shuffle(subset):
		x, y = subset
		ids = range(len(x))
		np.random.shuffle(ids)
		x = [x[i] for i in ids]
		y = [y[i] for i in ids]
		return (x, y)

	dataset = [shuffle(tuple(subset)) for subset in dataset]
	dataset = tuple(dataset)
	
	return dataset

def demo():
	dir_root = '../'
	fname_dataset = dir_root + 'dataset/7T300d50y20000.pkl'
	dir_tokid = dir_root + 'tokid/7T300d/'

	dataset = load(fname_dataset, dir_tokid)
	train, valid, test = dataset

	print len(train[0])
	print len(valid[0])
	print len(test[0])

if __name__ == '__main__':
	demo()
