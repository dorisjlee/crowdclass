import matplotlib.pyplot as plt
from numpy import *
import numpy as np
import pandas as pd 
import scipy.stats as stats
import fnmatch
import os
from collections import Counter
np.set_printoptions(precision=2)
def bar_chart(dataA,dataB, N=1,width=0.3):
	AMeans = mean(dataA)
	BMeans = mean(dataB)
	# Astd = [std(dataA), std(A_posttest_score)]
	# Bstd =[std(dataB), std(B_posttest_score)]
	A_yerr = stats.t.interval(0.95,len(dataA)-1,loc = mean(dataA), scale=stat.sem(dataA))- mean(dataA)
	B_yerr = stats.t.interval(0.95,len(dataB)-1,loc = mean(dataB), scale=stat.sem(dataB))- mean(dataB)
	ind = np.arange(N)  # the x locations for the groups

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, AMeans, width, color='r', yerr=A_yerr,ecolor= "black")
	rects2 = ax.bar(ind + width, BMeans, width, color='b', yerr=B_yerr,ecolor= "black")

	# add some text for labels, title and axes ticks
	ax.set_ylabel('Scores',fontsize=14)
	ax.set_title('Learning Scores',fontsize=16)
	ax.set_xticks(ind + width)
	ax.set_xticklabels(('Pre-test', 'Post-test'),fontsize=14)

	ax.legend((rects1[0], rects2[0]), ('A', 'B'))

def pcheck(p,null_hyp):
    '''
    if p>0.05 then reject null hypothesis
    '''
    if p>0.05:
        return  null_hyp
    else:
        return "NOT "+null_hyp

def basic_stats(data1,data2,mode="double"):

	print "A: mu = {0}; std = {1}".format(np.around(mean(data1),3),np.around(std(data1),3))
	if mode=="double": print "B: mu = {0}; std = {1}".format(np.around(mean(data2),3),np.around(std(data2),3))

def shapiro_wilks(data,name):
	'''
	Test for Normality
	'''
	result = stats.shapiro(data)
	print "{0} : W = {1} ; p ={2} ---> {3}".format(name,np.around(result[0],2),result[1],pcheck(result[1],"Normal"))


def kolmogorov_smirnov(data1,data2,name):
	'''
	See if data come from the same distribution
	'''
	result = stats.ks_2samp(data1,data2)
	print "{0} : D = {1} ; p ={2} ---> {3}".format(name,np.around(result[0],2),np.around(result[1],2),pcheck(result[1],"from same distribution"))

def unpaired_Welch_t(data1,data2,name):
	'''
	Test whether there is significant difference between the two distributions
	'''
	result =  stats.ttest_ind(a= data1,b= data2,equal_var=False)
	print "{0} : t = {1} ; p ={2} ---> {3}".format(name,np.around(result[0],2),np.around(result[1],5),pcheck(result[1],"no significant different in the means of the two groups"))

def eff_size_R(data1,data2,abbrev = ""):
    f = open("EffSize.r", "w")
    ncol = len(data1)
    f.write("library(effsize)\n")
    f.write("dataA <- c("+ ','.join(str(p) for p in data1)+") \n".format(ncol))
    f.write("dataB <- c("+ ','.join(str(p) for p in data2)+") \n".format(ncol))
    f.write("cohen.d(dataA,dataB)\n")
    f.write("cohen.d(dataA,dataB,hedges.correction=TRUE)\n")
    f.close()

    os.system("r -f EffSize.r > EffSize_{}.out".format(abbrev))
    f = open("EffSize_{}.out".format(abbrev), 'r')
    lines = f.readlines()[18:] # supress header outputs

    for l in lines[5:] :
        if l!='\n':
            if l.split()[0]==">":
                print "------------------------"
            else:
                print l 
    f.close()
def compareMeans(A,B):
    Abar = mean(A)
    Bbar = mean(B)
    if Abar==Bbar:
        print "A = B"
    elif Abar>Bbar:
        print "A > B"
    elif Abar<Bbar:
        print "A < B"
def run_all_my_analysis(A,B,abbrev=""):
    print "---------------------------------------------------------------------------------"
    print abbrev
    compareMeans(A,B)
    basic_stats(A,B)
    shapiro_wilks(A,"A")
    shapiro_wilks(B,"B")
    kolmogorov_smirnov(A,B,"KS test")
    unpaired_Welch_t(A,B,"Welch's t-test")
    eff_size_R(A,B,abbrev)

#Non Parametric Stuff
def compare_effect_size(es):
    if es>0.5:
        return "Large"
    elif es>0.3 and es<0.5:
        return "Medium"
    elif es>0.1:
        return "Small"
def compareMedians(A,B):
    Abar = median(A)
    Bbar = median(B)
    print "Median"
    print "A: ",Abar
    print "B: ",Bbar
    if Abar==Bbar:
        print "A = B"
    elif Abar>Bbar:
        print "A > B"
    elif Abar<Bbar:
        print "A < B"
    print "------"

def wilcoxon_R(data1,data2,abbrev = ""):
    '''
    Non-parametric version of Welch's unpaired t test
    '''
    f = open("Wilcoxon.r", "w")
    ncol = len(data1)
    f.write("library(coin)\n")
    f.write("GroupA <- c("+ ','.join(str(p) for p in data1)+") \n".format(ncol))
    f.write("GroupB <- c("+ ','.join(str(p) for p in data2)+") \n".format(ncol))
    f.write("wilcox.test(GroupA,GroupB)\n")
    f.write("g = factor(c(rep('GroupA', length(GroupA)), rep('GroupB', length(GroupB)))) \n")
    f.write("v = c(GroupA, GroupB) \n")
    f.write("r = rank(v) \n")
    f.write("data = data.frame(g, r) \n")
    f.write("wilcox_test(v ~ g, distribution='exact') \n")
    f.write("A = split(data,data$g)\n")
    f.write("mean(A$GroupA$r) \n")
    f.write("mean(A$GroupB$r) \n")
    f.close()

    os.system("r -f Wilcoxon.r > Wilcoxon_{}.out".format(abbrev))
    f = open("Wilcoxon_{}.out".format(abbrev), 'r')
    lines = f.readlines()[18:] # supress header outputs
    
    for l in lines[5:] :
        if l!='\n' and l.split()[0]!=">":
            if l[:3]=="Z =":
                Z = float(l.split(",")[0].split()[-1])
                eff_size = abs(Z/sqrt(len(data1)+len(data2)))
                print "Effect Size  = {0} -----> {1}".format(eff_size,compare_effect_size(eff_size))
                
            if l[11:18]=='p-value':
                p = float(l.split()[-1])
                print "{0} : p ={1} ---> {2}".format(abbrev,p,pcheck(p,"from same population"))
            if l[:3]=='[1]':    
                print "Mean ranks of group"
            print l
def run_all_non_parametric_analysis(A,B,abbrev=""):
    print "---------------------------------------------------------------------------------"
    print abbrev
    compareMedians(A,B)
    basic_stats(A,B)
    shapiro_wilks(A,"A")
    shapiro_wilks(B,"B")
    wilcoxon_R(A,B,abbrev)
