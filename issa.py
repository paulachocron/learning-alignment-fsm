
#!/usr/bin/python

import sys, getopt
from multiprocessing import Process, Pipe, Queue
import random
#from scipy.stats import rv_discrete
from interaction import *
from generators import *
from operator import itemgetter
import numpy as np

# verbose = 0
# if remote:
# 	verbose = 0

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def start_issa(agent1, agent2, act=1, verb = 0):
	global verbose
	verbose = verb
	first_conn, second_conn = Pipe()
	queue = Queue()
	result_1 = []
	result_2 = []
	a1 = Interlocutor(agent1, first_conn, queue)
  	a2 = Interlocutor(agent2, second_conn, queue)

	a1.start()
	a2.start()
  	a1.join()
	a2.join()

	while not queue.empty():
		history = queue.get()
		if agent1.id == history[0]:
			agent1.add_experience(history[1], history[2], act)
		elif agent2.id == history[0]:
			agent2.add_experience(history[1], history[2], act)
			
	a1.terminate()
#	print "this is process a2 which made matches {}".format(queue.get())
	a2.terminate()


class Interlocutor(Process):
	""" This class is an agent in interaction """

	def __init__(self, agent, connection, queue):
		# Here the agent is initialized with its own interaction model
		super(Interlocutor, self).__init__()
		self.agent = agent
		self.IM_cs = agent.IM.initial
		self.AP_cs = 'q0'
		self.connection = connection
		self.matches_made = []
		self.queue = queue
		self.history = []
		self.sending_situation = ''
		self.state_list = []


	def run(self):
		while self.AP_cs == 'q0':
			if self.agent.IM.i_send(self.IM_cs, self.agent.id):
				self.history.append((0, self.IM_cs))
				self.align_as_sender()

			else:
				self.align_as_rcvr()

		self.queue.put([self.agent.id, self.history, self.AP_cs])
		# HISTORY IS: 
		# 0: agent id
		# 1: state history: 
			# 0: i send or i receive
			# 1: state
			# 2: if i receive, word received
			# 3: if i receive, word chosen to match
			# 4: if i receive, matching possibilities
		# 2: final state

	def align_as_sender(self):
		if self.agent.IM.i_send(self.IM_cs, self.agent.id):
			poss = self.agent.IM.possible_paths(self.IM_cs)
			if len(poss)>1:
				self.state_list.append(self.IM_cs)
			t = random.choice(poss)
			self.IM_cs = t.target
			self.send_msg(t.msg)

			self.AP_cs = 'q1'

			# WE ARE IN STATE Q1 now wait for the confirmation of the message
			conf = self.connection.recv()

			if conf.ill == 'UTTER':
				#they are trying to send at the same time, cannot be aligned
				self.AP_cs = 'u'
				return
			
			if conf.ill == 'INFORM_FINAL': #our partner reached a final state
				self.AP_cs = 'q2'

				if self.agent.IM.is_final(self.IM_cs) and conf.ct == self.IM_cs: 
					self.confirm_final()
					self.AP_cs = 's'
					return
					
				else:
					self.deny_final()
					self.AP_cs = 'u'
					return 

			elif conf.ill == 'INFORM': #our partner reached a final state
				if conf.ct == 'non_final_state':	#our partner reached a non final state
					self.AP_cs = 'q3' 	
					if self.agent.IM.is_final(self.IM_cs):
						self.deny_not_final()
						self.AP_cs = 'u'
						return
					else:
						self.confirm_not_final()
						self.AP_cs = 'q0'
						return
				
				elif conf.ct == 'failure': #our partner failed
					self.AP_cs = 'u'
					return

		else:
			raise NameError('I am not a sender')


	def align_as_rcvr(self):
		self.sending_situation = 'r'
		# Here the agent waits for a message to arrive
		if not self.connection.poll(0.1):
			# they are both waiting, timeout
			self.AP_cs = 'u'
			return 

		a_msg = self.connection.recv()
		
		if a_msg.ill == 'UTTER':
			# new message
			self.AP_cs = 'q1'
			# decode the message and try to match it
			inner_msg = a_msg.ct 


			(match, vector) = self.agent.match(inner_msg, self.IM_cs)

		# history is a list of tuples <0, state> or <1, state, received word, chosen word, possibilities vector>
			if not match:
				self.inform_failure()
			 	self.AP_cs = 'u'

			else:
				self.history.append((1, self.IM_cs, inner_msg.ct, match.msg.ct, vector))
				self.matches_made.append([self.IM_cs, match.msg.ct, inner_msg.ct])
				if len(vector)>1:
					self.state_list.append(self.IM_cs)
				#print "matched {} with {}!".format(match.msg.ct, inner_msg.ct)
					#self.add_match(inner_msg.msg, t[2].msg)
				self.IM_cs = match.target

				if self.agent.IM.is_final(match.target):
					self.AP_cs = 'q2'
					self.inform_final2()
				else:
					self.AP_cs = 'q3'			
					self.inform_not_final()

				# Wait for the confirmation message
				conf = self.connection.recv()
			#	print "I am {} and my state is {} conf is {}".format(self.id, self.AP_cs, conf.msg)

				if self.AP_cs == 'q2':
					if conf.ill == 'CONFIRM':
						if conf.ct == 'final_state':	 	
							self.AP_cs = 's'
					
					elif conf.ill == 'DENY':
						if conf.ct == 'final_state':	 	
							self.AP_cs = 'u'

				elif self.AP_cs == 'q3':
					if conf.ill == 'CONFIRM':
						if conf.ct == 'non_final_state':	 	
							self.AP_cs = 'q0'

					elif conf.ill == 'DENY':
						if conf.ct == 'non_final_state':
							self.AP_cs = 'u'

	def send_msg(self, msg):
		alignment_msg = Message('UTTER', self.agent.id,1-self.agent.id, msg)
		self.connection.send(alignment_msg)

	def inform_final(self):
		alignment_msg = Message('INFORM', self.agent.id,1-self.agent.id, 'final_state')
		self.connection.send(alignment_msg)

	def inform_not_final(self):
		alignment_msg = Message('INFORM', self.agent.id,1-self.agent.id, 'non_final_state')
		self.connection.send(alignment_msg)

	def confirm_final(self):
		alignment_msg = Message('CONFIRM', self.agent.id,1-self.agent.id, 'final_state')
		self.connection.send(alignment_msg)

	def confirm_not_final(self):
		alignment_msg = Message('CONFIRM', self.agent.id,1-self.agent.id, 'non_final_state')
		self.connection.send(alignment_msg)

	def inform_failure(self):
		alignment_msg = Message('INFORM', self.agent.id,1-self.agent.id, 'failure')
		self.connection.send(alignment_msg)

	def deny_final(self):
		alignment_msg = Message('DENY', self.agent.id, 1-self.agent.id, 'final_state')
		self.connection.send(alignment_msg)

	def deny_not_final(self):
		alignment_msg = Message('DENY', self.agent.id, 1-self.agent.id, 'non_final_state')
		self.connection.send(alignment_msg)

	def inform_final2(self):
		alignment_msg = Message('INFORM_FINAL', self.agent.id,1-self.agent.id, self.IM_cs)
		self.connection.send(alignment_msg)




