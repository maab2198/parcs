# import gmpy2
from Pyro4 import expose
from random import randint
import random

class Solver:
	def __init__(self, workers=None, input_file_name=None, output_file_name=None):
		self.input_file_name = input_file_name
		self.output_file_name = output_file_name
		self.workers = workers
		print("Inited")

	def solve(self):
		print("Job Started")
		print("Workers %d" % len(self.workers))

		arr = self.read_input()
		step = int(len(arr) / len(self.workers))
		# map
		mapped = []
		for i in xrange(0, len(self.workers)):
			mapped.append(self.workers[i].mymap(([str(i) for i in arr[i*step:i*step+step]])))
		self.write_output(mapped)

	@staticmethod
	@expose
	def mymap(a):
		primes = []
		for el in a:
			line = str(el) + " ="
			prime = Solver.pollard_rho(int(el))
			line += " " + str(prime)
			b = int(el)/prime
			if Solver.is_probably_prime(int(b)):
				line += " * " + str(b)
			while(not(Solver.is_probably_prime(int(b))) and (int(b) > 1)):
			 	prime = Solver.pollard_rho(int(b))
			 	line += " * " + str(prime)
			primes.append(line)
		return primes


	def read_input(self):
		f = open(self.input_file_name, 'r')
		lines = [int(line.rstrip('\n')) for line in f]
		f.close()
		return lines

	def write_output(self, output):
		f = open(self.output_file_name, 'w')
		for a in output:
			for i in a.value: f.write(str(i) + '\n')
		#f.write(str(output))
		f.close()
		print("output done")

	@staticmethod
	@expose
	def gcd(a, b):
		while b:
			a, b = b, a % b
		return a

	@staticmethod
	@expose
	def pollard_rho(n):
		s = 2
		f = lambda x, m: (x**2 + 2) % m
		x = y = s
		d = 1
		while d == 1:
			x = f(x, n)
			y = f(f(y, n), n)
			d = Solver.gcd(abs(y - x), n)
		return d

	@staticmethod
	@expose
	def is_probably_prime(n):
		k = 5
		if (n < 2 ):
			return False
		output = True
		for i in range(0, k):
			a = randint(1, n-1)
			if (pow(a, n-1, n) != 1):
				return False 
		return output
