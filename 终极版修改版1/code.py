import sys
import math


def primes(numbers):
    n=eval(numbers[1])
    number=eval(numbers[2])
    amount=eval(numbers[3])

    if number==1:
        start=2
    else:
        start=int(n/amount*(number-1))+1
    if number==amount:
        end=n
    else:
        end=int(n/amount*number)

    allprimes=[]

    for i in range(start,end+1):
        flag=True
        for j in range(2,int(math.sqrt(i))+1):
            if i % j == 0:
                flag=False
                break
        if flag:
            allprimes.append(i)

    print(allprimes)


primes(sys.argv)