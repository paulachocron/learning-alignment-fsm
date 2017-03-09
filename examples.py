import random
from interaction import *
from generators import *

##################### EUROPE ##################### 
capitals = ['Tirana','Yerevan','Vienna','Baku','Minsk','Brussels','Sarajevo',
'Sofia','Zagreb','Nicosia','Prague','Copenhagen','Tallinn','Helsinki','Paris',
'Tbilisi','Berlin','Athens','Budapest','Reykjavik','Dublin','Rome','Astana','Pristina',
'Riga','Vaduz','Vilnius','Luxembourg','Skopje','Valletta','Chisinau','Monaco','Podgorica',
'Amsterdam','Oslo','Warsaw','Lisbon','Bucharest','Moscow','Belgrade','Bratislava',
'Ljubljana','Madrid','Stockholm','Bern','Ankara','Kyiv']


countries = ['Albania',	'Armenia','Austria','Azerbaijan','Belarus','Belgium','Bosnia','Bulgaria',
'Croatia','Cyprus','Czech','Denmark','Estonia','Finland','France','Georgia','Germany',
'Greece','Hungary','Iceland','Ireland','Italy','Kazakhstan','Kosovo','Latvia',	
'Liechtenstein','Lithuania','Luxembourg','Macedonia','Malta','Moldova','Monaco',
'Montenegro','Netherlands','Norway','Poland','Portugal','Romania','Russia',
'Serbia','Slovakia','Slovenia','Spain','Sweden','Switzerland','Turkey','Ukraine']

europe = []

europe_t = []

for i in range(int(len(capitals))):
	europe.append((countries[i],capitals[i],round(random.uniform(0.7,1),2)))

for i in range(int(len(capitals))):
	europe_t.append((capitals[i],countries[i],round(random.uniform(0.7,1),2)))


# THIS CREATES RANDOM PROTOCOLS AND ALIGNMENTS TO TEST AND SAVES THEM AS JSONS

# algEUHet = generate_heterogeneity(europe,countries,capitals,0.5,0.5)
# #print algEUHet
# algEUHet2 = invert_alg(algEUHet)


# f = open('examples/jsonALG-algEUHetn', 'w')		
# f.write(json.dumps(algEUHet))
# f.close()


# f = open('examples/jsonALG-algEUHet2n', 'w')		
# f.write(json.dumps(algEUHet2))
# f.close()

# proteu = generate_protocol(countries,40,36,1)
# proteu.set_name('proteun')

# proteu.to_json('examples/')

# prot2 = translate_protocol(proteu,europe)

# prot2.set_name('prot2jn')
# prot2.to_json('examples/')


######################## THIS USES EUROPE TO TEST THE PRAGMATIC ALIGNMENT
# protPrag0 = generate_protocol(countries,30,26,1)
# protPrag0.set_name('protPrag0')
# protPrag0.to_json('examples/')
# protPrag1 = translate_protocol(protPrag0,europe)
# protPrag1.set_name('protPrag1')
# protPrag1.to_json('examples/')

# problem1 = InteractionModel([0,1,2],[Transition(0,1,Message("say",1,0,'Barcelona')),
# 													 Transition(0,2,Message("say",1,0,'Paris')),],0,[1,2])

# #print europe
# algPr0 = get_pragmatic_alignment(protPrag0, protPrag1)
# algPr1 = get_pragmatic_alignment(protPrag1, protPrag0)

# print algPr0
# algPrag0 = generate_pragmatic_heterogeneity(algPr0, protPrag0, 0.6,0.5,countries,capitals)
# algPrag1 = generate_pragmatic_heterogeneity(algPr1, protPrag1, 0.6,0.5,capitals, countries)
# print algPrag0

# print len(algPr0)
# print len([p for p in algPrag0 if len([q for q in algPr0 if (p[0],p[1])==(q[1],q[2])])>0])
# print len(algPrag0)


# f = open('examples/jsonALG-algPrag0', 'w')		
# f.write(json.dumps(algPrag0))
# f.close()


# f = open('examples/jsonALG-algPrag1', 'w')		
# f.write(json.dumps(algPrag1))
# f.close()


###################### THIS IS THE TRAVEL AGENCY SCENARIO #########################

