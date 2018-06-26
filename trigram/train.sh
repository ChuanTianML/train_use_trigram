#!/bin/bash

VOC_SIZE=100
CORPUS_PATH=demo_corpus.txt
VOC_PATH=./model/vocab.txt
TRIGRAM_PATH=./model/trigram.pkl

time python vocab.py -iPath $CORPUS_PATH -oPath $VOC_PATH  -vocSize $VOC_SIZE
time python trigram.py -iPath $CORPUS_PATH -vocPath $VOC_PATH -triGramPath $TRIGRAM_PATH 

