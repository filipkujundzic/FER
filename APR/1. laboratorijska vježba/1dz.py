# Analiza i projektiranje racunalom
# 1DZ

epsilon = 1e-9
#epsilon = 1e-6

def loadMatrix(matrixname):
	filepath = matrixname
	
	with open(filepath) as f:
		content = f.readlines()

	content = [x.strip() for x in content]

	content2 = []
	for i in content:
		content2.append(i.split())

	matrix = []
	for i in content2:
		row = []
		for k in i:
			row.append(float(k))
		matrix.append(row)

	return matrix

def equal(matrixX, matrixY):
	matrixX = matrixY.copy()
	return matrixX

def number_of_rows(matrix):
	return len(matrix)

def number_of_columns(matrix):
	return len(matrix[0])

def print_matrix_file(matrix,path):
	file = open(path, "w") #Create - will create a file, returns an error if the file exist

	for i in matrix:
		string = [str(j) for j in i] 
		file.write( ", ".join(str(e) for e in string))
		file.write("\n")

	file.close()

def print_matrix(matrix):
	for i in matrix:
		tmp_list = i
		print(*i, sep=" ")
		#the star unpacks the list and return every element in the list. 
	print("\n")


def set_element(matrix,row,column,value):
	matrix[row][column] = value

def get_element(matrix,row,column):
	print(matrix[row][column])

def sum(matrixA, matrixB):
	if(number_of_rows(matrixA) != number_of_rows(matrixB) or (number_of_columns(matrixA) != number_of_columns(matrixB))):
		print("Nije moguce zbrojiti matrice zbog razlicitih dimenzija.")
		return

	result = []

	for i in range(0, len(matrixA)):
		line = []
		for j in range(0, len(matrixA[i])):
			line.append(matrixA[i][j] + matrixB[i][j])
		result.append(line)
			
	return result

def sub(matrixA,matrixB):
	if(number_of_rows(matrixA) != number_of_rows(matrixB) or (number_of_columns(matrixA) != number_of_columns(matrixB))):
		print("Nije moguce oduzeti matrice zbog razlicitih dimenzija.")
		return

	result = []

	for i in range(0, len(matrixA)):
		line = []
		for j in range(0, len(matrixA[i])):
			line.append(matrixA[i][j] - matrixB[i][j])
		result.append(line)
			
	return result

def product(matrixA,matrixB):
	if(number_of_columns(matrixA) != number_of_rows(matrixB)):
		print("Matrice nisu ulancane pa ih nije moguce pomnoziti.")

	result = []

	for i in range(0, number_of_rows(matrixA)):
		line = []
		for j in range(0, number_of_columns(matrixB)):
			zbroj = 0
			for k in range(0, number_of_columns(matrixA)):
				zbroj = zbroj + matrixA[i][k] * matrixB[k][j]
			line.append(zbroj)
		result.append(line)

	return result

def transpose(matrix):
	transp = []
	for i in range(0, number_of_columns(matrix)):
		line = []
		for j in range(0, number_of_rows(matrix)):
			line.append(matrix[j][i])
		transp.append(line)
	return transp

def operator_plusequal(matrix, constant):
	result = []
	for i in range(0, number_of_rows(matrix)):
		line = []
		for j in range(0, number_of_columns(matrix)):
			line.append(matrix[i][j] + constant)
		result.append(line)

	return result


def operator_minusequal(matrix, constant):
	result = []
	for i in range(0, number_of_rows(matrix)):
		line = []
		for j in range(0, number_of_columns(matrix)):
			line.append(matrix[i][j] - constant)
		result.append(line)

	return result

def product_scalar(matrix,constant):
	result = []
	for i in range(0, number_of_rows(matrix)):
		line = []
		for j in range(0, number_of_columns(matrix)):
			line.append(matrix[i][j] * constant)
		result.append(line)

	return result

def comapre_matrices(matrixA,matrixB):
	if(number_of_rows(matrixA) != number_of_rows(matrixB) or number_of_columns(matrixA) != number_of_columns(matrixB)):
		print("Matrice nisu jednakih dimenzija te se ne mogu usporediti.\n")
	for i in range(0,number_of_rows(matrixA)):
		for j in range(0, number_of_columns(matrixB)):
			if(abs(matrixA[i][j] - matrixB[i][j])) > epsilon:
				return 0
	return 1

def forward_supstitution(matrix,vector):
	for i in range(0, number_of_rows(matrix) -1):
		for j in range(i +1, number_of_rows(matrix)):
			vector[j][0] -= matrix[j][i] * vector[i][0]

	return vector


