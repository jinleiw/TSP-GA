import sys
import random

class Ga(object):

	'''
		scale:
		max_gen:
		Pc:
		Pm:
	'''
	def __init__(self, file_name, scale, max_gen, Pc, Pm):
		self.file_name = file_name
		self.scale = scale
		self.max_gen = max_gen
		self.Pc = Pc
		self.Pm = Pm

		self.cityNum = 9847
		self.distance = [[0 for i in range(self.cityNum)] for i in range(self.cityNum)]
		
		self.currentT = 0
		self.bestT = 0
		self.bestLength = sys.maxint
		self.bestTour = [0 for i in range(self.cityNum)]

		self.oldPopulation = [[0 for i in range(self.cityNum)] for i in range(scale)]
		self.newPopulation = [[0 for i in range(self.cityNum)] for i in range(scale)]
		self.fitness = [0 for i in range(scale)]
		self.Pi = [0 for i in range(scale)]
		#self.age = 1

		self.subCity = 100

		self.adjust = 100

		self.coordinates = []

		self.result = open('/home/rui/Documents/calcIntelligence/result.txt', 'wr')
		#print "init..."

	def calcDis(self):
		input = open(self.file_name, "r")
		for line in input.readlines():
			l = line.split(' ')
			x = float(l[1])
			y = float(l[2])
			self.coordinates.append((x, y))

		for i in range(self.cityNum):
			self.distance[i][i] = 0

		for i in range(self.cityNum - 1):
			
			x1 = self.coordinates[i][0]
			y1 = self.coordinates[i][1]
			
			for j in range(i+1, self.cityNum):
				
				x2 = self.coordinates[j][0]
				y2 = self.coordinates[j][1]
				d = (((x1 - x2) ** 2) + ((y1 - y2) ** 2)) ** 0.5
				self.distance[i][j] = d
				self.distance[j][i] = d

		#print self.distance
		print "calcDis..."

	# section init
	def initGSec(self):
		for i in range(self.scale):
			#oldPopulation[i][0] = random.randint(0, self.cityNum - 1)
			for j in range(0, self.cityNum, self.subCity):
				# subCity
				if (j + self.subCity <= self.cityNum):
					self.oldPopulation[i][j] = random.randint(j, j + self.subCity - 1)
					k = j + 1
					while (k < j + self.subCity):
						self.oldPopulation[i][k] = random.randint(j, j + self.subCity - 1)
						t = j
						while (t < k):
							if self.oldPopulation[i][t] == self.oldPopulation[i][k]:
								break
							t = t + 1
						if t == k:
							k = k + 1
				# < subCity
				else:
					self.oldPopulation[i][j] = random.randint(j, self.cityNum - 1)
					k = j + 1
					while (k < self.cityNum):
						self.oldPopulation[i][k] = random.randint(j, self.cityNum - 1)
						t = j
						while (t < k):
							if self.oldPopulation[i][t] == self.oldPopulation[i][k]:
								break
							t = t + 1
						if t == k:
							k = k + 1

		print "initG..."
		for i in range(self.scale):
			#print self.oldPopulation[i]
			pass

	# simple init
	def initG(self):
		pass

	# calsc fitness
	def calcFitness(self, k):
		len = 0
		for i in range(self.cityNum - 1):
			len = len + self.distance[self.oldPopulation[k][i]][self.oldPopulation[k][i+1]]
		len = len + self.distance[self.oldPopulation[k][self.cityNum-1]][self.oldPopulation[k][0]]
		self.fitness[k] = len

		#print "fitness..."
		#print self.fitness

	# calc Pi
	def calcPi(self):
		tmpf = [0 for i in range(self.scale)]
		for i in range(self.scale):
			tmpf[i] = self.adjust / self.fitness[i]

		sumFitness = sum(tmpf)

		self.Pi[0] = tmpf[0] / sumFitness

		for i in range(1, self.scale):
			self.Pi[i] = tmpf[i] / sumFitness + self.Pi[i-1]
		
		#print "calcPi..."
		'''
		print "fitness", self.fitness
		print "Pi", self.Pi
		'''
		self.result.write(str(self.fitness) + '\n')
		self.result.write(str(self.Pi) + '\n')
		self.result.write('\n')

	def copy2old(self):
		for i in range(self.scale):
			for j in range(self.cityNum):
				# todo new --> old
				self.oldPopulation[i][j] = self.newPopulation[i][j]
		self.currentT = self.currentT + 1
		
		# todo del
		'''
		for i in range(self.scale):
			print self.oldPopulation[i]
		'''

	def copy1(self, k_old, k_new):
		for i in range(self.cityNum):
			self.newPopulation[k_new][i] = self.oldPopulation[k_old][i]

	def selectBest(self):
		index = 0
		for i in range(1, self.scale):
			if self.fitness[i] < self.fitness[index]:
				index = i
		self.copy1(index, 0)

	def select(self):
		for i in range(1, self.scale):
			r = random.random()
			j = 0
			while j < self.scale:
				if r <= self.Pi[j]:
					break
				j = j + 1
			self.copy1(j, i)

	def crossover(self):

		for i in range(0, self.scale, 2):

			r = random.random()
			if r < self.Pc:

				print "crossover..." , i
				print self.newPopulation[i]
				print self.newPopulation[i+1]
				
				r1 = random.randint(0, self.cityNum - 1)
				r2 = random.randint(0, self.cityNum - 1)
				while r1 == r2:
					r2 = random.randint(0, self.cityNum - 1)

				if r1 > r2:
					r1 = r1 + r2
					r2 = r1 - r2
					r1 = r1 - r2
		
				print "r1", r1
				print "r2", r2
		
				g1 = [0 for x in range(self.cityNum)]
				g2 = [0 for x in range(self.cityNum)]

				index1 = 0
				index2 = r2
				while index2 < self.cityNum:
					#print "index2", index2
					g2[index1] = self.newPopulation[i][index2]
					index1 = index1 + 1
					index2 = index2 + 1
				print 'g2', g2

				for j in range(self.cityNum):
					t = 0
					for k in range(self.cityNum - r2):
						#print "k", k, "j", j
						if g2[k] == self.newPopulation[i+1][j]:
							t = 1
							break
					#print "t", t
					if t == 0:
						#print "index1", index1, "i + 1", i + 1, "j", j
						g2[index1] = self.newPopulation[i+1][j]
						index1 = index1 + 1
				print 'g2', g2

				s = 0
				for j in range(self.cityNum):
					t = 0
					for k in range(r1):
						if self.newPopulation[i][j] == self.newPopulation[i+1][k]:
							t = 1
							break
					if t == 0:
						g1[s] = self.newPopulation[i][j]
						s = s + 1
				
				print 'g1', g1

				for j in range(r1):
					g1[s] = self.newPopulation[i+1][j]
					s = s + 1

				print 'g1', g1

				for j in range(self.cityNum):
					self.newPopulation[i][j] = g1[j]
					self.newPopulation[i+1][j] = g2[j]

				print 'crossover end...', i
				print self.newPopulation[i]
				print self.newPopulation[i+1]

			else:
				r = random.random()
				print "variation...r...", r
				if r < self.Pm:
					print "variation...", self.newPopulation[i]
					self.variation(i)
					print "variation end...", self.newPopulation[i]
				r = random.random()
				if r < self.Pm:
					print "variation...", self.newPopulation[i+1]
					self.variation(i+1)
					print "variation end...", self.newPopulation[i+1]

	def variation(self, k):

		# times of variation
		count = random.randint(0, self.cityNum)

		for i in range(count):
			r1 = random.randint(0, self.cityNum - 1)
			r2 = random.randint(0, self.cityNum - 1)
			while r1 == r2:
				r2 = random.randint(0, self.cityNum - 1)

			self.newPopulation[k][r1] = self.newPopulation[k][r1] + self.newPopulation[k][r2]
			self.newPopulation[k][r2] = self.newPopulation[k][r1] - self.newPopulation[k][r2]
			self.newPopulation[k][r1] = self.newPopulation[k][r1] - self.newPopulation[k][r2]

	def evolution(self):
		self.selectBest()
		self.select()
		
		self.crossover()
		#self.variation()

	# record best Tour, best Length, best Time
	def recordBest(self):
		preBestLength = self.bestLength
		index = 0
		for i in range(self.scale):
			if self.fitness[i] < self.bestLength:
				self.bestLength = self.fitness[i]
				index = i

		if self.bestLength < preBestLength:
			for i in range(self.cityNum):
				self.bestTour[i] = self.oldPopulation[index][i]
			self.bestT = self.currentT

	def solve(self):
		self.calcDis()
		self.initGSec()
		
		'''
		print "----init G----" # put into file
		for i in range(self.scale):
			print self.oldPopulation[i]
		'''

		self.result.write("----init G----\n")
		for i in range(self.scale):
			self.result.write(str(self.oldPopulation[i]) + '\n')

		for i in range(self.scale):
			self.calcFitness(i)
		self.calcPi()
		self.recordBest()

		for i in range(self.max_gen):
			self.evolution() # todo
			self.copy2old()
			for j in range(self.scale):
				self.calcFitness(j)
			self.calcPi()
			self.recordBest()

		# put into file
		'''
		print "----last G----"
		for i in range(self.scale):
			print self.oldPopulation[i]
		'''

		self.result.write("----last G----\n")
		for i in range(self.scale):
			self.result.write(str(self.oldPopulation[i]) + '\n')
		
		'''
		print "---best Time---"
		print self.bestT
		
		print "---best Length---"
		print self.bestLength

		print "---best Tour---"
		print self.bestTour
		'''
	
		self.result.write("\n\n---best Time---\n" + str(self.bestT))
		self.result.write("\n\n---best Length---\n" + str(self.bestLength))
		self.result.write("\n\n---best Tour---\n" + str(self.bestTour))
		self.result.close()
		#print "solve..."



if __name__ == "__main__":
	g = Ga("/home/rui/Documents/calcIntelligence/japan9847.tsp", 100, 100, 0.8, 0.6)
	g.solve()