class Agent():
	""" An agent  that sends messages, and interprets the received ones """

	def __init__(self, id, IM):
		self.id = id
		self.IM = IM
		self.results = []

	def get_values(self, message, possibilities, cs):
		return {p: float(1/len(possibilities)) for p in possibilities}

	def choose_match(self, values_dict, values):
		""" Chooses match according to the values in a dictionary"""
		minVal = min(values)
		choices = []
		if minVal<0:
			add = minVal - 0.05*minVal	
			for p in values_dict.keys():
				values_dict[p] = (values_dict[p] - add)

		for p in values_dict.keys():
			for m in range(int(values_dict[p]*1000)):
				choices.append(p)
			
		if choices:
			match = random.choice(choices)
		else:
			match = random.choice(values_dict.keys())
		return match


	def match(self, message, cs):
		""" Finds an interpretation for a possible message"""
		message = message.ct # we only care about the content

		possibilities = self.get_possibilities(cs)
		vector = []

		if not possibilities:
			return None, []

		values_dict, history_buff = self.get_values(message, possibilities, cs)

		values = [values_dict[p] for p in values_dict.keys()]

		if len(possibilities)==1:
			match = possibilities[0]
	
 		else:
 			match = self.choose_match(values_dict, values)
 
		######################### THE GREEDY OPTION
			#match = random.choice([p for p in values_dict.keys() if values_dict[p]==max(values)])

		##################### THE STOCHASTIC OPTION 

		# do it manually... we consider 4 significant decimals
		# First make everything positive
			# minVal = min(values)
			# choices = []
			# if minVal<0:
			# 	add = minVal - 0.05*minVal	
			# 	for p in values_dict.keys():
			# 		values_dict[p] = (values_dict[p] - add)

			# for p in values_dict.keys():
			# 	for m in range(int(values_dict[p]*1000)):
			# 		choices.append(p)
			# if choices:
			# 	match = random.choice(choices)
			# else:
			# 	match = random.choice(values_dict.keys())

		#match = np.random.choice(norm_values_dict.keys(),  p=norm_values)

		# ######################################################
		if verbose:
			print "Experience: {}".format(self.experience) 
			print "Agent {} received message {}".format(self.id, message)
			print "Alignment values: {}".format(values_dict)
			print "Matched with : {}".format(match.msg.ct)
		return (match, history_buff)
 

	def add_experience(self,matches, s, act):
		if s=='s':
			self.results.append(1)
		else:
			self.results.append(0)