def backward_supstitution(matrix,vector):
	for i in range(number_of_rows(matrix)-1,-1,-1):
		if(abs(matrix[i][i])) < epsilon:
			print("Divisor is zero!")
			return
		vector[i][0] /= matrix[i][i]
		b = vector[i][0]
		for j in range(0, i):
			vector[j][0] -= matrix[j][i]*b

	return vector


def LU_decomposition(matrix):
	for i in range(0, number_of_rows(matrix)-1):
		for j in range(i+1,number_of_rows(matrix)):
			if(abs(matrix[i][i]) < epsilon):
				print("Division by zero!")
				return
			matrix[j][i] /= matrix[i][i]
			for k in range(i+1, number_of_rows(matrix)):
				matrix[j][k]-=matrix[j][i]*matrix[i][k]
		#print_matrix(matrix)
	return

def substitute(lista,i,j):
	temp = lista[i]
	lista[i] = lista[j]
	lista[j] = temp


def substitute_rows(matrix,a,b):
	temp = matrix[a]
	matrix[a] = matrix[b]
	matrix[a] = temp


def rearange(matrix,lista):
	copy = []
	for i in range(0,len(lista)):
		copy.append(matrix[lista[i]])

	matrix = copy
	return matrix

def LUP_decomposition(matrix):
	P = []
	
	for i in range(0, number_of_rows(matrix)):
		P.append(i) 

	for i in range(0, number_of_rows(matrix)-1):
		pivot = i
		for j in range(i +1, number_of_rows(matrix)):
			if(abs(matrix[P[j]][i]) > abs(matrix[P[pivot]][i])):
				pivot = j
		substitute(P,i,pivot)
		for j in range(i + 1, number_of_rows(matrix)):
			matrix[P[j]][i] /= matrix[P[i]][i]
			for k in range(i + 1, number_of_rows(matrix)):
				matrix[P[j]][k] -= matrix[P[j]][i] * matrix[P[i]][k]
	
	matrix = rearange(matrix,P)
	return matrix


def LUP_decomposition_get_A_P(matrix):
	P = []
	AP = []
	
	for i in range(0, number_of_rows(matrix)):
		P.append(i) 

	for i in range(0, number_of_rows(matrix)-1):
		pivot = i
		for j in range(i +1, number_of_rows(matrix)):
			if(abs(matrix[P[j]][i]) > abs(matrix[P[pivot]][i])):
				pivot = j
		if(abs(matrix[pivot][pivot]) < epsilon):
			raise("Pivot is zero!")
			return
		substitute(P,i,pivot)
		for j in range(i + 1, number_of_rows(matrix)):
			matrix[P[j]][i] /= matrix[P[i]][i]
			for k in range(i + 1, number_of_rows(matrix)):
				matrix[P[j]][k] -= matrix[P[j]][i] * matrix[P[i]][k]

	matrix = rearange(matrix,P)

	p1 = []
	p1.append(P)
	AP.append(matrix)
	AP.append(p1)

	return AP

def get_L(matrix):
	L = []
	for i in range(0, number_of_rows(matrix)):
		line = []
		for j in range(0, number_of_rows(matrix)):
			if(i == j):
				line.append(1.0)
			if(j > i):
				line.append(0.0)
			if(i > j):
				line.append(matrix[i][j])
		L.append(line)
	return L

def get_U(matrix):
	U = []
	for i in range(0, number_of_rows(matrix)):
		line = []
		for j in range(0, number_of_rows(matrix)):
			if(i == j):
				line.append(matrix[i][j])
			if(j > i):
				line.append(matrix[i][j])
			if(i > j):
				line.append(0.0)
		U.append(line)
	return U

def generate_e(n,indeks):
	e = []
	for i in range(0,n):
		if(i == indeks):
			e.append([1.0])			
		else:
			e.append([0.0])
	return e


def inverse(matrix):
	n = number_of_rows(matrix)
	inv = []
	
	AP = LUP_decomposition_get_A_P(matrix)
	A = AP[0]
	
	P = AP[1]
	L = get_L(A)
	U = get_U(A)

	for i in range(0,n):
		ei = generate_e(n,i)
		e_rearange = rearange(ei, P[0])
		y = forward_supstitution(L,e_rearange)
		x = backward_supstitution(U,y)
		inv.append(x)

	inv = transpose(inv)

	result = []
	for i in range(0, n):
		line = []
		for j in range(0,n):
			line.append(inv[i][j][0])
		result.append(line)
	print_matrix(result)

def number_of_permutations(vector):
	#print(vector[0])
	number = 0
	for i in range(0,len(vector[0])):
		if(vector[0][i] != 0):
			number = number + 1

	return number

