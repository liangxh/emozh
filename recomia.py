#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.07.18
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import cPickle
import nltk
from optparse import OptionParser

from utils import emojicoder
from wordindexer import WordIndexer
from classifier import Classifier


class EmojiRecommender():
	def __init__(self, fname_model, fname_embed, fname_dataset):
		print >> sys.stderr, 'EmojiRecommender: [info] loading word index...'
		self.windexer = WordIndexer.load(fname_embed)
	
		print >> sys.stderr, 'EmojiRecommender: [info] loading model...'		
		self.clf = Classifier()
		self.clf.load_model(fname_model)

		print >> sys.stderr, 'EmojiRecommender: [info] loading emojis...'
		ecode_split = cPickle.load(open(fname_dataset, 'r'))
		self.emojis = [emojicoder.decode(ecode) for ecode, split in ecode_split]

		self.ydim = len(self.emojis)

		print >> sys.stderr, 'EmojiRecommender: [info] initialization done'

	def preprocess(self, text):
		text = text.decode('utf8')
		seq = [t.lower() for t in nltk.word_tokenize(text)]
		idxs = self.windexer.seq2idx(seq)

		return idxs

	def predict_proba(self, text):
		idxs = self.preprocess(text)
		
		if len(idxs) == 0:
			return None
		else:
			return self.clf.predict_proba(idxs)

	def recommend(self, text, n = 5):
		proba = self.predict_proba(text)

		if proba is None:
			eids = [i for i in range(n)]
			scores = [0. for i in range(n)]
		else:
			ranks = [(i, proba[i]) for i in range(self.ydim)]
			ranks = sorted(ranks, key = lambda k:-k[1])

			eids = [ranks[i][0] for i in range(n)]
			scores = [ranks[i][1] for i in range(n)]

		res = [{'emoji':self.emojis[eid], 'score':'%.2f'%(score)} for eid, score in zip(eids, scores)]

		return res

def main():
	optparser = OptionParser()

	optparser.add_option('-x', '--exp_name', action='store', dest='exp_name')
	optparser.add_option('-e', '--embed', action='store', dest='key_embed')
	optparser.add_option('-s', '--dataset', action='store', dest='key_dataset')
	optparser.add_option('-p', '--prefix', action='store', dest='prefix')	

	opts, args = optparser.parse_args()

	prefix = opts.prefix
	dir_exp = '/data/lxh/exp/%s/'%(opts.exp_name)

	fname_dataset = dir_exp + 'dataset/%s.pkl'%(opts.key_dataset)
	fname_embed = dir_exp + 'wemb/' + '%s.txt'%(opts.key_embed)
	fname_model = dir_exp + 'model/' + '%s'%(prefix)

	recommender = EmojiRecommender(fname_model, fname_embed, fname_dataset)
	
	n = 5

	print 'Welcome - lxh'
	print '==========================================================='
	while True:
		text = raw_input('Say Something: ')
		if text == '.exit':
			break
		
		res = recommender.recommend(text, n)
		print '\t/'.join([item['emoji'] for item in res])

	print '==========================================================='
	print 'Byebye~ :)'	

if __name__ == '__main__':
	main()
