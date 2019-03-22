import pya
import io
#import skrf as rf
import scipy.io as sio
import numpy as np
import cmath as cm
import json as js
from pprint import pprint

class Component:
    def __init__(self, s_in, p_in, f_in):
        self.s = s_in
        self.p = p_in
        self.f = f_in

    def __str__(self):
        return ''.join(str(d) for d in self.f)
    
    def __repr__(self):
        return ' '.join(str(d) for d in self.p)

def p2r(radii, angle):
    return radii * np.exp(1j*angle)

def r2p(x):
    return abs(x), np.angle(x)


class Reader:
    #include bool for grating coupler
    def readSparamData(filename, numports, isgc):
        F = []
        S = []
        fid = open(filename, "r")
        if isgc is True:
            arrlen = 67-33
            lines = fid.readlines()
            F = np.zeros(arrlen)
            S = np.zeros((arrlen,2,2), 'complex128')
            for i in range(0, arrlen):
                words = lines[i+33].split()
                F[i] = float(words[0])
                S[i,0,0] = cm.rect(float(words[1]), float(words[2]))
                S[i,0,1] = cm.rect(float(words[3]), float(words[4]))
                S[i,1,0] = cm.rect(float(words[5]), float(words[6]))
                S[i,1,1] = cm.rect(float(words[7]), float(words[8]))
            F = F[::-1]
            S = S[::-1,:,:]
        
        else:
            line = fid.readline()
            line = fid.readline()
            numrows = int(tuple(line[1:-2].split(','))[0])
            S = np.zeros((numrows, numports, numports), dtype='complex128')
            r = m = n = 0
            for line in fid:
                if(line[0] == '('):
                    continue
                data = line.split()
                data = list(map(float, data))
                if(m == 0 and n == 0):
                    F.append(data[0])
                S[r,m,n] = p2r(data[1], data[2])
                r += 1
                if(r == numrows):
                    r = 0
                    m += 1
                    if(m == numports):
                        m = 0
                        n += 1
                        if(n == numports):
                            break
        fid.close()
        return [S, F]
        
pya.Cell.Reader = Reader

def findPort(name, list):
    for d in range(0, len(list)):
        for p in range(0, len(list[d].p)):
            if(list[d].p[p] == name):
                #print(name+' was found')
                return [d, p]
    #print(name+' cannot be found')
    return [-1, -1]