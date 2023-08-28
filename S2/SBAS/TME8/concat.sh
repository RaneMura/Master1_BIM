#!/bin/bash

cat searchResults95/*.out > allRes_95.txt
sed '/^#/d' allRes_95.txt > allRes_95.txt.ftt
cat allRes_95.txt.ftt | awk '{print $1" "$4" "$12}' > allRes_95.txt.ftt.2
sed -i -e 's/\.aln//g' allRes_95.txt.ftt.2
mv allRes_95.txt.ftt.2 allRes_95.txt.ftt

rm allRes_95.txt

echo "allRes_95.txt.ftt done"

cat searchResults30/*.out > allRes_30.txt
sed '/^#/d' allRes_30.txt > allRes_30.txt.ftt
cat allRes_30.txt.ftt | awk '{print $1" "$4" "$12}' > allRes_30.txt.ftt.2
sed -i -e 's/\.aln//g' allRes_30.txt.ftt.2
mv allRes_30.txt.ftt.2 allRes_30.txt.ftt

rm allRes_30.txt

echo "allRes_30.txt.ftt done"

