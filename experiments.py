#!/usr/bin/python

import sys, getopt
from interaction import *
from generators import *
from issa import *
from examples import * 
import json


#### Convergence methods with different proportions of success

def conv(list):
	if 'u' in list:
		return max([r for r in range(len(list)) if list[r]==0])
	else:
		return 0

def conv08(list):
	indexes = [r for r in range(len(list)) if list[r:-1].count(0)<0.2*len(list[r:-1])]
	if indexes:
		return min(indexes)
	else:
		return len(list)

def conv09(list):
	indexes = [r for r in range(len(list)) if list[r:-1].count(0)<0.1*len(list[r:-1])]
	if indexes:
		return min(indexes)
	else:
		return len(list)

def conv095(list):
	indexes = [r for r in range(len(list)) if list[r:-1].count(0)<0.05*len(list[r:-1])]
	if indexes:
		return min(indexes)
	else:
		return len(list)



################# CONVERGENCE EXPERIMENT #################

def convergence(protT0,protT1,reps,res):
	""" This experiment tests success rate after different learning periods for three classes of precision and recall"""

	res_conv = {}
	rInters = [pow(x,2) for x in range(2,20)]


	############## The ISSA agent
	print "Agent ISSA"
	results_a = {}
	for j in rInters:
		print >>res, j
		print j

		res_a = []
		for i in range(int(reps)):
					
			A0a = ISSAgent(0, protT0)
			A1a = ISSAgent(1, protT1)

			for h in range(j):
				start_issa(A1a,A0a)

			for h in range(50):
				start_issa(A1a,A0a, act=0)
							
			res_a.append(sum(A0a.results[-50:])/float(50))
				
		print >>res, "1: "+ str(sum(res_a)/float(len(res_a)))
		print "1: "+ str(sum(res_a)/float(len(res_a)))
				
		results_a[j] = sum(res_a)/float(len(res_a))
				

	for precision in [0.2,0.5,0.8]:
		res_conv[precision] = {}
		#for recall in [float(x)/5 for x in range(1,5)]:
		for recall in [0.2,0.5,0.8]:
			print >>res, "precision: {}, recall: {}".format(precision,recall)
			print  "precision: {}, recall: {}".format(precision,recall)
			
			lalg0 = []
			lalg1 = []
			for i in range(reps):
		 		alg0T = generate_heterogeneity(europe, countries, capitals, precision, recall)
		 	# 	if remote:
				# 	f = open('../input/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')
				# else:
		 	# 		f = open('examples/suite/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')
		 	# 	f.write(json.dumps(alg0T))
		 	# 	f.close()
		 		alg1T = invert_alg(alg0T)
		 		alg0T = Alignment(alg0T)
		 		alg1T = Alignment(alg1T)	
		 		lalg0.append(alg0T)
			 	lalg1.append(alg1T)

			results_d = {}
			results_b = {}
			results_c0 = {}
			results_c = {}

		##################### The aligner agent
			print "Agent ALIGNMENT"
			res_d = []
			for i in range(int(reps)):
				alg0T = lalg0[i]
				alg1T = lalg1[i]
				A0d = AgentWA(0, protT0, alg0T)
				A1d = AgentWA(1, protT1, alg1T)
				for h in range(60):
					start_issa(A1d,A0d, act=0)
				res_d.append(sum(A0d.results[-60:])/float(60))
			results_d = {j: sum(res_d)/float(len(res_d)) for j in rInters}
			print >>res, "2: "+ str(sum(res_d)/float(len(res_d)))
			print "2: "+ str(sum(res_d)/float(len(res_d)))

		######################## All the other agents
			print "Other Agents"
			for j in rInters:
				print >>res, j
				print j

			#	res_a = []
				res_b = []
				res_c = []
				res_c0 =[]
				#res_d = []
				for i in range(int(reps)):

					alg0T = lalg0[i]
					alg1T = lalg1[i]
									
					A0b = ISSAgentWA(0, protT0, alg0T)
					A1b = ISSAgentWA(1, protT1, alg1T)

					A0c = AgentWAExp(0, protT0, alg0T, mode=1, punishment=0.8, alpha=0.3, gamma=0.8)
					A1c = AgentWAExp(1, protT1, alg1T, mode=1, punishment=0.8, alpha=0.3, gamma=0.8)

					A0c0 = AgentWAExp(0, protT0, alg0T, mode=0, punishment=0.8, alpha=0.3, gamma=0.8)
					A1c0 = AgentWAExp(1, protT1, alg1T, mode=0, punishment=0.8, alpha=0.3, gamma=0.8)

					for h in range(j):
						#start_issa(A1a,A0a)
						#start_issa(A1d,A0d)
						start_issa(A1b,A0b)
						start_issa(A1c,A0c)
						start_issa(A1c0,A0c0)

					for h in range(60):
						#start_issa(A1a,A0a, act=0)
						#start_issa(A1d,A0d, act=0)
						start_issa(A1b,A0b, act=0)
						start_issa(A1c,A0c, act=0)
						start_issa(A1c0,A0c0, act=0)
						
					#res_a.append(sum(A0a.results[-50:])/float(50))
					res_b.append(sum(A0b.results[-60:])/float(60))
					res_c.append(sum(A0c.results[-60:])/float(60))
					res_c0.append(sum(A0c0.results[-60:])/float(60))
					#res_d.append(sum(A0d.results[-50:])/float(50))

			#	print >>res, "1: "+ str(sum(res_a)/float(len(res_a)))
				#print >>res, "2: "+ str(sum(res_d)/float(len(res_d)))
				print >>res, "3: "+ str(sum(res_b)/float(len(res_b)))
				print >>res, "4: "+ str(sum(res_c)/float(len(res_c)))
				print >>res, "5: "+ str(sum(res_c0)/float(len(res_c0)))	
			#	print "1: "+ str(sum(res_a)/float(len(res_a)))
				#print "2: "+ str(sum(res_d)/float(len(res_d)))
				print "3: "+ str(sum(res_b)/float(len(res_b)))
				print "4: "+ str(sum(res_c)/float(len(res_c)))
				print "5: "+ str(sum(res_c0)/float(len(res_c0)))

			#	results_a[j] = sum(res_a)/float(len(res_a))
				results_b[j] = sum(res_b)/float(len(res_b))
				results_c[j] = sum(res_c)/float(len(res_c))
				results_c0[j] = sum(res_c0)/float(len(res_c0))
				#results_d[j] = sum(res_d)/float(len(res_d))


			res_conv[precision][recall] = {'first' : results_a,
							'second' : results_d,
							'third' : results_b,
							'fourth' : results_c,
							'fifth' : results_c0}
	return res_conv


