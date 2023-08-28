def logistic4(x1,x2,r,n):

    xValues1 = [x1]
    xValues2 = [x2]
    pValues = [i for i in range(0,n+1)]
    for j in pValues:
        if j==0:
            xValues1.append(x1)
            xValues2.append(x2)
        if j>0 : 
            xValues1.append(f(xValues1[j],r))
            xValues2.append(f(xValues2[j],r))
    xv1 =  np.array(xValues1[1::])      
    xv2 = np.array(xValues2[1::])
    diff = np.log(abs(xv2-xv1))
    return pValues,diff
