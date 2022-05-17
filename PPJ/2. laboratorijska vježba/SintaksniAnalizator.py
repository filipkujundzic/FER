#!/usr/bin/python3

import sys
#import pprint

stablo = ("<program>", [])
stog = [("<dno>",[]), stablo]
a = sys.stdin
ulaz = a.readlines() + ["<kraj_programa>"]

prev = None

def tip(s):
	#print("Ovo mi je " + s.split()[0])
	return s.split()[0]

def do_program():
	if(tip(ulaz[0]) in ["IDN", "KR_ZA", "<kraj_programa>"]):
		zamijeni(["<lista_naredbi>"])
	else:
		odbaci()

def do_lista_naredbi():
	if (tip(ulaz[0]) in ["IDN", "KR_ZA"]):
		zamijeni(["<lista_naredbi>", "<naredba>"])
	elif(tip(ulaz[0]) in ["KR_AZ", "<kraj_programa>"]):
		zamijeni("$")
	else:
		odbaci()

def do_naredba():
	if(tip(ulaz[0]) in ["IDN"]):
		zamijeni(["<naredba_pridruzivanja>"])
	elif(tip(ulaz[0]) in ["KR_ZA"]):
		zamijeni(["<za_petlja>"])
	else:
		odbaci()

def do_naredba_pridruzivanja():
	if(tip(ulaz[0]) in ["IDN"]):
		vrh = stog[-1]
		zamijeni(["<E>", "OP_PRIDRUZI", "IDN"])
	else:
		odbaci()

def ispisi(cvor, dubina):
	if(cvor[0][0] != '<'):
		#print("cvor" + str(cvor))
		print(" " * dubina + cvor[1][0][0].strip())
		return
	print(" " * dubina + cvor[0])
	for dijete in cvor[1]:
		ispisi(dijete, dubina + 1)

def do_za_petlja():
	if(tip(ulaz[0]) in ["KR_ZA"]):
		zamijeni(["KR_AZ","<lista_naredbi>","<E>","KR_DO","<E>","KR_OD","IDN","KR_ZA"])
	else:
		odbaci()

def do_t():
	if (tip(ulaz[0]) in ["IDN","BROJ","OP_PLUS","OP_MINUS","L_ZAGRADA"]):
		zamijeni(["<T_lista>","<P>"])
	else:
		odbaci()

def do_e_lista():
	if (tip(ulaz[0]) in ["OP_PLUS"]):
		zamijeni(["<E>","OP_PLUS"])
	elif (tip(ulaz[0]) in ["OP_MINUS"]):
		zamijeni(["<E>","OP_MINUS"])
	elif (tip(ulaz[0]) in ["IDN","KR_ZA","KR_DO","KR_AZ","D_ZAGRADA","<kraj_programa>"]):
		zamijeni("$")
	else:
		odbaci()

def do_t_lista():
	if(tip(ulaz[0]) in ["OP_PUTA"]):
		zamijeni(["<T>","OP_PUTA"])
	elif(tip(ulaz[0]) in ["OP_DIJELI"]):
		zamijeni(["<T>","OP_DIJELI"])
	elif(tip(ulaz[0]) in ["IDN","KR_ZA","KR_DO","KR_AZ","OP_PLUS","OP_MINUS","D_ZAGRADA","<kraj_programa>"]):
		zamijeni("$")
	else:
		odbaci()

def do_p():
	if(tip(ulaz[0]) in ["OP_PLUS"]):
		zamijeni(["<P>","OP_PLUS"])
	elif(tip(ulaz[0]) in ["OP_MINUS"]):
		zamijeni(["<P>","OP_MINUS"])
	elif(tip(ulaz[0]) in ["L_ZAGRADA"]):
		zamijeni(["D_ZAGRADA","<E>","L_ZAGRADA"])
	elif(tip(ulaz[0]) in ["IDN"]):
		zamijeni(["IDN"])
	elif(tip(ulaz[0]) in ["BROJ"]):
		zamijeni(["BROJ"])
	else:
		odbaci()

def odbaci():
	if(ulaz[0] == "<kraj_programa>"):
		print("err kraj")
	else:
		print("err " + ulaz[0], end='')
	sys.exit(0)

def pomakni():
	del ulaz[0]

def prihvati():
	#print("prihvaceno")
	#pprint.pprint(stablo)
	ispisi(stablo, 0)
	sys.exit(0)


def do_e():
	if(tip(ulaz[0]) in ["IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA"]):
		zamijeni(["<E_lista>","<T>"])
	else:
		odbaci()

prev = 0
tmp = ""
def zamijeni_i_pomakni():
	global prev
	global tmp
	vrh = stog.pop()
	#print("ovo je vrh: " + str(vrh))
	#print("ulaz: " + str(ulaz[0]))
	if(vrh[0] != "$"):
		if(prev == 1):
			#print("jedan je")
			vrh[1].append((ulaz[0],[]))
			pomakni()
			prev = 0
			tmp = ""
		else:
			vrh[1].append((ulaz[0],[]))
			pomakni()
	else:
		vrh[1].append((ulaz[0],[]))
		prev = 1
		tmp = ulaz[0]
		#print(tmp)
		#pomakni()
		#ulaz[0] = tmp

def korak():
	vrh = stog[-1][0]
	znak = ulaz[0]
	#print([vrh, znak])
	if (vrh == "<dno>" and znak == "<kraj_programa>"):
		prihvati()
		return

	if (vrh == tip(znak)):
		zamijeni_i_pomakni()
		return

	if (vrh == "<program>"):
		do_program()
		return

	if (vrh == "<lista_naredbi>"):
		do_lista_naredbi()
		return

	if (vrh == "<naredba>"):
		do_naredba()
		return

	if (vrh == "<naredba_pridruzivanja>"):
		do_naredba_pridruzivanja()
		return

	if(vrh == "<za_petlja>"):
		do_za_petlja()
		return

	if (vrh == "<T>"):
		do_t()
		return

	if(vrh == "<E_lista>"):
		do_e_lista()
		return

	if(vrh == "<T_lista>"):
		do_t_lista()
		return

	if (vrh == "<P>"):
		do_p()
		return

	if (vrh == "<E>"):
		do_e()
		return

	if(vrh == "$"):
		zamijeni_i_pomakni()
		return

	#print("evo me")
	odbaci()

def zamijeni(a):
	#print("pozvao zamijeni sa " + str(a))
	global prev
	if(a == "$"):
		for x in a:
			vrh = stog.pop()
			novi = (x, ["$"])
			stog.append(novi)
			vrh[1].insert(0,novi)
	else:
		vrh = stog.pop()
		#print("stog pop:" + str(vrh))
		for x in a:
			novi = (x, [])
			stog.append(novi)
			vrh[1].insert(0, novi)


while(True):
	korak()
	#print(ulaz,stog)

