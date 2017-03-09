from examples import *
from issa import *


def main(argv):

	name = 'test'
	size = 50
	inters = 100
	agentType = 3
	ver = 0
	prot = 'europe'

	try:
		opts, args = getopt.getopt(argv,"a:i:s:v:p:",["agent=","interactions=","size=", "verbose=", "protocol="])
	except getopt.GetoptError:
		print '-a agent type \n -i number of interactions \n -s protocol size'
		sys.exit(2)
	for opt, arg in opts:
		if not arg=='':
			if opt == '-h':
				print '-a agent type \n -i number of interactions \n -s protocol size'
				sys.exit()
			if opt in ("-a", "--agent"):
				try:	
					agentType = int(arg)
				except:
					print "-a must be 0,1,2, or 3"
			if opt in ("-i", "--interactions"):
				inters = int(arg)
			if opt in ("-s", "--size"):
				size = int(arg) 
			if opt in ("-v", "--verbose"):
				ver = int(arg) 
			if opt in ("-p", "--protocol"):
				prot = arg 		

	if prot == 'europe':
		prot0 = generate_protocol(countries,size,int(size-(size*0.2)),1)
		prot1 = translate_protocol(prot0,europe)
		print "I generated a protocol"
		# print "I generated the protocol: \n {}".format(prot0)
		alg0 = generate_heterogeneity(europe,countries,capitals,0.5,0.5)
		alg1 = invert_alg(alg0)

	elif prot == 'travel':
		prot0 = travelC
		prot1 = travelTA
		alg0 = FalconC
		alg1 = FalconTA

	print "agentType {}".format(agentType)
	if agentType == 0:
		a0 = AgentWA(0, prot0, Alignment(alg0))
		a1 = AgentWA(1, prot1, Alignment(alg1))
	elif agentType == 1:
		a0 = ISSAgent(0, prot0)
		a1 = ISSAgent(1, prot1)
	elif agentType == 2:
		a0 = ISSAgentWA(0, prot0, Alignment(alg0))
		a1 = ISSAgentWA(1, prot1, Alignment(alg1))
	else:
		a0 = AgentWAExp(0, prot0, Alignment(alg0))
		a1 = AgentWAExp(1, prot1, Alignment(alg1))

	for h in range(inters):
		print "\n Interaction {}".format(h)
		start_issa(a1,a0, act=0, verb=ver)
		print "Result: {}".format(a1.results[-1])

	print "Percentage of success: {}".format(sum(a0.results)/float(inters))

if __name__ == "__main__":
   main(sys.argv[1:])


