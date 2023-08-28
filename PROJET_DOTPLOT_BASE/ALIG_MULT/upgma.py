import numpy as np

def readmatrix(nomFi):
	mat=[]
	infile=open(nomFi,'r')
	for line in infile:
		mat.append(line.split())
	indices=mat[0]
	del(mat[0])
	npmat=np.array(mat)
	npmat=npmat.astype(int)
	for i in range(len(npmat)):
		npmat[i,i]=1000
			
	return indices,npmat
	
def trouvermin(mat):
	ind=np.unravel_index(np.argmin(mat, axis=None), mat.shape)
	return ind

def MAJnewick(a,b,dist):
	return '('+a+':'+str(dist/2)+','+b+':'+str(dist/2)+')'


def afficherArbre(groupes,mat):
	mat2=np.copy(mat)
	groupes2=list(groupes)

	while len(groupes2)>1:
		newrow=[]
		m=trouvermin(mat2)
		
		m1=min(m)
		m2=max(m)

		dist=mat2[m1,m2]
		
		w1=1
		w2=1
		for i in groupes[m[0]]:
			if i==',':
				w1+=1
		for i in groupes[m[1]]:
			if i==',':
				w2+=1

			
		for i in range(len(mat2)):
			if i!=m[0] and i!=m[1]:
				newrow.append( ( mat2[i,m[0]]*w1 + mat2[i,m[1]]*w2 ) / (w1+w2) )


		newrow2=np.empty((1,len(mat2)-2))
		newrow2[0]=newrow
		newlabel=MAJnewick(groupes2[m1],groupes2[m2],dist)
		mat2=np.delete(mat2,m2,0)
		mat2=np.delete(mat2,m1,0)
		mat2=np.delete(mat2,m2,1)
		mat2=np.delete(mat2,m1,1)
		del(groupes2[m2])
		del(groupes2[m1])
		groupes2.append(newlabel)
		mat2=np.concatenate((mat2,newrow2),axis=0)
		newrow.append(1000)
		newrow2=np.empty((1,len(mat2)))
		newrow2[0]=newrow
		mat2=np.concatenate((mat2,np.transpose(newrow2)),axis=1)

	return groupes2[0]
		

		
		
		
groupes,mat=readmatrix("matdist.txt")

arbre=afficherArbre(groupes,mat)
print(arbre)
	
	

