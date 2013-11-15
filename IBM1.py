import json, sys, itertools
from collections import defaultdict
from math import log
import cPickle as pickle

#IBM MODEL 1 CODE

enwords = "corpus.en"
dewords = "corpus.de"

#print "IBM Model1 Loaded"

def loadwords(enwords=enwords, dewords=dewords):
  fen = open(enwords,'r')
  fde = open(dewords,'r')
  tdict = defaultdict(set)
  #gerdict = defaultdict(int)
  #parser = HTMLParser.HTMLParser()
  for eng,ger in itertools.izip(fen,fde):
    eng= ['_NULL_']+ eng.split()
    #ger = parser.unescape(ger)
    ger= ger.split()
    #german = german | set(ger)
    for word in eng:
      tdict[word] |= set(ger)

  return tdict

#def q(j,i,l,m):
  #deLogified
  #return (1.0/(l+1))


def tfe(tdict):
  #deLogified (Confirmed)
  t = defaultdict(dict)
  for engword in tdict:
    for gerword in tdict[engword]:
      t[engword][gerword] = 1.0/float(len(tdict[engword]))
      #print t[engword][gerword]
  return t

#t_fe = tfe(loadwords())



def runEM (t,dewords=dewords,enwords=enwords):
  #number of iterations = k
  
  S = 5

  #parser = HTMLParser.HTMLParser()
  for itr in range(S):
    print 'iteration',itr+1
    fen = open(enwords,'r')
    fde = open(dewords,'r')
    c = defaultdict(float)
    #print "c[man,mann]=", c[('man','mann')],"c[man]",c['man'], "Tfe:",t['man']['mann']
    
    for e,f in itertools.izip(fen,fde):
      e=  ['_NULL_']+ e.split()
      #f = parser.unescape(f)
      f= ['*'] + f.split()
      l = len(e)-1
      m = len(f)-1
      
      for i in range(1,m+1):
        denom = 0
        for j in range(0,l+1):
          denom += t [e[j]] [f[i]]
        #delta = 0
        for j in range(0,l+1):
          #delta = t [f[i]] [e[j]] / denom
          num = t[e[j]][f[i]]
          delta = num / denom
          c[ (e[j], f[i]) ] += delta
          c[ e[j] ] += delta
          c[ (i,j,l,m) ]+= delta
          c[ (i,l,m) ]+=delta
          

    for en in t:
      for fr in t[en]:
        try:
          t[en][fr]= c[(en, fr)]/c[en]
        except:
          pass#print en
  return t

devwords = "devwords.txt"
def loaddevwords(devwords=devwords):
  f = open(devwords,'r')
  out = []
  for word in f:
    out+=[word.strip()]
  return out

def script(outT):
  dev = loaddevwords()
  #dev = ['man','treaty','absolutely','perhaps','propose','the','.',',','?']
  for word in dev:
    templist = []
    for ger in  outT[word]:
      templist += [(ger,outT[word][ger])]

    templist=sorted(templist, key = lambda x:x[1], reverse=True)
    print word
    print templist[:10]
    print '\n'

  return

def reversedic (tf):
  trev = defaultdict(dict)
  for e in tf:
    for f in tf[e]:
      trev[f][e] = tf[e][f]
  #Returns reversed dictionary (useful for runtime optimization)
  return trev

def alignments (tf):
  fde = open(dewords)
  fen = open(enwords)
  tdict = defaultdict(set)
  tf2e = reversedic(tf)
  count = 0
  for eng,ger in itertools.izip(fen,fde):
    engstr = eng
    eng = ['_NULL_']+ eng.split()
    gerstr = ger
    ger = ger.split()
    len_a = len(ger)
    a = [None]*len_a
    count+=1
    if count ==21:
      return
    #print tf2e['mann'] ['_NULL_']

    for index in range(len (ger)):
      maxval =0
      argmax = None
      for i in range(len(eng)):
        try:
          temp = tf2e[ger[index]][eng[i]]
          #print ger[index], eng[i], tf2e[ger[index]][eng[i]]
          if temp > maxval:
            maxval = temp
            argmax = i
        except:
          print ger[index], eng[i]
        
      a[index] = argmax 
    print engstr, gerstr, a, '\n'
    
def picklIt (obj,filename):
  f = open(filename,'w')
  pickle.dump(obj,f)
  print "Filewrite Complete"
  f.close()

def unpicklIt(filename):
  f = open(filename,'r')
  obj = pickle.load(f)
  return obj

def main():
  tdict = loadwords()
  tf = tfe(tdict)
  outT = runEM(tfe(tf))
  picklIt(outT,"Model1T.dat")
  #script(outT)
  #alignments(outT)
  
#First 10 alignment values are correct
#alignments()

#Less than 1% error in the probability values in the script
#WTF Why?
#script(outT)

if __name__ == '__main__':
  main()