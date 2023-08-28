import psycopg2
region = input("ou ?")
conn = psycopg2.connect("dbname=ranepoly")

cur = conn.cursor()

cur.execute("SELECT * FROM populations WHERE nom_region = '"+region+"'")

res = cur.fetchall()

conn.close()

print(res)

for ppl in res:
	(pid,pop,loc) = ppl
	print("Population id : "+pid+" | Population name :  "+pop+" | Region : "+loc)

