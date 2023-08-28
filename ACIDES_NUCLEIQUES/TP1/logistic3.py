rValues = np.arange(2,4,0.001)
xval =[]
for i in range(len(rValues)):
    pvi, xvi = logistic(0.1,rValues[i],2000)
    xval.append(xvi[1000::])

plt.plot(rValues,xval,'k,')

plt.title("Représentation de la bifurcation de x en fonction r")
plt.xlabel("r")
plt.ylabel("x")
plt.legend()
plt.savefig("logistic3.png",dpi=300)
plt.show()
