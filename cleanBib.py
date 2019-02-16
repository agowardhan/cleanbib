import numpy as  np 
import re
from collections import Counter
import argparse

def main(infile,outfile, verbose=True): 
    infile = infile
    eprints=[]
    if verbose:
        print('Using file:', infile)
    w = open(infile, mode='r')
    lines = w.readlines()
    w.close()
    
    if verbose:
        print('Reading...')

    temp=[]
    for line in lines:
        if 'eprint' in line: 
        #eprint = line.strip('\n').strip(' ').strip(',').strip('}').strip('{').strip('eprint = {')
            temp.append(line)
    
    eprints = [x.split('= {')[1].split('}')[0] for x in temp]
        
    if verbose:
        print('Read!')
    
    counts = Counter(eprints)
    delcount=0
    for item, key in counts.items(): 
        if key>1:
            for ii in range(key-1): 
                lines = delete(item, lines)
                delcount+=1
    if verbose:
        print('Deleted ' + str(delcount)+' duplicates.')

    if verbose:
        print('writing output file to:', outfile)
    
    out = open(outfile, mode='w')
    out.writelines(lines)
    out.close()
    
def delete(item, lines):

    indxs = [i for i, x in enumerate(lines) if 'eprint' in x and x.split('= {')[1].split('}')[0]==item]
    
    i = indxs[0]
    j=i
    indx0=-1
    while indx0==-1:
        if lines[j].strip(' ').startswith('@ARTICLE{'): 
            begin=True
            indx0 = j
        else:
            j = j-1
    k=i
    indxn=-1
    while indxn==-1:
        if lines[k]=='}\n': 
            begin=True
            indxn = k
        else:
            k=k+1

    lines = lines[:indx0] + lines[indxn+1:]
    return lines

parser = argparse.ArgumentParser(description='Delete duplicates from the bib file')
parser.add_argument('infile', nargs='?',default='./in.bib')
parser.add_argument('outfile', nargs='?',default='./out.bib')
parser.add_argument('verbose', nargs='?',default=True)

args = parser.parse_args()

main(infile=args.infile, outfile=args.outfile, verbose=args.verbose)
