#!/bin/bash


export ALN_PATH_95="scop/scop95/aln" 
export ALN_PATH_30="scop/scop30/aln"


mkdir hmmModels95
for FILE in $ALN_PATH_95/*.sto; do
	old=".aln.sto"
	new=".hmm"
	NAME_HMM=${FILE/$old/$new}
	echo "Building ${NAME_HMM}"
	
	echo "hmmbuild ${NAME_HMM} ${FILE}"
	hmmbuild ${NAME_HMM} ${FILE} > /dev/null


done

mv $ALN_PATH_95/*.hmm hmmModels95/

mkdir hmmModels30
for FILE in $ALN_PATH_30/*.sto; do
	old=".aln.sto"
	new=".hmm"
	NAME_HMM=${FILE/$old/$new}
	echo "Building ${NAME_HMM}"
	
	echo "hmmbuild ${NAME_HMM} ${FILE}"
	hmmbuild ${NAME_HMM} ${FILE} > /dev/null

done

mv $ALN_PATH_30/*.hmm hmmModels30/

echo "Number of aln 95"
ls -c $ALN_PATH_95/ | wc -l

echo "Number of models 95"
ls -c hmmModels95/ | wc -l

echo "Number of aln 30"
ls -c $ALN_PATH_30/ | wc -l

echo "Number of models 30"
ls -c hmmModels30/ | wc -l
