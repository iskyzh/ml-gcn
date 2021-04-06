#!/bin/bash

for i in {1..100}
do
	rm -rf cache/run/
	./run.sh
	python src/train.py
	./save.sh
	./submit.sh "GCN trial ${i}"
done