def diagonal_product(matrix):
	product = 1
	for i in range(number_of_rows(matrix)):
		for j in range(number_of_rows(matrix)):
			if(i == j):
				product *= matrix[i][j]
	if(abs(product) < epsilon):
		product = 0
	return product

def determinant(matrix):
	AP = LUP_decomposition_get_A_P(matrix)
	A = AP[0]
	
	P = AP[1]
	L = get_L(A)
	U = get_U(A)
	
	number = number_of_permutations(P)
	if(abs(number) < epsilon):
		number = 0
	elif(number == 0 or number %2 == 0):
		number = 1
	elif(number %2 == 1):
		number = -1

	diagonal_L = diagonal_product(L)
	diagonal_U = diagonal_product(U)
	return number * diagonal_L * diagonal_U

def test():
	A = []
	B = []
	C = []
	zbroj = []
	razlika = []
	A = loadMatrix("A.txt")
	print(A)
	print("Ovo je B prije pozivanja metode equal:")
	print(B)
	print("Ovo je B nakon pozivanja metode equal:")
	B = equal(B,A) # B = A
	print(B)
	print("Broj redaka matrice A:")
	print(number_of_rows(A))
	print("Broj stupaca matrice A:")
	print(number_of_columns(A))
	print("Ispis matrice:")
	print_matrix(A)
	print_matrix_file(A,"datoteka.txt")
	set_element(A,1,1,100)
	print("\n")
	print_matrix(A)
	get_element(A,1,3)
	B = loadMatrix("B.txt")
	print_matrix(B)
	C = loadMatrix("C.txt")
	sum(A,C)
	zbroj = sum(A,B)
	print_matrix(zbroj)
	razlika = sub(A,B)
	print_matrix(razlika)

	####

	A1 = []
	B1 = []
	umnozak = []
	A1 = loadMatrix("A1.txt")
	B1 = loadMatrix("B1.txt")
	umnozak = product(A1,B1)
	print_matrix(umnozak)
	print("\n")

	####

	T = []
	T = transpose(A1)
	print_matrix(T)
	print("\n")

	####

	A = operator_plusequal(A,100)
	print_matrix(A)
	print("\n")
	
	####

	B = operator_minusequal(B,10)
	print_matrix(B)
	print("\n")

	####

	M = []
	print_matrix(A)
	M = product_scalar(A,0.5)
	print("\n")
	print_matrix(M)

	####

	A = []
	B = []
	A = loadMatrix("A.txt")
	print_matrix(A)
	B = loadMatrix("A.txt")
	print_matrix(B)
	if(comapre_matrices(A,B)):
		print("Matrice A i B su jednake.")

	####

	print("\nLU dekompozicija:")
	e1 = []
	e1 = loadMatrix("LU.txt")
	print_matrix(e1)
	LU_decomposition(e1)
	print_matrix(e1)

	####

	print("\nLUP dekompozicija:")
	lup = []
	lup = loadMatrix("LUP.txt")
	print("\n")
	print_matrix(lup)
	lup = LUP_decomposition(lup)
	print_matrix(lup)


	####

	C = []
	C = loadMatrix("C.txt")
	print_matrix(C)
	Lc = get_L(C)
	print_matrix(Lc)


	####

	C = []
	C = loadMatrix("C.txt")
	print_matrix(C)
	Uc = get_U(C)
	print_matrix(Uc)


	####

	print("Trazimo inverz")
	inv = []
	inv = loadMatrix("inverz.txt")
	print_matrix(inv)
	inverse(inv)

	####

	print("Trazimo determinantu")
	det = []
	det = loadMatrix("det.txt")
	print_matrix(det)
	result = determinant(det)
	print(result)


#test()

def main():
	print("\n1] ZADATAK\n")
	A1 = loadMatrix("1A.txt")
	
	r1 = []
	const = 0.2474820938409035792433
	print_matrix(A1)
	print("Konstanta kojom smo mnozili " + str(const))
	r1 = product_scalar(A1,const)
	r2 = product_scalar(r1,1/const)

	print(A1[0][0] == r2[0][0])
	print(comapre_matrices(A1,r2))
######################################################################################
	print("\n2] ZADATAK\n")
	print("LU")

	A2 = loadMatrix("2A.txt")
	b2 = loadMatrix("2b.txt") 

	try:
		lu = LU_decomposition(A2)
		L1 = get_L(lu)
		U1 = get_U(lu)
		y = forward_supstitution(L,b2)
		x = backward_supstitution(U,y)
		print(x)
	except:
		print("Greška - dijeljenje nulom\n")


	print("LUP")
	A2 = loadMatrix("2A.txt")
	b2 = loadMatrix("2b.txt") 

	AP = LUP_decomposition_get_A_P(A2)
	A = AP[0]

	P = AP[1]
	L = get_L(A)
	U = get_U(A)
	y = forward_supstitution(L,rearange(b2,P[0]))
	x = backward_supstitution(U,y)

	print_matrix(x)
