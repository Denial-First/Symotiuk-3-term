import random
import copy
import pickle
import sys
import time



def check_sort():
    fcheck = open("a.txt", "r")
    prev = fcheck.readline()
    for i in fcheck:
        if int(i) < int(prev):
            return False
        prev = copy.copy(i)
    fcheck.close()
    return True


def create_file():
    fw = open("a.txt", "w")
    check = 0
    while check < 10485760:     # 10485760
        cur = random.randint(-10000000, 100000000)
        check = check + len(str(cur)) + 1
        fw.write(str(cur) + "\n")
    fw.close()


def classic_merge():
    fo = open("a.txt", "r")
    first = open("b.txt", "w")
    second = open("c.txt", "w")
    check = 0
    for i in fo:
        if check == 0:
            first.write(i)
            check = 1
        else:
            second.write(i)
            check = 0

    fo.close()
    first.close()
    second.close()
    power = 1
    while not check_sort():
        fo = open("a.txt", "w")
        first = open("b.txt", "r")
        second = open("c.txt", "r")
        fpointer = 0
        spointer = 0
        step = True
        while True:
            if (spointer >= power and fpointer >= power) or (spointer == 0 and fpointer == 0):
                a = first.readline()
                b = second.readline()
                fpointer = 0
                spointer = 0
            elif step is True:
                b = second.readline()
            elif step is False:
                a = first.readline()
            if a == '' and b == '':  # end of files
                break
            if b == '':  # end of second file
                fo.write(a)
                fpointer += 1
                while fpointer < power:
                    a = first.readline()
                    fo.write(a)
                    fpointer += 1
                fpointer = 0
                spointer = 0
            elif a == '':  # end of first file
                fo.write(b)
                spointer += 1
                while spointer < power:
                    b = second.readline()
                    fo.write(b)
                    spointer += 1
                fpointer = 0
                spointer = 0
            else:  # common occasion
                if int(a) > int(b):
                    fo.write(b)
                    spointer += 1
                    step = True
                    if spointer == power:
                        fo.write(a)
                        fpointer += 1
                        while fpointer < power:
                            a = first.readline()
                            fo.write(a)
                            fpointer += 1
                else:
                    fo.write(a)
                    fpointer += 1
                    step = False
                    if fpointer == power:
                        fo.write(b)
                        spointer += 1
                        while spointer < power:
                            b = second.readline()
                            fo.write(b)
                            spointer += 1

        first.close()
        second.close()
        fo.close()
        power = power * 2
        check = 0
        step = True
        fo = open("a.txt", "r")
        first = open("b.txt", "w")
        second = open("c.txt", "w")
        for i in fo:
            if step is True:
                first.write(i)
                check += 1
                if check == power:
                    step = False
                    check = 0
            else:
                second.write(i)
                check += 1
                if check == power:
                    step = True
                    check = 0
        first.close()
        second.close()
        fo.close()


start = time.time()
create_file()
sort = time.time()
# if input("enter 1: ") == "1":
#     print("True")
print("created file:" + str(sort - start))
classic_merge()
print("sorted: " + str(time.time() - sort))