class AgentWA(Agent):
	""" An agent that has an alignment and uses it to interpret messages"""

	def __init__(self, id, IM, alignment, explo = 0.9):
		#  alignment.v1() is the vocabulary of this agent
		# alignment.v2() is the vocabulary of its interlocutor

		Agent.__init__(self,id,IM)
		self.alignment = alignment
		self.explo = explo 


	def similarity(self, c1, c2):
		if c1 == c2:
			return 1
		else:
			return 0

	def get_values(self, message, possibilities, cs):

		uniform =  {p: float(1)/float(len(possibilities)) for p in possibilities}

		valg = self.get_alg_values(message, possibilities)
		combine = {p: uniform[p]*(1-self.explo) + valg[p]*self.explo for p in possibilities}
		# print "frombefore {}".format([valg[p] for p in valg.keys()])
		return combine, [valg[p] for p in valg.keys()]


	def get_possibilities(self, cs):
		return [p for p in self.IM.possible_paths(cs)]


	def get_alg_values(self, message, possibilities):
		valg = {}
		for p in possibilities:
			matches = self.alignment.get_matches_f(message)
			par = 0  # ------------- HC 

			if len(matches)>0:
				sim, best_match = max([(self.similarity(p.msg.ct, m), m) for m in matches], key=itemgetter(0))

				value = sim * self.alignment.get_confidence(best_match, message)

			else:
				value = 0  # ------------- HC 
				
			if (message not in self.alignment.get_matches(p.msg.ct)) and len(self.alignment.get_matches(p.msg.ct))>0:
				value = value - par

			valg[p] = value
		return valg


