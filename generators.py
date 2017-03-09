import random
from interaction import *
import json
import string
import math
from sets import Set
import copy

remote = 0

def generate_alignment(voc1, voc2, per=1, cant=0, confidence=False):
	"""Generates a random alignment between vocabularies voc1 and voc2
		Matches are one to one. Matches only up to per% of voc1 (per% if it is not larger than voc2)
		Assumes voc1 and voc2 have no repearted elements
		TODO: Add parametrization of the confidence distribution, and to allow multiple matches for the same word
	"""

	alg = []
	# generate a subset
	to_match = []

	# if cant == 0:
	# 	cant = min(len(voc1), len(voc2))

	for i in range(int(cant)):
		w = random.choice([x for x in voc1])
		to_match.append(w)

	for w in to_match:
		v = random.choice([x for x in voc2])
		if confidence:
			c = round(random.uniform(0.4,1),2)
			alg.append((w,v,c))
		else:
			alg.append((w,v))
	return alg


def generate_heterogeneity(alg, voc1, voc2, precision, recall):
	""" Generates an alignment between voc1 and voc2 with the given precision and recall with respect to alg
	Pre: alg is an alignment between voc1 and voc2
	"""

	# precision is #(found matches \cap relevant matches) / # found matches
	# recall is #(found matches \cap relevant matches) / #relevant matches

	# rv = # relevant matches, frm = # found relevant matches, fm = # found matches
	frm = recall * len(alg)
	fm = frm/precision

	prev = []

	for i in range(int(frm)):
		match = random.choice([x for x in alg if not x in prev])
		prev.append(match)

	to_match1 = [x for x in voc1 if not [t for t in prev if t[0]==x]]	
	to_match2 = [x for x in voc2 if not [t for t in prev if t[1]==x]]
	new = generate_alignment(voc1, voc2, cant = fm-frm, confidence=(len(alg[0])==3))
	
	return prev + new


def generate_vocabulary(size):
	"""
	Generates a random vocabulary of the given size
	The vocabulary is composed by strings of the necessary size
	""" 
	voc = []
	while len(voc)<size:
		word = ''.join(random.choice(string.lowercase) for i in range(int(math.ceil(math.log(size, 23.0)))))
		if not word in voc:
			voc.append(word)
	return voc


def generate_protocol(vocabulary, ctrans, cstates, fstates, max_out=0, prop_choices=0):
	"""Generates an protocol with cstates states, ctrans transitions, and messages in vocabulary
		max_out and prop_choices are parameters to control the distribution of outgoing arrows, if desired
	"""

	if ctrans < cstates-1:
		raise NameError('Too few transitions')

	if ctrans > (cstates-1)*cstates:
		raise NameError('Too many transitions')

	if cstates==0:
		raise NameError('At least one state needed')

	if max_out==0:
		max_out = ctrans
	if prop_choices==0:
		max_choices = ctrans
	else:
		max_choices = ctrans/prop_choices
	
	transitions = []
	speaker = [0]
	states = [i for i in range(cstates)]
	choices = 0
	final_states = states[-fstates:]

	# Add one transition for each state
	for target in range(1, cstates):
		source = random.choice([i for i in range(len(transitions)+1) if not i in final_states and not len([t for t in transitions if t.source==i])>max_out and (choices<max_choices or len([m for m in transitions if m.source==i])==0)])
		if len([t for t in transitions if t.source==source])>0:
			choices = choices + 1

		speaker.append(1 - speaker[source])
		msg = Message('say',speaker[source], 1-speaker[source], random.choice([v for v in vocabulary if not [t for t in transitions if t.source == source and t.msg.ct == v]]))
		trans = Transition(source, target, msg)

		transitions.append(trans)

	# Add extra transitions
	for i in range(len(transitions), ctrans):
		# choose a pair of states that are not connected
		node = random.choice([(s,t) for s in range(cstates) for t in range(cstates) if (len([trans for trans in transitions if trans.source == s and trans.target == t])==0 and not s in final_states and not (s==t and len([tr for tr in transitions if tr.source == s])==0))])
		source = node[0]
		target = node[1]
		msg = Message('say', speaker[source], 1-speaker[source], random.choice([v for v in vocabulary if not [t for t in transitions if t.source == source and t.msg.ct == v]]))
		trans = Transition(source, target, msg)
		transitions.append(trans)

	final_states = [s for s in states if s in final_states or not [j for j in transitions if s == j.source]]

	return InteractionModel(range(cstates), transitions, 0, final_states)


def translate_protocol(protocol, alignment):
	"""Receives a protocol and an alignment
	Returns a structurally equivalent protocol with the messages translated according to the alignment
	Pre: alignment has a translation for each message in protocol
	"""
	transitions = []
	for t in protocol.transitions: 
		transitions.append(Transition(t.source, t.target, Message(t.msg.ill, t.msg.snd, t.msg.rcv, [x for x in alignment if x[0] == t.msg.ct][0][1])))
	return InteractionModel(protocol.states, transitions, protocol.initial, protocol.final_states)