######################################################################################
	print("\n3] ZADATAK\n")
	A3 = loadMatrix("3A.txt")
	print_matrix(A3)
	LU_decomposition(A3)
	print("LU")
	print_matrix(A3)

	print("LUP")
	try:
		A3 = loadMatrix("3A.txt")
		A3 = LUP_decomposition_get_A_P(A3)
		print_matrix(A3[0])
	except:
		print("Greška")

	print("Rješavanje sustava LUP dekompozicijom")
	A3 = loadMatrix("3A.txt")
	print_matrix(A3)
	b3 = loadMatrix("3b.txt")

	AP = LUP_decomposition_get_A_P(A3)
	A = AP[0]

	P = AP[1]
	L = get_L(A)
	U = get_U(A)
	y = forward_supstitution(L,rearange(b3,P[0]))
	x= backward_supstitution(U,y)

######################################################################################
	print("\n4] ZADATAK\n")
	A4 = loadMatrix("4A.txt")
	print_matrix(A4)
	b4 = loadMatrix("4b.txt")
	print_matrix(b4)

	print("LU")

	LU_decomposition(A4)
	L = get_L(A4)
	U = get_U(A4)
	y = forward_supstitution(L,b4)
	x = backward_supstitution(U,y)
	print_matrix(x)

	print("LUP")
	A4 = loadMatrix("4A.txt")
	b4 = loadMatrix("4b.txt")
	AP = LUP_decomposition_get_A_P(A4)
	A = AP[0]

	P = AP[1]
	L = get_L(A)
	U = get_U(A)
	y = forward_supstitution(L,rearange(b4,P[0]))
	x= backward_supstitution(U,y)
	print_matrix(x)

######################################################################################
	print("\n5] ZADATAK\n")
	A5 = loadMatrix("5A.txt")
	print_matrix(A5)
	b5 = loadMatrix("5b.txt")
	print_matrix(b5)

	print("LU")
	try:
		LU_decomposition(A5)
		L = get_L(A5)
		U = get_U(A5)
		y = forward_supstitution(L,b5)
		x = backward_supstitution(U,y)
		print_matrix(x)
	except:
		print("Greška")

	print("LUP")
	A5 = loadMatrix("5A.txt")
	b5 = loadMatrix("5b.txt")
	AP = LUP_decomposition_get_A_P(A5)
	A = AP[0]

	P = AP[1]
	L = get_L(A)
	U = get_U(A)
	y = forward_supstitution(L,rearange(b5,P[0]))
	x= backward_supstitution(U,y)
	print_matrix(x)

######################################################################################
	print("\n6] ZADATAK\n")
	print("LUP")
	A6 = loadMatrix("6A.txt")
	print_matrix(A6)

	for i in range(0, number_of_rows(A6)):
		A6[0][i] /= 1e+9

	for i in range(0, number_of_rows(A6)):
		A6[2][i] *= 1e+9

	print_matrix(A6)
	b6 = loadMatrix("6b.txt")
	print_matrix(b6)
	b6[0][0] /= 1e+9
	b6[2][0] *= 1e+9
	print_matrix(b6)

	AP = LUP_decomposition_get_A_P(A6)
	A = AP[0]

	P = AP[1]
	L = get_L(A)
	U = get_U(A)
	y = forward_supstitution(L,rearange(b6,P[0]))
	x= backward_supstitution(U,y)
	print_matrix(x)

######################################################################################
	print("\n7] ZADATAK\n")
	print("Računanje inverza")
	A7 = loadMatrix("7A.txt")
	print_matrix(A7)
	det = determinant(A7)
	if(abs(det) == 0):
		print("Determinanta je 0, matrica nema inverza.")

######################################################################################
	print("\n8] ZADATAK\n")
	print("Računanje inverza LUP dekompozicijom")
	A8 = loadMatrix("8A.txt")
	print_matrix(A8)
	inv = []
	inv = inverse(A8)

######################################################################################
	print("\n9] ZADATAK\n")
	print("Računanje determinante")
	A9 = loadMatrix("9A.txt")
	print_matrix(A9)
	det = determinant(A9)
	print(det)

######################################################################################
	print("\n10] ZADATAK\n")
	print("Računanje determinante")
	A10 = loadMatrix("10A.txt")
	print_matrix(A10)
	det = determinant(A10)
	print(det)


main()