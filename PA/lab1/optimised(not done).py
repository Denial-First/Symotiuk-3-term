
def check_files():
    ra = open("a.bin", "rb")
    rb = open("b.bin", "rb")
    rc = open("c.bin", "rb")
    wa = open("a.txt", "w")
    wb = open("b.txt", "w")
    wc = open("c.txt", "w")
    while True:
        try:
            a = pickle.load(ra)
            wa.write(str(a) + '\n')
        except EOFError:
            break
    while True:
        try:
            b = pickle.load(rb)
            wb.write(str(b) + '\n')
        except EOFError:
            break
    while True:
        try:
            c = pickle.load(rc)
            wc.write(str(c) + '\n')
        except EOFError:
            break
    ra.close()
    rb.close()
    rc.close()
    wa.close()
    wb.close()
    wc.close()



def optimised_create_file():
    fw = open("b.bin", "wb")
    check = 0
    while check < 1024 * 1024 * 1024:  # 10485760
        cur = random.randint(-100000, 1000000)
        check = check + 28  # size of ints
        pickle.dump(cur, fw)
    fw.close()


def optimised_check_sort():     # перевіряти кожен max_size елемент
    fcheck = open("a.bin", "rb")
    prev = pickle.load(fcheck)
    # max_size = 1024 * 1024 * 1024 / 8
    while True:
        try:
            i = pickle.load(fcheck)
        except EOFError:
            break
        if i < prev:
            return False
        prev = copy.copy(i)

    fcheck.close()
    return True


def optimised_merge():

    fr = open("b.bin", "rb")
    fw = open("a.bin", "wb")
    # first = open("b.bin", "wb")
    # second = open("c.bin", "wb")
    # while True:
    #     try:
    #         i = pickle.load(fo)
    #         pickle.dump(i, first)
    #     except EOFError:
    #         break
    #     try:
    #         i = pickle.load(fo)
    #         pickle.dump(i, second)
    #     except EOFError:
    #         break
    list = []
    counter = 0
    power = 1024 * 1024 * 1024 / 8
    while True:
        try:
            list.append(pickle.load(fr))
            counter += 1
            if counter >= power:
                list.sort()
                for i in list:
                    pickle.dump(i, fw)
                list.clear()
                counter = 0
        except EOFError:
            list.sort()
            for i in list:
                pickle.dump(i, fw)
            print(sys.getsizeof(list))
            del list, counter
            break
    fr.close()
    fw.close()
    # first.close()
    # second.close()

    while not optimised_check_sort():
        fo = open("a.bin", "wb")
        first = open("b.bin", "rb")
        second = open("c.bin", "rb")
        fpointer = 0
        spointer = 0
        step = True
        while True:
            if (spointer >= power and fpointer >= power) or (spointer == 0 and fpointer == 0):
                try:
                    a = pickle.load(first)
                except EOFError:
                    a = ''
                try:
                    b = pickle.load(second)
                except EOFError:
                    b = ''
                fpointer = 0
                spointer = 0
            elif step is True:
                try:
                    b = pickle.load(second)
                except EOFError:
                    b = ''
            elif step is False:
                try:
                    a = pickle.load(first)
                except EOFError:
                    a = ''
            if a == '' and b == '':  # end of files
                break
            if b == '':  # end of second file
                pickle.dump(a, fo)
                fpointer += 1
                while fpointer < power:
                    try:
                        a = pickle.load(first)
                        pickle.dump(a, fo)
                        fpointer += 1
                    except EOFError:
                        break

                fpointer = 0
                spointer = 0
            elif a == '':  # end of first file
                pickle.dump(b, fo)
                spointer += 1
                while spointer < power:
                    try:
                        b = pickle.load(second)
                        pickle.dump(b, fo)
                        spointer += 1
                    except EOFError:
                        break
                fpointer = 0
                spointer = 0
            else:  # common occasion
                if a > b:
                    pickle.dump(b, fo)
                    spointer += 1
                    step = True
                    if spointer == power:
                        pickle.dump(a, fo)
                        fpointer += 1
                        while fpointer < power:
                            try:
                                a = pickle.load(first)
                                pickle.dump(a, fo)
                                fpointer += 1
                            except EOFError:
                                break
                else:
                    pickle.dump(a, fo)
                    fpointer += 1
                    step = False
                    if fpointer == power:
                        pickle.dump(b, fo)
                        spointer += 1
                        while spointer < power:
                            try:
                                b = pickle.load(second)
                                pickle.dump(b, fo)
                                spointer += 1
                            except EOFError:
                                break

        first.close()
        second.close()
        fo.close()
        power = power * 2
        check = 0
        step = True
        fo = open("a.bin", "rb")
        first = open("b.bin", "wb")
        second = open("c.bin", "wb")
        while True:
            if step is True:
                try:
                    i = pickle.load(fo)
                    pickle.dump(i, first)
                    check += 1
                except EOFError:
                    break
                if check == power:
                    step = False
                    check = 0
            else:
                try:
                    i = pickle.load(fo)
                    pickle.dump(i, second)
                    check += 1
                except EOFError:
                    break
                if check == power:
                    step = True
                    check = 0
        first.close()
        second.close()
        fo.close()

