from operator import attrgetter
import json

class Message:
	"""A Message with sender, receiver, and content."""

	def __init__(self, ill, snd, rcv, c):
		self.ill = ill
		self.snd = snd 
		self.rcv = rcv 
		self.ct = c

	def equal(self, msg):
		return 	self.snd == msg.snd and	self.rcv == msg.rcv and self.ct == msg.c

	def __str__(self):
		return "<%s -> %s, %s> " % (self.snd,self.rcv,self.ct)

	def __repr__(self):
		return "<%s -> %s, %s> " % (self.snd,self.rcv,self.ct)


class Transition:
	"""	A transition has source state, target state, and a message """
	def __init__(self, source, target, msg):
		self.source = source
		self.target = target
		self.msg = msg

	def __str__(self):
		return "(source %s, target %s, msg %s) " % (self.source, self.target, self.msg)

	def __repr__(self):
		return "(source %s, target %s, msg %s) " % (self.source, self.target, self.msg)


class InteractionModel:
 	""" The interaction model has states, transitions, initial state and final states """

	def __init__(self, states, transitions, initial_state, final_states, name = "p"):
		self.states = states #is A LIST
		self.transitions = transitions
		self.initial = initial_state
		self.final_states = final_states
		self.name = name

	def is_final(self, state):
		return state in self.final_states

	def initial_state(self):
		return self.initial

	def possible_paths(self, state):
		"""Out arrows from a state"""
		#print "state: %s" % state
		return [t for t in self.transitions if t.source == state]

	def possible_paths_msg(self, state, message):
		"""Out arrows from a state that match with a message"""
		return [t for t in self.transitions if t.source == state and t.msg.equal(message)]

	def reaches(self, trans, state):
		"""Returns true if a state can be reached from a transition"""
		prev = []
		paths = [[trans]]
		result = False

		while not prev == paths:
			prev = paths
			for p in paths:
				for t in self.transitions:
					if t.source == p[-1].target:
						p.append(t)
						if t.source == state:
							result = True
		return result


	def set_name(self, name):
		self.name = name

	def possible_paths_ill(self, state, illocution):
		return [t for t in self.transitions if t.source == state and t.msg.ill == illocution]

	def initial_state(self):
		return self.initial

	def i_send(self, state, id):
		return len([t for t in self.possible_paths(state) if t.msg.snd == id])>0

	def get_transition(self, state, message):
		# assumes there is only one transition per state, message, and that all messages are in one direction

		return [t for t in self.transitions if t.source==state and t.msg.ct==message][0]

	def neighbours(self, state):
		return [t.target for t in self.possible_paths(state)]
		
	def in_cycle(self, trans):
		"""A transition is in a cycle if its source state can be reached from it"""
		return self.reaches(trans, trans.source)

	def __str__(self):
		return "Name: %s \n States: %s \n Transitions: %s \n  Final states: %s " % (self.name, self.states, self.transitions, self.final_states)


	def to_tikz(self):
		""" Prints a tikz version of the protocol"""
		f = open('IM-'+self.name, 'w')
		f.write('\\begin{tikzpicture}[>=stealth\',shorten >=1pt,auto,node distance=2cm] \n')

		# a line for each state
		for i in self.states:
			accepting = ''
			if i in self.final_states:
				accepting = ', accepting'

			position = ''

			trans = [t for t in self.transitions if t.target == i]


			if trans:
				source = trans[0].source
				brothers = [t for t in self.transitions if t.target < i and t.source == source]
				if not brothers:
					position = '[right of={}]'.format(str(source))
				else:
					b = max(brothers, key=attrgetter('target'))
					position = '[below of={}]'.format(str(b.target))


			f.write('\\node[state ' + accepting + '] (' + str(i) + ')   ' + position + ' {' + str(i) +'}; \n')
		
		f.write('\n')
		f.write('\\path[->] ')
		# now the transitions
		for t in self.transitions[:-1]:
			f.write('(' + str(t.source) + ')  edge node {' + t.msg.ct + '} (' + str(t.target) + ') \n')
		
		f.write('(' + str(self.transitions[-1].source) + ')  edge node {' + self.transitions[-1].msg.ct + '} (' + str(self.transitions[-1].target) + '); \n')

		f.write('\\end{tikzpicture}')

		f.close()

		
	def to_json(self, path = ''):
		f = open(path+'jsonIM-'+self.name, 'w')		
		f.write(json.dumps(self, cls=MyJSONEncoder))
		f.close()



class MyJSONEncoder(json.JSONEncoder):
	"""Prints JSON versions of a protocol"""
	def default(self, o):
		return o.__dict__    

def from_json(json_object):
	if 'ill' in json_object:
		return Message(json_object['ill'],json_object['snd'],json_object['rcv'],json_object['ct'])

	elif 'source' in json_object:
		return Transition(json_object['source'], json_object['target'], json_object['msg'])

	elif 'states' in json_object:
		return InteractionModel(json_object["states"], json_object['transitions'],  json_object['initial'], json_object['final_states'])

# def im_from_doc(document):

def IM_from_json(doc):
	f = open(doc, 'r')
	json_object = f.read()
	im = json.JSONDecoder(object_hook = from_json).decode(json_object)
	return im

IM = InteractionModel([1,2,3,4],[Transition(1,2,Message("ask",0,1,'39')), Transition(2,3,Message("say",1,0,'44')), Transition(2,4,Message("say",1,0,'82'))],1,[3], name = 'test')

IM.to_json()

imb = IM_from_json('jsonIM-test')
