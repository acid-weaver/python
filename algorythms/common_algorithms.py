def gcd(a:int, b:int) -> int:
	'''
	Euclidian algotithm for GCD (greatest common divisor)
	'''
	while (a != 0) and (b != 0):
		if a > b:
			a %= b
		else:
			b %= a

	return a + b


class Fraction():
	'''Fraction a/b'''

	def __init__(self, n=0, b:int=1):
		self.a = n
		self.b = b

		if isinstance(n, Fraction):
			self = n

		if isinstance(n, str):
			self.read(n)
			return	#in self.read(n) we already have self.reduction()

		if isinstance(n, float):
			while abs(n - int(n)) > 0.000001:
				n *= 10
				b *= 10
			self.a = int(n)
			self.b = b

		self.reduction()

	def __numerators_compare(self, other) -> tuple:
		other = Fraction(other)        
		return self.a*other.b, other.a*self.b

	def read(self, input:str, i:int = 0, sep:set = {' ', '\n', '\t'}):
		part = 0
		self.a = 0
		self.b = 0
		
		while ( i<len(input) ) and ( input[i] not in sep):
			if input[i] == '/':
				part = 1
			else:
				if not part:
					self.a = self.a*10 + int(input[i])
				else:
					self.b = self.b*10 + int(input[i])
			i += 1

		if (self.b == 0) and (part == 0):
			self.b = 1

		self.reduction()

	def reduction(self) -> None:
		if (self.a < 0) != (self.b < 0):
			self.a = -abs(self.a)
			self.b =  abs(self.b)
		else:
			self.a = abs(self.a)
			self.b = abs(self.b)

		n = gcd(abs(self.a), abs(self.b))
		while n != 1:
			self.a = self.a // n
			self.b = self.b // n
			n = gcd(abs(self.a), abs(self.b))

	def value(self) -> float:
		return self.a / self.b

	#to print
	def __str__(self) -> str:
		if self.b != 1:
			return str(self.a) + '/' + str(self.b)
		else:
			return str(self.a)

	#compare operators
	def __lt__(self, other) -> bool:
		a, b = self.__numerators_compare(other)
		return a < b

	def __le__(self, other) -> bool:
		a, b = self.__numerators_compare(other)
		return a <= b

	def __eq__(self, other) -> bool:
		a, b = self.__numerators_compare(other)
		return a == b

	def __ne__(self, other) -> bool:
		a, b = self.__numerators_compare(other)
		return a != b

	def __gt__(self, other) -> bool:
		a, b = self.__numerators_compare(other)
		return a > b

	def __ge__(self, other) -> bool:
		a, b = self.__numerators_compare(other)
		return a >= b

	#arithmetic operators
	def __abs__(self):
		return Fraction(abs(self.a), self.b)

	def __float__(self):
		return self.a / self.b

	def __add__(self, other):
		other = to_Fraction(other)

		num = self.a*other.b + other.a*self.b
		den = self.b*other.b
		return Fraction(num, den)

	def __radd__(self, other):
		return (self + other)

	def __iadd__(self, other):
		return (self + other)

	def __sub__(self, other):
		other = to_Fraction(other)

		num = self.a*other.b - other.a*self.b
		den = self.b * other.b
		return Fraction(num, den)

	def __rsub__(self, other):
		return (self - other)

	def __isub__(self, other):
		return (self - other)

	def __mul__(self, other):
		other = to_Fraction(other)

		num = self.a * other.a
		den = self.b * other.b
		return Fraction(num, den)

	def __imul__(self, other):
		return (self * other)

	def __truediv__(self, other):
		other = to_Fraction(other)

		num = self.a * other.b
		den = self.b * other.a
		return Fraction(num, den)

	def __pow__(self, other):
		other = to_Fraction(other)

		num = self.a ** other.value
		den = self.b ** other.value
		return Fraction(num, den)



def to_Fraction(n) -> Fraction:
	if isinstance(n, Fraction):
		return n

	if isinstance(n, int):
		return Fraction(n)
	
	den = 1
	if isinstance(n, float):
		while abs(n - int(n)) > 0.000001:
			n *= 10
			den *= 10
		return Fraction(int(n), den)

	return Fraction()

# def add_fractions(a : Fraction, b : Fraction) -> Fraction:
#     num = a.a*b.b + b.a*a.b
#     den = a.b * b.b
#     return Fraction(num, den)



if __name__ == '__main__':
	a = Fraction(-1, 10)
	b = Fraction(4, 20)
	print(b / a)
	a.read('571')
	print(a)
	print(a * b)
	pass