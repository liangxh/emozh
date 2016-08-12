#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.06.28
'''

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import traceback

import cPickle
import json
import urllib
import urllib2
from optparse import OptionParser
from flask import Flask, request, make_response, send_from_directory
from functools import wraps

sys.path.append('..')

from recomia import EmojiRecommender
recommender = None

def load_emojiurl():
	emoji_url = {}
	with open('../data/emoji_urls.txt', 'r') as fobj:
		for line in fobj:
			params = line[:-1].split(' ')
			k = params[0].decode('utf8')
			v = params[1]
			emoji_url[k] = y

	return emoji_url

emoji_url = load_emojiurl

import re
pattern_en = re.compile('[a-zA-Z]+')

def allow_cross_domain():
	def wrapper(fn):
		@wraps(fn)
		def _enable_cors(*args, **kwargs):
			rst = make_response(fn(*args, **kwargs))
			rst.headers['Access-Control-Allow-Origin'] = '*'
			rst.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
			rst.headers['Access-Control-Allow-Headers'] = 'Referer,Accept,Origin,User-Agent'
			return rst
		return _enable_cors
	return wrapper

default_host = '0.0.0.0'
default_port = 8000

app = Flask('NoticeBoard', static_url_path = '')

@app.route('/static/<dtype>/<fname>', methods = ['GET'])
def get_static(dtype, fname):
	dname = {'html':'demo/html/',
		'js':'demo/js/',
		'img':'demo/img/',
		}[dtype]

	if os.path.exists(os.path.join(dname, fname)):
		return send_from_directory(dname, fname)
	else:
		return '%s not found'%(fname)


@app.route('/recommend', methods = ['GET'])
def predict():
	if request.method == 'GET':
		try:
			params = request.args
			text = params.get('text')
			
			res = recommender.recommend(text)

			for ri in res:
				ri['url'] = emoji_url[ri['emoji']]

			return json.dumps({'status':0, 'res':res})
		except:
			print traceback.format_exc()
			return json.dumps({'status':1})

def main():
	optparser = OptionParser()
	optparser.add_option('-i', '--host', action='store', type='str', dest='host', default=default_host)
	optparser.add_option('-t', '--port', action='store', type='int', dest='port', default=default_port)

	optparser.add_option('-p', '--prefix', action='store', dest='prefix')
	optparser.add_option('-s', '--dataset', action='store', dest='key_dataset')
	optparser.add_option('-e', '--embed', action='store', dest='key_embed')
	
	opts, args = optparser.parse_args()

	prefix = opts.prefix

	dir_exp = '../'
	fname_dataset = dir_exp + 'dataset/%s.pkl'%(opts.key_dataset)
	fname_embed = dir_exp + 'wemb/%s.txt'%(opts.key_embed)
	fname_model = dir_exp + 'model/%s'%(opts.prefix)

	global recommender
	recommender = EmojiRecommender(fname_model, fname_embed, fname_dataset)

	app.run(host = opts.host, port = opts.port, debug = True, threaded = True)

if __name__ == '__main__':
	main()