################## PRECISION AND RECALL EXPERIMENT ###################
def pir(protT0,protT1,reps,inters,res):
	""" This experiment tests success rate for different values of presicion and recall"""

	# results_b = {}
	results_d = {}

	# results_c0 = {}
	# results_c = {}

	for precision in [float(x)/10 for x in range(1,11)]:
	#for precision in [0.3]:
		#print precision

		# results_b[precision] = {}
		results_d[precision] = {}
		# results_c[precision] = {}
		# results_c0[precision] = {}

	
		for recall in [float(x)/10 for x in range(1,11)]:
		#for recall in [0.7]:
			print >>res, "precision: {}, recall: {}".format(precision,recall)
			print  "precision: {}, recall: {}".format(precision,recall)
			

			total_d = []
			conv_d = []

			# total_b = []
			# conv_b = []
			# total_c = []
			# conv_c = []
			# total_c0 = []
			# conv_c0 = []


			for i in range(int(reps)):

				alg0T = generate_heterogeneity(europe, countries, capitals, precision, recall)
				if remote:
					f = open('../input/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')
				else:
					f = open('examples/suite/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')

				f.write(json.dumps(alg0T))
				f.close()
				alg1T = invert_alg(alg0T)
				alg0T = Alignment(alg0T)
				alg1T = Alignment(alg1T)

				# A0b = ISSAgentWA(0, protT0, alg0T)
				# A1b = ISSAgentWA(1, protT1, alg1T)

				A0d = AgentWA(0, protT0, alg0T)
				A1d = AgentWA(1, protT1, alg1T)

				# A0c = AgentWAExp(0, protT0, alg0T, mode=1, punishment=0.8, alpha=0.3, gamma=0.8)
				# A1c = AgentWAExp(1, protT1, alg1T, mode=1, punishment=0.8, alpha=0.3, gamma=0.8)


				# A0c0 = AgentWAExp(0, protT0, alg0T, mode=0, punishment=0.8, alpha=0.3, gamma=0.8)
				# A1c0 = AgentWAExp(1, protT1, alg1T, mode=0, punishment=0.8, alpha=0.3, gamma=0.8)

				for j in range(int(inters)):
					start_issa(A1d,A0d)
					# start_issa(A1b,A0b)
					# start_issa(A1c,A0c)
					# start_issa(A1c0,A0c0)
				
				total_d.append(sum(A0d.results))
				conv_d.append(conv09(A0d.results))

				# total_b.append(sum(A0b.results))
				# conv_b.append(conv09(A0b.results))
				
				# total_c.append(sum(A0c.results))
				# conv_c.append(conv09(A0c.results))
				# total_c0.append(sum(A0c0.results))
				# conv_c0.append(conv09(A0c0.results))

			print "With alignment:"
			print  str(sum(total_d) / float(len(total_d)))
			print  str(sum(conv_d) / float(len(conv_d)))
			print >>res, "With alignment:"
			print >>res, str(sum(total_d) / float(len(total_d)))
			print >>res, str(sum(conv_d) / float(len(conv_d)))
			results_d[precision][recall] = (sum(total_d) / float(len(total_d)), sum(conv_d) / float(len(conv_d)))

			# print "With alignment + issa:"
			# print  str(sum(total_b) / float(len(total_b)))
			# print  str(sum(conv_b) / float(len(conv_b)))
			# print >>res, "With alignment + issa:"
			# print >>res, str(sum(total_b) / float(len(total_b)))
			# print >>res, str(sum(conv_b) / float(len(conv_b)))
			# #res.write( convergence(A0b.results))
			# results_b[precision][recall] = (sum(total_b) / float(len(total_b)), sum(conv_b) / float(len(conv_b)))

			
			# print "With alignment + experience: (prop)"
			# print str(sum(total_c) / float(len(total_c)))
			# print str(sum(conv_c) / float(len(conv_c)))				
			# print >>res, "With alignment + experience: (prop)"
			# print >>res, str(sum(total_c) / float(len(total_c)))
			# print >>res, str(sum(conv_c) / float(len(conv_c)))	
			# results_c[precision][recall] = (sum(total_c) / float(len(total_c)), sum(conv_c) / float(len(conv_c)))

			# print "With alignment + experience: (no prop)"
			# print str(sum(total_c0) / float(len(total_c0)))
			# print str(sum(conv_c0) / float(len(conv_c0)))				
			# print >>res, "With alignment + experience: (no prop)"
			# print >>res, str(sum(total_c0) / float(len(total_c0)))
			# print >>res, str(sum(conv_c0) / float(len(conv_c0)))	
			# results_c0[precision][recall] = (sum(total_c0) / float(len(total_c0)), sum(conv_c0) / float(len(conv_c0)))
	
	return {
	#'first' : results_a,
				'second' : results_d}
	 		# 	'third' : results_b,
				# 'fourth' : results_c,
				# 'fifth' : results_c0}



