from common_algorithms import Fraction

TRIVIAL_MULTIPLICATION_BOUND = 8


class Matrix:

	def __init__(self, i:int =1, j:int =1, file_name:str = '', fract:bool=0):
		self.fract = fract
		if file_name != '':
			self.init_file(file_name, fract)
		else:
			self.init_indentity(i, j)

	def init_indentity(self, i:int, j:int) -> None:
		self.i, self.j = max(1, i), max(1, j)
		self.a = [[0 if i!=j else 1 for j in range(self.j)] for i in range(self.i)]

	def init_file(self, file_name:str, fract:bool=0) -> None:
		self.a = []
		self.i, j = 0, 0
		file = open(file_name)

		for line in file:
			self.i += 1
			line = line.split(' ')
			self.a.append([])
			for n in line:
				if not fract:
					self.a[self.i-1].append(int(n))
				else:
					self.a[self.i-1].append(Fraction(n))
				j += 1
			self.j = j
			j = 0
		file.close()

	def init_str(self, i:int, j:int, s:str) -> None:
		self.a = []
		s = s.split(' ')[::-1]
		for n in range(i):
			self.a.append([])
			for m in range(j):
				self.a[n].append(s.pop())
		self.i, self.j = i, j

	def out_console(self) -> None:
		for n in self.a:
			for m in n:
				print(m, sep = '', end = '\t')
			print('\n\n', end = '')

	def transposition(self) -> None:
		a = [[self.a[m][n] for m in range(self.i)] for n in range(self.j)]
		self.a, self.i, self.j = a, self.j, self.i

	def fill_to_size(self, size:int = 2) -> None:
		if (size == self.i) and (size == self.j):
			return

		while size < max(self.i, self.j):
			size *= 2
		
		for i in range(self.i):
			for j in range(size - self.j):
				if a.fract:
					self.a[i].append(Fraction())
				else:
					self.a[i].append(0)

		while self.i < size:
			self.i += 1
			if a.fract:
				self.a.append([Fraction() for j in range(size)])
			else:
				self.a.append([0 for j in range(size)])
		self.i, self.j =size, size

	def cut_to_size(self, i:int, j:int) -> None:
		self.a = [[self.a[r][c] for c in range(j)] for r in range(i)]
		self.i, self.j = i, j

	def concatenate_from_2x2(self, m2x2:list) -> None:
		self.i, self.j = m2x2[0][0].i + m2x2[1][0].i, m2x2[0][0].j + m2x2[0][1].j
		self.a = [[] for i in range(self.i)]
		for i in range(m2x2[0][0].i):
			self.a[i] = m2x2[0][0].a[i] + m2x2[0][1].a[i]
			self.a[m2x2[0][0].i+i] = m2x2[1][0].a[i] + m2x2[1][1].a[i]

	def nullify(self) -> None:
		self.a = [[0 for j in range(self.j)] for i in range(self.i)]

	def det(self) -> float:
		if self.i == 2:
			return self.a[0][0]*self.a[1][1] - self.a[1][0]*self.a[0][1]
		else: 
			if self.i == 1: 
				return self.a[0][0]

		k = 0
		res = 0
		calc = Matrix(self.i, self.j)
		#self.out_console()
		#print()
		calc.a = [list(self.a[i]) for i in range(self.i)]
		if calc.a[0][0] == 0:
			for i in range(calc.i):
				if (calc.a[i][0] != 0) and (k == 0):
					calc.a[0] = self.a[i]
					calc.a[i] = self.a[0]
					k += 1
		if calc.a[0][0] == 0:
			return 0

		for i in range(self.i - 1):
			res = calc.a[i+1][0]
			for j in range(self.j):
				calc.a[i+1][j] -= calc.a[0][j]*(res/calc.a[0][0])
		#calc.out_console()
		if k:
			res = -self.a[0][0]
		else:
			res = self.a[0][0]
		calc.a = [[calc.a[i+1][j+1] for j in range(self.j-1)] for i in range(self.i-1)]
		calc.i, calc.j = self.i -1, self.j -1
		res *= calc.det()
		return res

	def __neg__(self):
		self.a = [[-self.a[i][j] for j in range(self.j)] for i in range(self.i)]

	def __add__(self, other):
		res = Matrix(self.i, self.j)
		res.a = [[(self.a[i][j] + other.a[i][j]) for j in range(res.j)] for i in range(res.i)]
		return res

	def __sub__(self, other):
		res = Matrix(self.i, self.j)
		res.a = [[(self.a[i][j] - other.a[i][j]) for j in range(res.j)] for i in range(res.i)]
		return res

	def __eq__(self, other) -> bool:
		if (self.i, self.j) != (other.i, other.j):
			return 0
		for i in range(self.i):
			for j in range(self.j):
				if self.a[i][j] != other.a[i][j]:
					return 0
		return 1


def multMatrix(a:Matrix, b:Matrix) -> Matrix:
	res = Matrix(a.i, b.j)
	for i in range(res.i):
		for j in range(res.j):
			if i == j:
				res.a[i][j] -= 1
			for r in range(a.j):
				res.a[i][j] += a.a[i][r]*b.a[r][j]
	return res

def copy_matrix(a:Matrix, from_i:int, from_j:int, to_i:int, to_j:int) -> Matrix:
	copy = Matrix(to_i - from_i, to_j - from_j)
	copy.i, copy.j = (to_i - from_i), (to_j - from_j)
	for i in range(copy.i):
		for j in range(copy.j):
			copy.a[i][j] = a.a[from_i+i][from_j+j]
	return copy

def split_to_2x2(a:Matrix) -> list:
	return [[copy_matrix(a, 0, 0, a.i//2, a.j//2),   copy_matrix(a, 0, a.j//2, a.i//2, a.j)], 
			[copy_matrix(a, a.i//2, 0, a.i, a.j//2), copy_matrix(a, a.i//2, a.j//2, a.i, a.j)]]

def multStrassen(a:Matrix, b:Matrix) -> Matrix:
	
	assert (a.j == b.i)
	i, j = a.i, b.j
	res = Matrix()
	size = 2
	while size < max(a.i, a.j, b.i, b.j):
		size *= 2
	a.fill_to_size(size)
	b.fill_to_size(size)

	if a.i <= TRIVIAL_MULTIPLICATION_BOUND:
		res = multMatrix(a, b)
		res.cut_to_size(i, j)
		return res

	res.concatenate_from_2x2(multStrassen2x2(*map(split_to_2x2, [a, b])))
	res.cut_to_size(i, j)
	return res

def multStrassen2x2(lb:list, rb:list) -> list:
	d = multStrassen(lb[0][0] + lb[1][1], rb[0][0] + rb[1][1])
	d_1 = multStrassen(lb[0][1] - lb[1][1], rb[1][0] + rb[1][1])
	d_2 = multStrassen(lb[1][0] - lb[0][0], rb[0][0] + rb[0][1])

	left = multStrassen(lb[1][1], rb[1][0] - rb[0][0])
	right = multStrassen(lb[0][0], rb[0][1] - rb[1][1])
	top = multStrassen(lb[0][0] + lb[0][1], rb[1][1])
	bottom = multStrassen(lb[1][0] + lb[1][1], rb[0][0])

	return [[d + d_1 + left - top, right + top],
			[left + bottom, d + d_2 + right - bottom]]



if __name__ == '__main__':
	a = Matrix(file_name = 'inputA.txt', fract=1)
	b = Matrix(file_name = 'inputB.txt')
	print(b.det())
	print(a.det())
	a.out_console()
	(a+b).out_console()
	multStrassen(a, b).out_console()