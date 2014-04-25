import IBM1, collections, sys, cPickle
from collections import defaultdict
import itertools
from math import log
from array import array

#print "IBM Model2 Loaded"

"""Code for the IBM Model 2 Machine Translation System"""

class Q():
  """A simple class to handle "q"
  parameter functionalities"""
  def __init__(self):
    self.q = {}

  def get(self, j,i,l,m):
    if (j,i,l,m) in self.q:
      return self.q[(j,i,l,m)]
    else:
      self.q[(j,i,l,m)] = 1.0/float(l+1)
      return self.q[(j,i,l,m)]

  def set(self, j,i,l,m, value):
    self.q[(j,i,l,m)] = value
    
  def getkeys(self):
    return self.q

  def size(self):
    return len(self.q)

  def __len__(self):
    return len(self.q)

    
def runEM (t,dewords=IBM1.dewords,enwords=IBM1.enwords):
  #number of iterations = k
  S = 5
  q = Q()

  for itr in range(S):

    print 'iteration',itr+1
    fen = open(enwords,'r')
    fde = open(dewords,'r')
    c = defaultdict(float)
    
    for e,f in itertools.izip(fen,fde):
      e=  ['_NULL_']+ e.split()
      f= ['*'] + f.split()
      l = len(e)-1
      m = len(f)-1
      
      for i in range(1,m+1):
        #denom = 0
        d = array('d')
        for j in range(0,l+1):
          d.append(q.get(j,i,l,m)*t[e[j]][f[i]])
        #print d
        denom = sum(d)
        #print 'denom',d,denom
        for j in range(0,l+1):
          delta = d[j]/denom
          #print 'delta', delta
          c[ (e[j], f[i]) ] += delta
          c[ e[j] ] += delta
          c[ (j,i,l,m) ]+= delta
          c[ (i,l,m) ]+=delta

    for en in t:
      for fr in t[en]:
        try:
          t[en][fr]= c[(en, fr)]/c[en]
        except:
          print 'exception occurred'
          pass

    #print q.size()
    for j,i,l,m in q.getkeys():
      #print j,i,l,m
      #ensure that the discrepencies in 
      #if(j,i,l,m) in c:
      newval = c[ (j,i,l,m) ]/ c[(i,l,m)]
      q.set(j,i,l,m, newval) 
  return t,q


def sentence_align(ger,eng,tf2e,q):
    eng = ['_NULL_']+ eng.split()
    ger = ger.split()
    #len_a = len(ger)
    l = len(eng)-1
    m = len(ger)
    a = [None]*m
    #Transformation, replaced old 'index' with i, and old 'i' with 'j'
    finalval = 0
    for i in range(len (ger)):
      maxval = -float('inf')
      argmax = None
      for j in range(len(eng)):
        try:
          temp = log(tf2e[ger[i]][eng[j]] * q.get(j,i+1,l,m))
          #temp = log(tf2e[ger[i]][eng[j]] * q[(j,i+1,l,m)])
        except:
          temp = -1000000
        if temp > maxval:
          maxval = temp
          argmax = j

      a[i] = argmax
      finalval += maxval
    return a, finalval

def alignment2 (tf,q):
  
  fde = open(IBM1.dewords)
  fen = open(IBM1.enwords)
  tdict = defaultdict(set)
  tf2e = IBM1.reversedic(tf)
  count = 0
  for eng,ger in itertools.izip(fen,fde):
    if count==20:
      return
    a, maxval = sentence_align(ger,eng,tf2e,q)
    count+=1

def main():
  outT = IBM1.unpicklIt("Model1T.dat")
  t,q = runEM(outT)
  IBM1.picklIt(t,"M2T.dat")
  IBM1.picklIt(q,"M2Q.dat")
  alignment2(t,q)

  
if __name__ == '__main__':
  main()