FalconC = [('Return', 'Package', 0.41), ('Single', 'RoundTrip', 0.19), 
('Customer', 'Booking', 0.05), ('RegisteredCustomer', 'User', 0.04), 
('UnregisteredCustomer', 'OneWay', 0.03), ('Result', 'Outcome', 0.01),
('Item', 'Product', 0.01), ('CurrentSearch', 'NonUser', 0.01),
('Search', 'Search', 0.01), ('Flight', 'Customer', 0.01),
('boardingPass', 'boardingPass', 1), ('destination', 'airlineCompany', 0.99),
('carrier', 'to', 0.99), ('numberOfPassengers', 'passengers', 0.99),
('departing', 'leavingDate', 0.99), ('origin', 'from', 0.99),
('hasCustomer', 'hasCustomer', 0.98), ('outboundTome', 'flexibleOnDates', 0.86),
('returning', 'returnDate' , 0.76), ('hasItem', 'hasProduct', 0.74),
('inboundTime', 'lodgerData', 0.63), ('guestDetails', 'passengerData', 0.56),
('numberOfRooms', 'rooms', 0.56), ('rate', 'stars', 0.56),
('passengerDetails', 'contactInfo', 0.56), ('checkIn', 'checkIn', 0.52),
('customerDetails', 'rulesAndRestrictions', 0.39), ('reservationTerms', 'payingInfo', 0.30),
('totalAmountToPay', 'totalPrice', 0.30), ('paymentInfo', 'hotelSummary', 0.30),
('reservationSummary', 'packageSummary', 0.30), ('hotelBookingsIn', 'city', 0.30),
('signOut', 'register', 0.30), ('numberOfGuests', 'nights', 0.30),
('hasIdentification', 'hasIdentification' , 0.30 ), ('signIn' , 'flightSummary' , 0.28 ),
('hasResult' , 'hasOutcome', 0.11)]

FalconTA = invert_alg(FalconC)

travelC = InteractionModel([0,1,2,3,4,5,6,7,8,9,10,11],
	[Transition(0,1,Message("say",1,0,'Flight')),
	 Transition(1,2,Message("say",1,0,'origin')),
	 Transition(2,3,Message("say",1,0,'destination')),
	 Transition(3,4,Message("say",1,0,'departing')),
	 Transition(4,5,Message("say",1,0,'Single')),
	 Transition(4,6,Message("say",1,0,'Return')),
	 Transition(6,5,Message("say",1,0,'returning')),
	 Transition(5,7,Message("say",0,1,'no')),
	 Transition(5,8,Message("say",0,1,'show')),
	 Transition(0,9,Message("say",1,0,'Hotel')),
	 Transition(9,10,Message("say",1,0,'hotelBookIn')),
	 Transition(10,11,Message("say",0,1,'show')),],
	0,[7,8,11])

travelTA = InteractionModel([0,1,2,3,4,5,6,7,8,9,10,11],
	[Transition(0,1,Message("say",1,0,'Flight')),
	 Transition(1,2,Message("say",1,0,'from')),
	 Transition(2,3,Message("say",1,0,'to')),
	 Transition(3,4,Message("say",1,0,'leavingDate')),
	 Transition(4,5,Message("say",1,0,'OneWay')),
	 Transition(4,6,Message("say",1,0,'RoundTrip')),
	 Transition(6,5,Message("say",1,0,'returnDate')),
	 Transition(5,7,Message("say",0,1,'no')),
	 Transition(5,8,Message("say",0,1,'show')),
	 Transition(0,9,Message("say",1,0,'Accomodation')),
	 Transition(9,10,Message("say",1,0,'city')),
	 Transition(10,11,Message("say",0,1,'show')) ],
		0,[7,8,11])


algC = Alignment(FalconC)
algTA = Alignment(FalconTA)



######################## AND THESE ARE OTHER INTERESTING TEST CASES

test0 = InteractionModel([1,2,3,4,5,6,7,8,9],[Transition(1,2,Message("say",0,1,'b')),
												 Transition(1,3,Message("say",0,1,'a')),
												 Transition(3,4,Message("say",0,1,'c')),
												 Transition(3,5,Message("say",0,1,'d')),
												 Transition(4,6,Message("say",0,1,'e')),
												 Transition(2,7,Message("say",0,1,'c')),
												 Transition(2,8,Message("say",0,1,'d')),
												 Transition(7,9,Message("say",0,1,'e'))],1,[5,6,9,8])


test1 = InteractionModel([1,2,3,4,5,6,7,8,9],[Transition(1,2,Message("say",0,1,'b1')),
												 Transition(1,3,Message("say",0,1,'a1')),
												 Transition(3,4,Message("say",0,1,'c1')),
												 Transition(3,5,Message("say",0,1,'d1')),
												 Transition(4,6,Message("say",0,1,'e1')),
												 Transition(2,7,Message("say",0,1,'c1')),
												 Transition(2,8,Message("say",0,1,'d1')),
												 Transition(7,9,Message("say",0,1,'e1'))],1,[5,6,9,8])

algt0 = [('b', 'a1', 0.5), ('c', 'c1', 0.6), ('d', 'd1', 0.6), 
			('e', 'e1', 0.6), ('f', 'f1', 0.9), ('a', 'b1', 0.5), ('g', 'g1', 0.6), ('h', 'h1', 0.6)]

algt1 = invert_alg(algt0)

algt0 = Alignment(algt0)
algt1 = Alignment(algt1)