####################### SIZE EXPERIMENT #############################

def sizes(reps,inters,res,sizes):
	""" This tests how the size of the protocol affects the convergence"""

	alg0T = generate_heterogeneity(europe, countries, capitals, precision=0.5, recall=0.5)
	# if remote:
	# 	f = open('../input/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')
	# else:
	# 	f = open('examples/suite/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')

	# f.write(json.dumps(alg0T))
	# f.close()
	alg1T = invert_alg(alg0T)
	alg0T = Alignment(alg0T)
	alg1T = Alignment(alg1T)
	
	results_a = {}
	results_b = {}
	results_c = {}
	results_c0 = {}
	results_d = {}

	for n in sizes:
		transitions = n*10
		states = n*10-int(0.1*n)

		print >>res, "transitions: {}".format(transitions)

		print "transitions: {}".format(transitions)
		protT0 = generate_protocol(countries,transitions,states,1)
		protT0.set_name('proteu')

		if remote:
			protT0.to_json('../input/')
		else:
			protT0.to_json('Experimentation/oalg/input/')

		protT1 = translate_protocol(protT0,europe)

		for i in range(int(reps)):

			A0d = AgentWA(0, protT0, alg0T)
			A1d = AgentWA(1, protT1, alg1T)
			A0a = ISSAgent(0, protT0)
			A1a = ISSAgent(1, protT1)
			A0b = ISSAgentWA(0, protT0, alg0T)
			A1b = ISSAgentWA(1, protT1, alg1T)

			A0c = AgentWAExp(0, protT0, alg0T, mode=1, punishment=0.8, alpha=0.3, gamma=0.8)
			A1c = AgentWAExp(1, protT1, alg1T, mode=1, punishment=0.8, alpha=0.3, gamma=0.8)

			A0c0 = AgentWAExp(0, protT0, alg0T, mode=0, punishment=0.8, alpha=0.3, gamma=0.8)
			A1c0 = AgentWAExp(1, protT1, alg1T, mode=0, punishment=0.8, alpha=0.3, gamma=0.8) 
	
			total_a = []
			conv_a = []
			total_d = []
			conv_d = []
			total_b = []
			conv_b = []
			total_c = []
			conv_c = []
			total_c0 = []
			conv_c0 = []

		
			for j in range(int(inters)):
				#print "j: {}".format(j)
				start_issa(A1a,A0a)
				start_issa(A1d,A0d)
				start_issa(A1b,A0b)
				start_issa(A1c,A0c)
				start_issa(A1c0,A0c0)

			total_a.append(sum(A0a.results))
			conv_a.append(conv09(A0a.results))
			total_d.append(sum(A0d.results))
			conv_d.append(conv09(A0d.results))

			total_b.append(sum(A0b.results))
			conv_b.append(conv09(A0b.results))
					
			total_c.append(sum(A0c.results))
			conv_c.append(conv09(A0c.results))
			total_c0.append(sum(A0c0.results))
			conv_c0.append(conv09(A0c0.results))
		
		print "Without alignment:"
		print str(sum(total_a) / float(len(total_a)))
		print str(sum(conv_a) / float(len(conv_a)))
		print >>res, "Without alignment:"
		print >>res, str(sum(total_a) / float(len(total_a)))
		print >>res, str(sum(conv_a) / float(len(conv_a)))
		results_a[n] = (sum(total_a) / float(len(total_a)), sum(conv_a) / float(len(conv_a)))

		print "With alignment:"
		print  str(sum(total_d) / float(len(total_d)))
		print  str(sum(conv_d) / float(len(conv_d)))
		print >>res, "With alignment:"
		print >>res, str(sum(total_d) / float(len(total_d)))
		print >>res, str(sum(conv_d) / float(len(conv_d)))
		results_d[n] = (sum(total_d) / float(len(total_d)), sum(conv_d) / float(len(conv_d)))

		print "With alignment + issa:"
		print  str(sum(total_b) / float(len(total_b)))
		print  str(sum(conv_b) / float(len(conv_b)))
		print >>res, "With alignment + issa:"
		print >>res, str(sum(total_b) / float(len(total_b)))
		print >>res, str(sum(conv_b) / float(len(conv_b)))
		results_b[n] = (sum(total_b) / float(len(total_b)), sum(conv_b) / float(len(conv_b)))

			
		print "With alignment + experience: (prop)"
		print str(sum(total_c) / float(len(total_c)))
		print str(sum(conv_c) / float(len(conv_c)))				
		print >>res, "With alignment + experience: (prop)"
		print >>res, str(sum(total_c) / float(len(total_c)))
		print >>res, str(sum(conv_c) / float(len(conv_c)))	
		results_c[n] = (sum(total_c) / float(len(total_c)), sum(conv_c) / float(len(conv_c)))

		print "With alignment + experience: (no prop)"
		print str(sum(total_c0) / float(len(total_c0)))
		print str(sum(conv_c0) / float(len(conv_c0)))				
		print >>res, "With alignment + experience: (no prop)"
		print >>res, str(sum(total_c0) / float(len(total_c0)))
		print >>res, str(sum(conv_c0) / float(len(conv_c0)))	
		results_c0[n] = (sum(total_c0) / float(len(total_c0)), sum(conv_c0) / float(len(conv_c0)))
	
	return {
	'first' : results_a,
				'second' : results_d,
	 			'third' : results_b,
				'fourth' : results_c,
				'fifth' : results_c0}