class ISSAgent(Agent):
	""" An agent that uses the ISSA learning method, remembering successful matches"""

	def __init__(self, id, IM):
		# Here the agent is initialized with its own interaction model
		Agent.__init__(self,id,IM)

		self.experience = {}
		for s in self.IM.states:
			self.experience[s] = []
		self.success = 0

	def get_possibilities(self,cs):
		return [p for p in self.IM.possible_paths(cs)]

		# return 	[p for p in self.IM.possible_paths_ill(cs, message.ill) if len([t for t in self.experience[cs] if t[1]==p.msg.ct and not t[0]==message])==0]

	def get_prev_values(self, message, possibilities, cs):
		"""These are the starting values
			Uniform distribution in this case
		"""
		return {p: float(1)/float(len(possibilities)) for p in possibilities}, [float(1)/float(len(possibilities)) for p in possibilities]

	def choose_match(self, values_dict, values):
		match = random.choice([p for p in values_dict.keys() if values_dict[p]==max(values)])
		return match

	def get_values(self, message, possibilities, cs):

		wexp = {}
		prev_values_dict, values = self.get_prev_values(message, possibilities, cs)
		
 		exp = [m[1] for m in self.experience[cs] if m[0] == message]

	 	if exp:
	 		for p in prev_values_dict.keys():
				# wexp[p] = (float(exp.count(p.msg.ct))/float(len(exp)))*float(0.9) + float(0.1) * prev_values_dict[p]  # ------------- HC 
				wexp[p] = float(exp.count(p.msg.ct))/float(len(exp))
			return wexp, values

		else:
			return prev_values_dict, values

	def add_experience(self,states, s, act):
		# the experience is a dictionary state: (received, chosen)
		Agent.add_experience(self,states, s, act)
		if s=='s' and act:
			for st in states:
				if st[0]==1:
					self.experience[st[1]].append([st[2],st[3]]) # this is very bad, for the other one we use a dictionary	
		

	def get_experience(self):
		return self.experience

	def get_results(self):
		return results


class ISSAgentWA(ISSAgent, AgentWA):
	""" An agent that uses the ISSA method and has an alignment"""

	def __init__(self, id, IM, alignment, explo = 0.9):
		#  alignment.v1() is the vocabulary of this agent
		# alignment.v2() is the vocabulary of its interlocutor

		ISSAgent.__init__(self,id,IM)

		AgentWA.__init__(self,id,IM, alignment, explo)

	def get_prev_values(self, message, possibilities, cs):
		return AgentWA.get_values(self, message, possibilities, cs)

	def get_values(self, message, possibilities, cs):
		return ISSAgent.get_values(self, message, possibilities, cs)

	# this doesn't seem to be necessary
	# def choose_match(self, values_dict, values):
	# 	if values==[values_dict[p] for p in values_dict.keys()]:
	# 		return AgentWA.choose_match(self, values_dict, values)
	# 	else:
	# 		return ISSAgent.choose_match(self, values_dict, values)


