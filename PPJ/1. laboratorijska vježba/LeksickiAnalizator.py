#!/usr/bin/python3

import sys
#fin = sys.stdin
#fin = "lab1/testovi1/test00/test.in"

sep = "//"
umnozak = ""
ima = 0

br_linije = 0
p = sys.stdin
a = p.readlines()
#with open(p) as fp:
	#provjeri da li je linija prazna	
	#broj linije
for line in a:
	if not line.strip():
		br_linije = br_linije + 1
	else:
		br_linije = br_linije + 1
	#preskoci liniju ako je komentar
	if(line.startswith(sep)):
		continue
	if(sep in line):   # ako je unutar linije // onda obrisi desni dio te linije (komentar)
		line = line.split(sep,1)[0] + "\n"
	
	#napravi niz sa znakovima iz linije
	if(line is not []):
		niz = line.strip().split()

	#print(niz)
	#ako imamo znak + unutar izraza, ali bez razmaka
	dodatni = 0
	for i in niz:
		if("+" in i and len(i)>=2 or "(" in i and len(i)>=2 or ")" in i and len(i)>=2 or "-" in i and len(i)>=2 or "*" in i and len(i)>=2 or "=" in i and len(i)>=2
			or "/" in i and len(i)>=2):
			del niz[dodatni]
			ind = 0
			tmp = ""
			d = 0
			a = 0
			duljina = len(i)
			for k in i:
				duljina = duljina - 1
				if(k.isdigit()):
					if("" not in tmp):
						niz.insert(ind + dodatni,str(tmp))
						tmp = ""
					if (d == 1):
						tmp = tmp + str(k)
						if(k == i[-1]):
							niz.insert(ind + dodatni,str(tmp))
							ind = ind + 1
							continue
						else:
							continue
					else:
						d = 1
						a = 0
						if ("" not in tmp):
							niz.insert(ind + dodatni,str(tmp))
							ind = ind + 1
							tmp = ""
						else:
							tmp = tmp + str(k)
							if(k == i[-1] and duljina == 0):
								niz.insert(ind + dodatni,str(tmp))
								ind = ind + 1
								continue
							else:
								continue
				if(k.isalpha()):
					if("" not in tmp):
						niz.insert(ind + dodatni,str(tmp))
						tmp = ""
					if (a == 1):
						tmp = tmp + str(k)
						if(k == i[-1]):
							niz.insert(ind + dodatni,str(tmp))
							ind = ind + 1
							continue
						else:
							continue
					else:
						a = 1
						d = 0
						if ("" not in tmp):
							niz.insert(ind + dodatni,str(tmp))
							ind = ind + 1
							tmp = ""
						else:
							tmp = tmp + str(k)
							if(k == i[-1] and duljina == 0):
								niz.insert(ind + dodatni,str(tmp))
								ind = ind + 1
								continue
							else:
								continue

				else:
					if(a == 1 or d == 1):
						niz.insert(ind + dodatni,str(tmp))
						ind = ind + 1
						
					tmp = ""
					tmp = tmp + str(k)
					a = d = 0
					niz.insert(ind + dodatni,str(tmp))
					ind = ind + 1
					tmp = ""
		dodatni = dodatni + 1

	#poseban slucaj - nema razmaka izmedu broja i identifikatora
	if(niz):
		if(niz[0][0].isdigit() and not niz[0].isdigit() and not "+" in niz and not "-" in niz):
			pomocni = []
			for i in niz:
				for j in i:
					pomocni.append(j)

			indeks = 0;
			kopiraj = 0
			for i in pomocni:
				if(i.isalpha() == True):
					kopiraj = i
					break
				indeks = indeks + 1

			niz1 = niz2 = ""
			niz1 = pomocni[:indeks]
			niz2 = pomocni[indeks:]
			
			drugiDio = ""
			prviDio = ""
			for i in niz1:
				prviDio = prviDio + i

			for i in niz2:
				drugiDio = drugiDio + i

			
			del niz[:]
			niz.append(str(prviDio))
			niz.append(str(drugiDio))

	for n in niz:
		#identifikatori
		if (n[0].isalpha() and not (n.startswith("za") and len(n) == 2) and not (n.startswith("az") and len(n) == 2)
			and not (n.startswith("od") and len(n) == 2) and not (n.startswith("do") and len(n) == 2)):
			print ("IDN " + str(br_linije) + " " + n)
		#operator =
		if (n == "="):
			print("OP_PRIDRUZI " + str(br_linije) + " " + n)
		#konstanta
		if (n.isdigit()):
			print("BROJ " + str(br_linije) + " " + n)
		#za
		if (n == "za"):
			print("KR_ZA " + str(br_linije) + " " + n)
		#od
		if (n == "od"):
			print("KR_OD " + str(br_linije) + " " + n)
		#do
		if (n == "do"):
			print("KR_DO " + str(br_linije) + " " + n)
		# +
		if (n == "+"):
			print("OP_PLUS " + str(br_linije) + " " + n)
		# -	
		if (n == "-"):
			print("OP_MINUS " + str(br_linije) + " " + n)
		# *
		if (n == "*"):
			print("OP_PUTA " + str(br_linije) + " " + n)
		# /
		if (n == "/"):
			print("OP_DIJELI " + str(br_linije) + " " + n)
		# az
		if (n == "az"):
			print("KR_AZ " + str(br_linije) + " " + n)
		# (
		if ( n == "("):
			print("L_ZAGRADA " + str(br_linije) + " " + n)
		# )
		if ( n == ")"):
			print("D_ZAGRADA " + str(br_linije) + " " + n)