####################### GAMMA AND ALPHA ###########################
def parameters(protT0,protT1,reps,inters,res):
	""" This experiment tests how using different parameters in the learning affect the convergence"""

	results_par = {}
	precision = 0.5
	recall = 0.5
	alg0T = generate_heterogeneity(europe, countries, capitals, precision, recall)
	if remote:
		f = open('../input/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')
	else:
		f = open('examples/suite/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')
	f.write(json.dumps(alg0T))
	f.close()
	alg1T = invert_alg(alg0T)
	alg0T = Alignment(alg0T)
	alg1T = Alignment(alg1T)

	for gamma in [float(h)/10 for h in range(0,11)]:
		results_par[gamma]={}
		for alpha in [float(h)/10 for h in range(0,11)]:

			print >>res, "gamma: {}, alpha: {}".format(gamma,alpha)
			print  "gamma: {}, alpha: {}".format(gamma,alpha)

			total_c = []
			conv_c = []
			for i in range(reps):

				A0c = AgentWAExp(0, protT0, alg0T, mode=0, gamma = gamma, alpha = alpha)
				A1c = AgentWAExp(1, protT1, alg1T, mode=0, gamma = gamma, alpha = alpha)
				for j in range(inters):
				# 	start_issa(A1d,A0d)
				# 	start_issa(A1b,A0b)

					start_issa(A1c,A0c)

				total_c.append(sum(A0c.results))
				conv_c.append(conv09(A0c.results))
						
			print "With alignment + experience: (prop)"
			print str(sum(total_c) / float(len(total_c)))
			print str(sum(conv_c) / float(len(conv_c)))				
			print >>res, "With alignment + experience: (prop)"
			print >>res, str(sum(total_c) / float(len(total_c)))
			print >>res, str(sum(conv_c) / float(len(conv_c)))	
			results_par[gamma][alpha] = (sum(total_c) / float(len(total_c)), sum(conv_c) / float(len(conv_c)))

	return results_par


