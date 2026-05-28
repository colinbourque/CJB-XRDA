import numpy as np

def interp_qdp(file):
    a,b,c,d = [[],[],[],[]]
    clstr = []
    sublists = []
    wlist = []
    nsl = []

    with open(file) as rawout:
        qdpl = rawout.readlines()

        qdpl = qdpl[3:]


        for line in qdpl:
            line = line.replace('\n', '')
            line = line.replace('NO', '')
            clstr.append(line)


        for line in clstr:
            if not any(num in line for num in [str(x) for x in range(10)]):
                sublists.append(wlist)
                wlist=[]

            else:
                wlist.append(line)

        sublists.append(wlist)



        for l in sublists:
            l = [i.split() for i in l]
            nsl.append(l)

        a = np.array(nsl[0])
        a = a.astype(float).T

        b = np.array(nsl[1])
        b = b.astype(float).T

        c = np.array(nsl[2])
        c = c.astype(float).T

        d = np.array(nsl[3])
        d = d.astype(float).T

        return a,b,c,d

def sl_qdp(file):
    a,b = [[],[]]
    clstr = []
    sublists = []
    wlist = []
    nsl = []

    with open(file) as rawout:
        qdpl = rawout.read()

    qdpl = qdpl.replace('-\n', '')
    qdpl = qdpl.split('\n')
    qdpl = qdpl[3:]

    for line in qdpl:
        line = line.replace('-\n', '')
        line = line.replace('NO', '')
        clstr.append(line)


    for line in clstr:
        if not any(num in line for num in [str(x) for x in range(10)]):
            sublists.append(wlist)
            wlist=[]

        else:
            wlist.append(line)

    sublists.append(wlist)



    for l in sublists:
        l = [i.split() for i in l]
        nsl.append(l)

    a = np.array(nsl[0])
    a = a.astype(float).T

    b = np.array(nsl[1])
    b = b.astype(float).T

    return a,b