testBETA = InteractionModel([1,2,3],[Transition(1,2,Message("say",0,1,'1a2')),
								 	Transition(1,3,Message("say",0,1,'1a3')),
								 	Transition(2,1,Message("say",0,1,'2a1')),
									Transition(2,3,Message("say",0,1,'2a3'))],1,[3])


# test11 = InteractionModel([1,2,3],[Transition(1,2,Message("say",0,1,'b1')),
# 												 Transition(1,3,Message("say",0,1,'a1')),
# 												 Transition(3,4,Message("say",0,1,'c1')),
# 												 Transition(3,5,Message("say",0,1,'d1')),
# 												 Transition(4,6,Message("say",0,1,'e1')),
# 												 Transition(2,7,Message("say",0,1,'f1')),
# 												 Transition(2,8,Message("say",0,1,'g1')),
# 												 Transition(7,9,Message("say",0,1,'h1'))],1,[5,6,9,8])

# algt00 = [('b', 'a1', 0.5), ('c', 'f1', 0.6), ('d', 'g1', 0.6), 
# 			('e', 'h1', 0.6), ('f', 'c1', 0.9), ('a', 'b1', 0.5), ('g', 'd1', 0.6), ('h', 'e1', 0.6)]

# algt11 = invert_alg(algt00)

# algt00 = Alignment(algt00)
# algt11 = Alignment(algt11)

if not remote:
	problem1 = InteractionModel([1,2,3,4,5,6,7,8,9,10,11,12],[Transition(1,2,Message("say",1,0,'Madrid')),
													 Transition(2,3,Message("say",1,0,'Paris')),
													 Transition(2,4,Message("say",1,0,'Brussels')),
													 Transition(3,5,Message("say",1,0,'Lisbon')),
													 Transition(5,7,Message("say",1,0,'Amsterdam')),
													 Transition(4,6,Message("say",1,0,'Lisbon')),
													 Transition(4,8,Message("say",1,0,'Rome')),
													 Transition(8,10,Message("say",0,1,'Bern')),
													 Transition(3,9,Message("say",1,0,'Berlin')),
													 Transition(9,11,Message("say",1,0,'Berlin')),
													 Transition(11,12,Message("say",0,1,'Athens'))],1,[6,7,10,12])


	problem0 = InteractionModel([1,2,3,4,5,6,7,8,9,10,11,12],[Transition(1,2,Message("say",1,0,'Spain')),
													 Transition(2,3,Message("say",1,0,'France')),
													 Transition(2,4,Message("say",1,0,'Belgium')),
													 Transition(3,5,Message("say",1,0,'Portugal')),
													 Transition(5,7,Message("say",1,0,'Netherlands')),
													 Transition(4,6,Message("say",1,0,'Portugal')),
													 Transition(4,8,Message("say",1,0,'Italy')),
													 Transition(8,10,Message("say",0,1,'Switzerland')),
													 Transition(3,9,Message("say",1,0,'Germany')),
													 Transition(9,11,Message("say",1,0,'Germany')),
													 Transition(11,12,Message("say",0,1,'Greece'))],1,[6,7,10,12])


	# algp0 = [('Spain', 'Madrid', 0.9), ('France', 'Brussels', 0.9), ('Belgium', 'Paris', 0.9), ('Portugal', 'Lisbon', 0.9), ('Netherlands', 'Amsterdam', 0.9), ('Italy','Rome', 0.9), ('Germany','Berlin', 0.9)]

	# algp1 = invert_alg(algp0)

	# prot0 = IM_from_json('examples/jsonIM-proteun')
	# prot1 = IM_from_json('examples/jsonIM-prot2jn')
	# f = open('examples/jsonALG-algEUHetn', 'r')
	# f2 = open('examples/jsonALG-algEUHet2n', 'r')

	# alg0 = Alignment(json.JSONDecoder().decode(f.read()))
	# alg1 = Alignment(json.JSONDecoder().decode(f2.read()))

	# f.close()
	# f2.close()

	# algp0 = Alignment(algp0)
	# algp1 = Alignment(algp1)

	# protPrag0 = IM_from_json('examples/jsonIM-protPrag0')
	# protPrag1 = IM_from_json('examples/jsonIM-protPrag1')
	# f = open('examples/jsonALG-algPrag0', 'r')
	# f2 = open('examples/jsonALG-algPrag1', 'r')

	# algPrag0 = Alignment(json.JSONDecoder().decode(f.read()))
	# algPrag1 = Alignment(json.JSONDecoder().decode(f2.read()))

	# f.close()
	# f2.close()

counts = ['Spain', 'France', 'Portugal', 'Netherlands', 'Germany', 'Greece', 'Belgium', 'Italy', 'Switzerland']

caps = ['Madrid','Paris','Lisbon', 'Amsterdam', 'Berlin', 'Athens','Brussels','Rome','Bern']