########################## PUNISHMENT ####################################
def punishment(protT0,protT1,reps,inters,res):
	""" This experiment tests how using different punishment values in the learning affect the convergence"""

	results_pun = {}

	precision = 0.5
	recall = 0.5

	alg0 = []
	alg1 = []

	for i in range(reps):
		alg0T = generate_heterogeneity(europe, countries, capitals, precision, recall)
		# f = open('examples/suite/jsonALG-alg'+str(precision)+'-'+str(recall), 'w')
		# f.write(json.dumps(alg0T))
		# f.close()
		alg1T = invert_alg(alg0T)
		alg0T = Alignment(alg0T)
		alg1T = Alignment(alg1T)
		alg0.append(alg0T)
		alg1.append(alg1T)		

	for punishment in [float(h)/10 for h in range(0,11)]:

		print >>res, "punishment: {}".format(punishment)
		print "punishment: {}".format(punishment)


		total_c = []
		conv_c = []
		for i in range(reps):

			alg0T = alg0[i]
			alg1T = alg1[i]
					
			A0c = AgentWAExp(0, protT0, alg0T, punishment=punishment, alpha=0.8)
			A1c = AgentWAExp(1, protT1, alg1T, punishment=punishment, alpha=0.8)
			for j in range(inters):

				start_issa(A1c,A0c)


			total_c.append(sum(A0c.results))
			conv_c.append(conv09(A0c.results))

		print "With alignment + experience"
		print str(sum(total_c) / float(len(total_c)))
		print str(sum(conv_c) / float(len(conv_c)))				
		print >>res, "With alignment + experience"
		print >>res, str(sum(total_c) / float(len(total_c)))
		print >>res, str(sum(conv_c) / float(len(conv_c)))	
		results_pun[punishment] = (sum(total_c) / float(len(total_c)), sum(conv_c) / float(len(conv_c)))

	return results_pun
	