class AgentWAExp(ISSAgent, AgentWA):
	"""An agent that uses the ISSA method and has an alignment, and it also actualizes the alignment with experience"""
	# alpha is forgetting parameter
	# gamma is the learning propagation parameter
	
	def __init__(self, id, IM, alignment, type='all', alpha=0.3, gamma=0.8, mode=1, punishment = 1):
		# alignment.v1() is the vocabulary of this agent
		# alignment.v2() is the vocabulary of its interlocutor
		ISSAgent.__init__(self,id,IM)
		AgentWA.__init__(self,id,IM, alignment)

		self.alpha = alpha
		self.gamma = gamma
		self.align_experience = {}
		self.type = type
		self.mode = mode
		self.punishment = punishment

		for s in IM.states:
			self.align_experience[s] = {}


	def get_prev_values(self, message, possibilities, cs):
		valg = AgentWA.get_alg_values(self, message, possibilities)
		values = {}

		for p in possibilities:
			if message in self.align_experience[cs] and p.msg.ct in self.align_experience[cs][message]:
				values[p] = self.align_experience[cs][message][p.msg.ct]
			else:
				values[p] = valg[p]
		# values.values( = softmax(values.values())	
		# valuest = softmax(alignment[v].values())
		
		# values = {k: valuest[values.keys().index(k)] for k in alignment[v].keys()}		

		return values, [values[p] for p in possibilities]


		# # # we need to normalize this if we're going to use probabilities instead of values 
		# valg = AgentWA.get_alg_values(self, message, possibilities)

		# #valg = self.compute_valg(message, possibilities)
		# for p in valg.keys():
		# 	if message in self.align_experience.experience[cs]:
		# 		if p.msg.ct in self.align_experience.experience[cs][message]:
		# 			valg[p] = min(1, valg[p] + self.align_experience.experience[cs][message][p.msg.ct])

		# return valg, [valg[p] for p in valg.keys()]


	def choose_match(self, values_dict, values):
		match = random.choice([p for p in values_dict.keys() if values_dict[p]==max(values)])
		return match

	def estimate_precision(self):
		increased = []
		decreased = []

		found_mappings = {}

		for s in self.align_experience.keys():
			for v in self.align_experience[s]:
				for w in self.align_experience[s][v]:
					if [v,w] in self.experience[s]:
							found_mappings[(v,w)]= 1
					else:
						if (v,w) in found_mappings and self.align_experience[s][v][w]>found_mappings[(v,w)]:
							found_mappings[(v,w)]= self.align_experience[s][v][w]
						else:
							found_mappings[(v,w)]= self.align_experience[s][v][w]

		for (v,w) in found_mappings.keys():
			#print found_mappings.keys()
			if self.alignment.is_match(w,v):
				if self.alignment.get_confidence(w,v)<=found_mappings[(v,w)]:
					increased.append((v,w))
				else:
					decreased.append((v,w))
		# print increased
		# print decreased

		total_matches = [(v,w) for v in self.alignment.keys() for w in self.alignment.get_matches(v)]
		#print self.align_experience
		
		if decreased == [] and increased == []:
			return 0
		else:
			precision = float(len(increased))/float(len(increased)+len(decreased))
			# print precision
			return precision

	def get_values(self, message, possibilities, cs):
		#check. this is giving some very strange results
		return ISSAgent.get_values(self, message, possibilities, cs)

	def add_experience(self, history, s, act):
		# print "addexp"
		# print s
		# print history
		# print act

		ISSAgent.add_experience(self,history, s, act)

		if act:
			if s=='u':
				self.align_update(history)


	def get_possibilities_simple(self, cs):
		return [p for p in self.IM.possible_paths(cs)]


	def align_update(self, history):
			# history is a list of tuples <i align, state, received word, chosen word, possibilities: [word, v_alg]>
		if self.mode==0:
			################# Q-Learning, fast
			myHistory = [(h[1],h[2],h[3],max(h[4])) for h in history if h[0]]
			# print self.id
			# print self.align_experience
			# print myHistory
			for i in list(reversed(range(len(myHistory)))):
				s, rcv, match, rew = myHistory[i]
				if i==len(myHistory)-1:
					value = (-1)*self.punishment 
				else:
					possibilities = self.get_possibilities(myHistory[i+1][0])
					values = self.get_prev_values(myHistory[i+1][1],possibilities,myHistory[i+1][0])
					value = max(values[1])

				if verbose:
					print "update"
					print rcv
					print match
					print value
						#now add the values
				if not rcv in self.align_experience[s]:
					self.align_experience[s][rcv] = {}
				if not match in self.align_experience[s][rcv]:
					#this fix is not nice. only works when greedy
					self.align_experience[s][rcv][match] = myHistory[i][3]

	 			self.align_experience[s][rcv][match] = self.align_experience[s][rcv][match]  * (1-self.alpha)  + value * self.alpha		
		
		else:
			################# Q-Learning, slow
			myHistory = [(h[1],h[2],h[3],max(h[4])) for h in history if h[0]]
			# print self.id
			# print self.align_experience
			# print myHistory
			for i in list(reversed(range(len(myHistory)))):
				s, rcv, match, rew = myHistory[i]
				if i==len(myHistory)-1:
					value = (-1)*self.punishment 
				else:
					value = myHistory[i+1][3] * self.gamma
					
				if verbose:
					print "update"
					print rcv
					print match
					print value
						#now add the values
				if not rcv in self.align_experience[s]:
					self.align_experience[s][rcv] = {}
				if not match in self.align_experience[s][rcv]:
					#this fix is not nice. only works when greedy
					self.align_experience[s][rcv][match] = myHistory[i][3]

	 			self.align_experience[s][rcv][match] = self.align_experience[s][rcv][match]  * (1-self.alpha)  + value * self.alpha		


def conv(list):
	if 0 in list:
		return max([r for r in range(len(list)) if list[r]==0])
	else:
		return 0

