from collections import defaultdict
import cPickle as pickle
import IBM1, IBM2
from math import log
#from q6 import readTParameters, readQParameters

Q = IBM2.Q

t = IBM1.unpicklIt("M2T.dat")
q = IBM1.unpicklIt("M2Q.dat")

def unscramble(tf,q):
  fde = open("original.de")
  tf2e = tf
  tf2e = IBM1.reversedic(tf)
  output = ""
  for ger in fde:
    
    fen = open("scrambled.en")
    
    finalguess = None
    maxval = float('-inf')
    
    for eng in fen:
      #found argmax a
      a, temp = IBM2.sentence_align(ger,eng,tf2e,q)
      
      if temp > maxval:
        maxval = temp
        finalguess = eng

    output+= finalguess

  print output

if __name__ == '__main__':

  unscramble(t,q)

  """"
    count = 0
    for j,i,l,m in q.getkeys():
        count +=1
        try:
            if abs(q.get(j,i,l,m)- q2[(j,i,l,m)])>1e-11:
                print q.get(j,i,l,m), q2[(j,i,l,m)], (j,i,l,m), count
        except:
            #print q.get(j,i,l,m), q2[(j,i,l,m)], (j,i,l,m), count
    print "lolmax"
    """