def main(argv):

	name = 'test'
	size = [9]
	reps = 5
	inters = 100
	experiment = 'conv'
	
	directory = 'Experimentation/ecai2016/'
	try:
		opts, args = getopt.getopt(argv,"e:i:r:s:n:",["experiment=","interactions=","repetitions=","sizes=", "name="])
	except getopt.GetoptError:
		print '-e experiment \n -n name \n -r number of repetitions \n -i number of interactions \n -s list of sizes (between quotes)'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print '-e experiment \n -n name \n -r number of repetitions \n -i number of interactions \n -s list of sizes (between quotes)'
			sys.exit()
		if arg:		
			if opt in ("-e", "--experiment"):
				experiment = arg
			if opt in ("-i", "--interactions"):
				inters = int(arg)
			if opt in ("-r", "--repetitions"):
				reps = int(arg)
			if opt in ("-s", "--sizes"):
				size = [int(x) for x in arg.split()]
			if opt in ("-n", "--name"):
				name = arg

	results = {}

	print name

	if remote:
		res = open('../results/results' + name, 'w+')	
	else:
		res = open('results/results'+name, 'w+')	

	if experiment=='size':
		results = sizes(reps,inters,res,size)
		if remote:
			resjson = open('../results/JSON'+name, 'w+')
		else:
			resjson = open('results/JSON' + name, 'w+')

		resjson.write(json.dumps(results))	
		resjson.close()

	else:
		for n in size :
			results = {}
			transitions = n*10
			states = n*10-int(0.1*n)
			print >>res, "transitions: {}".format(transitions)

			print "transitions: {}".format(transitions)
			# Fixing the protocol, play with different kinds of  precision and recall and parameters for the learning. Analyze convergence
			protT0 = generate_protocol(countries,transitions,states,1)
			protT0.set_name('proteu')

			if remote:
				protT0.to_json('../input/')
			else:
				protT0.to_json('../Experimentation/ecai2016/input/')

			protT1 = translate_protocol(protT0,europe)

			results[transitions] = {}
			if experiment=='pun':
				results[transitions] = punishment(protT0,protT1,reps,inters,res)
			if experiment=='par':
				results[transitions] = parameters(protT0,protT1,reps,inters,res)
			if experiment=='pir':
				results[transitions] = pir(protT0,protT1,reps,inters,res)
			if experiment=='conv':
				results[transitions] = convergence(protT0,protT1,reps,res)


			if remote:
				resjson = open('../results/JSON'+name+str(n), 'w+')
			else:
				resjson = open('../Experimentation/ecai2016/JSON' + name+str(n), 'w+')

			resjson.write(json.dumps(results))	
			resjson.close()

	res.close()


if __name__ == "__main__":
   main(sys.argv[1:])

