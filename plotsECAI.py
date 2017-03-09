import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import json
import matplotlib.font_manager as fm
import seaborn as sns
from scipy.interpolate import UnivariateSpline

# sns.set()

doc = open('Experimentation/JSONexp3-om-test1', 'r')	

results = json.JSONDecoder().decode(doc.read()) 

######### PALG, exp 1
# exp = results
# conv=1

# fig = plt.figure(figsize=(7,5))
# t = sorted([float(k)/10 for k in exp[str(5)].keys()])
# # matrix = [[exp['third'][str(float(pres)/10)][str(float(rec)/10)][conv]-exp['fourth'][str(float(pres)/10)][str(float(rec)/10)][conv] for pres in range(1,11)] for rec in range(1,11)]
# matrix = [[exp[str(pres)][str(rec)] for pres in range(1,10)] for rec in reversed(list(range(1,10)))]

# ax = sns.heatmap(matrix)
# ax.set_xticklabels(t)
# ax.set_yticklabels(t)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.legend(loc = 'best', fontsize=18)


# cax = plt.gcf().axes[-1]
# cax.tick_params(labelsize=12)

# plt.ylabel('recall', fontsize=18)
# plt.xlabel('precision',  fontsize=18)

# sns.plt.show()


# # plt.ylabel('recall', fontsize=19 )
# # plt.xlabel('precision', fontsize=19 )

# #plt.title('S', fontsize=22)
# fig.subplots_adjust(bottom=0.14)
# # # fig.suptitle('alg-exp-ev', fontsize=22)
# fig.savefig('exp1.jpg')

###################################

t = [str(x) for x in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]]

first, = plt.plot(t, [results[str(0.2)][exp] for exp in t], 'y-',label='0.2')
second, = plt.plot(t, [results[str(0.5)][exp] for exp in t], 'b*--',label='0.5')
third, = plt.plot(t, [results[str(0.8)][exp] for exp in t], 'r^:',label='0.8')

sns.set_style("white")
plt.legend(loc = 'best', fontsize=18)
#rcParams.update({'font.size': 34})
#plt.legend()
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.ylabel('Proportion of correct interactions', fontsize=19 )
plt.xlabel('alpha', fontsize=19)

#fig.subplots_adjust(bottom=0.15)

# fig.suptitle(pren+' precision, '+recn+' recall', fontsize=22)
# fig.savefig('convp'+str(int(pres*10))+'r'+str(int(rec*10))+'.jpg')

plt.show()


############################ ECAI ##############################

################### THIS IS FOR THE HEATMAP (EXP 2)
# # # precision is x, recall is y

# exp = results[str(90)]
# conv=1

# fig = plt.figure(figsize=(7,5))
# t = sorted([float(k) for k in exp['fifth'][str(0.5)].keys()])
# # matrix = [[exp['third'][str(float(pres)/10)][str(float(rec)/10)][conv]-exp['fourth'][str(float(pres)/10)][str(float(rec)/10)][conv] for pres in range(1,11)] for rec in range(1,11)]
# matrix = [[exp['fifth'][str(float(pres)/10)][str(float(rec)/10)][conv] for pres in range(1,11)] for rec in reversed(list(range(1,11)))]

# ax = sns.heatmap(matrix)
# ax.set_xticklabels(["" for x in range(5)]+t[5:])
# # ax.set_xticklabels(t[5:])
# # ax.set_xticklabels(t)
# ax.set_yticklabels(t)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.legend(loc = 'best', fontsize=18)
# print t
# print ax.get_xticks()

# cax = plt.gcf().axes[-1]
# cax.tick_params(labelsize=12)

# plt.ylabel('recall', fontsize=18)
# plt.xlabel('precision',  fontsize=18)

# sns.plt.show()


# # plt.ylabel('recall', fontsize=19 )
# # plt.xlabel('precision', fontsize=19 )

# plt.title('ev-alg-exp', fontsize=22)
# fig.subplots_adjust(bottom=0.14)
# # # fig.suptitle('alg-exp-ev', fontsize=22)
# fig.savefig('prrc5.jpg')

# ################## THE FOLLOWING IS FOR THE CONVERGENCE (EXP 1)
# for pres in [0.2,0.5,0.8]:
# 	for rec in [0.2,0.5,0.8]:

# pres = 0.8
# rec = 0.2


# exp = results[str(90)]
# precision = str(pres)
# recall = str(rec)

# t = sorted([int(k) for k in exp[precision][recall]['second'].keys()])


# spline1 = UnivariateSpline(t, [exp[precision][recall]['second'][str(p)] for p in t])
# spline2 = UnivariateSpline(t, [exp[precision][recall]['first'][str(p)] for p in t])
# spline3 = UnivariateSpline(t, [exp[precision][recall]['third'][str(p)] for p in t])
# spline4 = UnivariateSpline(t, [exp[precision][recall]['fourth'][str(p)] for p in t])
# spline5 = UnivariateSpline(t, [exp[precision][recall]['fifth'][str(p)] for p in t])

# 	# first, = plt.plot(tnew, spline1(tnew), 'y-', label='alg')
# 	# second, = plt.plot(tnew, spline2(tnew), 'b-')
# 	# third, = plt.plot(tnew, spline3(tnew), 'r-')
# 	# fourth, = plt.plot(tnew, spline4(tnew), 'w-')
# 	# fourth, = plt.plot(tnew, spline5(tnew), 'g-')

# fig = plt.figure(figsize=(7,5))

# first, = plt.plot(t, [exp[precision][recall]['second'][str(p)]*100 for p in t], 'y-',label='alg')
# second, = plt.plot(t, [exp[precision][recall]['first'][str(p)]*100 for p in t], 'b*--',label='exp')
# third, = plt.plot(t, [exp[precision][recall]['third'][str(p)]*100 for p in t], 'r^:',label='alg-exp')
# # fourth, = plt.plot(t, [exp[precision][recall]['fourth'][str(p)] for p in t], 'g*-',label='alg+exp+ev')
# fifth, = plt.plot(t, [exp[precision][recall]['fifth'][str(p)]*100 for p in t], 'go-',label='ev-alg-exp')

# sns.set_style("white")
# plt.legend(loc = 'best', fontsize=14)
# #rcParams.update({'font.size': 34})
# #plt.legend()
# plt.yticks(fontsize=16)
# #plt.yticks([10,20,30,40,50,60,70,90,100],fontsize=16)
# plt.xticks(fontsize=16)
# print plt.yticks()
# plt.xlim((0,350))
# plt.ylabel('% of successful interactions', fontsize=19 )
# plt.xlabel('Number of interactions', fontsize=19)

# fig.subplots_adjust(bottom=0.15)

# if pres==0.2:
#  	pren = 'Low'
# elif pres==0.5:
# 	pren = 'Medium'
# elif pres==0.8:
# 	pren = 'High'
# if rec==0.2:
# 	recn = 'low'
# elif rec==0.5:
# 	recn = 'medium'
# elif rec==0.8:
# 	recn = 'high'

# fig.suptitle(pren+' precision, '+recn+' recall', fontsize=22)
# fig.savefig('convp'+str(int(pres*10))+'r'+str(int(rec*10))+'.jpg')

#plt.show()
