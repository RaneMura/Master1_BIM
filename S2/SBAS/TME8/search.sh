#!/bin/bash
mkdir searchResults95
mkdir searchResults30

export MODELS_PATH_95="hmmModels95" 
export MODELS_PATH_30="hmmModels30" 

#execute it in hmmModels directory
for FILE in $MODELS_PATH_95/*.hmm
do
        old=".hmm"
        new=".out"
        NAME_RES=${FILE//$old/$new}
        echo "Searching ${NAME_RES}"
        hmmsearch --domtblout ${NAME_RES} -E 1 ${FILE} scop/scopTestSeq.fasta > /dev/null
       
done

mv $MODELS_PATH_95/*.out searchResults95/

for FILE in $MODELS_PATH_30/*.hmm
do
        old=".hmm"
        new=".out"
        NAME_RES=${FILE//$old/$new}
        echo "Searching ${NAME_RES}"
        hmmsearch --domtblout ${NAME_RES} -E 1 ${FILE} scop/scopTestSeq.fasta > /dev/null
       
done

mv $MODELS_PATH_30/*.out searchResults30/

echo "Number of models 95"
ls -c $MODELS_PATH_95/ | wc -l

echo "Number of results 95"
ls -c searchResults95/ | wc -l

echo "Number of models 30"
ls -c $MODELS_PATH_30/ | wc -l

echo "Number of results 30"
ls -c searchResults30/ | wc -l
