# -*- coding: utf-8 -*-
import os
from pyltp import SentenceSplitter
from pyltp import Segmentor

# ltp model's catalogue
LTP_DATA_DIR = 'D:\Python\安装包\3.4'

# cws model's catalogue
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')

segmentor = Segmentor()
segmentor.load("D:\\Python\\3.4\\cws.model")
words = segmentor.segment('我其实想说你这样做有点不太好')
print('\t'.join(words))
segmentor.release()

sentences = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')  # 分句
print('\n'.join(sentences))
