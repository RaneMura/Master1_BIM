
##Create a string of 1000 "a" and of 1000 "ab"
s = ''
j = ''
for k in range(1000) :
    s = s + 'a'
    j = j + 'ab'

#print(s)
#print(j)

#Create a list of 100 integers equal to 1
k=1
l = []
while k<= 100 :
    l.append(1)
    k = k+1
print(l)

#Make a list that contains all the even number ≤ 100
even = list(range(0, 101,2))

#Compute the sum of the 100 first integers (sum100.py)
somme = 0
for k in range(100) :
    somme = somme + k;
    
#Compute the sum of the odd integers ≤ 100 (sumpair100.py)
s_odd = 0
for i in range(1, 100, 2) :
    s_odd = s_odd + i
    
print(s_odd)


#Create a list of number by yourself and find the maximum of that list.
#Can you also find the index at which this maximum is reached ?

l = [1.2, 2, 13, 10, 10, 2, 1.20, 10.2, 9.2]
m = l[0]
index = 0
for jj in range(len(l)) :
    if l[jj] > m :
        m = l[jj]
        index = jj


print("max",m)
print("index", index)

#Make a function that tests if the integer sent as a parameter is divisible by 3
def div3(x) :
    return(x%3==0)

#Use the previous function to get the list of multiples of 3 less than 1000 (optional : you can use filter)
ll = []
num = 0
while num < 1000 :
    if div3(num) :
        ll.append(num)
    num +=1
    

#In the same way, list the quotients obtained by dividing by 7 numbers less than 1000 (optional you can use map)


#Do the factorial function n! = 1.2 . . . n with a loop and recursively and test how far it can go.

#loop :
def fac_loop(n) :
    j = n
    f = 1
    while j>1:
        f = f*j
        j = j-1
    return(f)
# rec
def fac(n) :
    if n == 1 :
        return 1
    else :
        return (n * fac(n-1))


import random


string_one = "je test des trucs"
print ("Original String: ", string_one)

char_list = list(string_one) # convert string inti list
random.shuffle(char_list) #shuffle the list

string_one = ''.join(char_list)
print ("shuffled String is: ", string_one)


#Make a function that takes a list as an argument and a function and applies the function to each element of the list and returns it. in one line

def appli(lis, func) :
    return [func(x) for x in lis]