def generate_pragmatic_heterogeneity(prot1, prot2, precision, recall):
	""" Receives two structurally equivalent protocols and two values between 0 and 1
	Returns an alignment ((word, word, confidence)) between the vocabularies in prot1 and prot2.
	That alignment has the precision and recall received as parameters with respect to the one between the protocols
	"""
	prag_alg = alg_from_prag_alg1(get_pragmatic_alignment(prot1,prot2))

	useN = float(recall) * len(prag_alg)
	totN = useN/precision
	misN = totN-useN

	found_matches = []
	matched_states = []

	# get the good ones
	if int(useN)>len(prag_alg):
		raise NameError('Impossible precision/recall values')

	useful = random.sample(prag_alg, int(useN))

	# now we need to find misleading ones, which is a bit trickier
	# we compute all compatible paths and find the wrong mappings that could be made on each of them
	comp = compatible_paths(prot1, prot2)
	misleadingp = []

	for x in comp:
		path1, path2 = x
		for i in range(len(path1)):
			s2 = path2[i].source
			# print path1[i]
			# and now we need to get all the possible mistaken mappings. that is easy
			misli = [(path1[i].msg.ct,m2.msg.ct) for m2 in prot2.possible_paths(s2) if not m2.msg.ct == path2[i].msg.ct]
			misleadingp = misleadingp + [m for m in misli if not m in misleadingp]

	if int(misN)>len(misleadingp):
		raise NameError('Impossible precision/recall values')
	else:
		misleading = random.sample(misleadingp, int(misN))
		alignment = useful + misleading
		alignment = [(x[0],x[1],0.9) for x in alignment]

	return alignment


def invert_alg(alignment):
	new = []
	for m in alignment:
		new.append((m[1],m[0],m[2]))

	return new


class Alignment(dict):

	def __init__(self, matches):
		# matches is a list of triples
		super(Alignment, self).__init__()
		self.v2 = Set()
		self.length = len(matches)
		for m in matches:
			self.v2.add(m[1])
			if m[0] not in self:
				self[m[0]] = [(m[1], m[2])]
			else:
				self[m[0]].append((m[1], m[2]))
		
	def voc1(self):
		return self.keys()

	def voc2(self):
		return self.v2

	def is_match(self, w1, w2):
		return w1 in self.keys() and len([x for x in self[w1] if x[0]==w2])>0

	def get_confidence(self, w1, w2):
		
		if not self.is_match(w1,w2):
			return 0

		else:
			#return filter(x[0]==w2, self[w1])[0][1]
			return [x for x in self[w1] if x[0]==w2][0][1]

	def has_match(self, w1):
		return w1 in self.keys()

	def has_match_f(self,w2):
		# for a foreign word 
		return len([w for w in self.keys() if self.is_match(w,w2)])>0


	def get_matches_f(self,w2):
		# doesn't assumes surjectivity in the alignment
		if self.has_match_f(w2):
			return [w for w in self.keys() if self.is_match(w,w2)]

		else:
			return [] # should fail

	def get_matches(self, w1):
		if not w1 in self.keys():
			return []

		else:
			return self[w1]

	def length(self):
		total_matches = [(v,w) for v in self.keys() for w in self.get_matches(v)]
	#	print total_matches
		return len(total_matches)


def paths(graph):
	"""Returns paths in a graph. These paths only include one cycle per state.
	   A path is (visited states, transitions) just for convenience.
	"""
	path = ([graph.initial],[])               # path traversed so far
   	paths = []
   	
	def search(path):
		for neighbour in graph.possible_paths(path[0][-1]):
			if path[0].count(neighbour.target)<2: # only one cycle containing each node per path is enough to find alignment
				new_path = copy.deepcopy(path)
				new_path[1].append(neighbour)
				new_path[0].append(neighbour.target)
				if neighbour.target in graph.final_states:
					paths.append(new_path)
				else:
					search(new_path)

   	search(path)
	return paths



def compatible_paths(prot0, prot1):
	""" Returns a list of tuples of compatible paths from prot0 and prot1
	    Compatible: same lenght, end states with equal properties, same sender in all states
	"""

	paths0 = paths(prot0)
	paths1 = paths(prot1)

	compatible_paths =[(p0[1],p1[1]) for p0 in paths0 for p1 in paths1 if len(p0[0])==len(p1[0]) and p0[0][-1]==p1[0][-1]
					 and len([i for i in range(len(p1[1])) if not p0[1][i].msg.snd == p1[1][i].msg.snd])==0]
 
 	return compatible_paths


def get_pragmatic_alignment(prot0, prot1):
	"""Returns the alignment derived from two protocols, with the states"""
	comp = compatible_paths(prot0, prot1)

	matches = []
	for pair in comp:
		for i in range(len(pair[0])):
			match = [pair[0][i].source, pair[0][i].msg.ct, pair[1][i].msg.ct]
			if not match in matches:
				matches.append(match)
	return matches


def alg_from_prag_alg1(prag_alg):
	""" Returns pragmatic mappings, no duplicates"""
	return list(set(alg_from_prag_alg2(prag_alg)))

def alg_from_prag_alg2(prag_alg):
	""" Returns pragmatic mappings"""
	return [(m[1],m[2]) for m in prag_alg]
