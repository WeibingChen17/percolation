import random
from math import sqrt
import matplotlib.pyplot as plt

class SquareCells:
    def __init__(self, n, prob):
        self.cells = [['-' if random.random() > prob else '*' for _ in range(n)] for __ in range(n)]

    def __repr__(self):
        return '\n'.join([''.join(line) for line in cells])

    def fromSring(string):
        self.cells = [list(line) for line in string.strip().split('\n')]
        
    def neighborhood(self, cells, i, j):
        n = len(self.cells)
        return [(i+di, j+dj) for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1))
            if 0<=i+di<n and 0<=j+dj<n and cells[i+di][j+dj]=='*']

    def isPercolated(self):
        n = len(self.cells)
        level = set([(0, i) for i in range(n) if self.cells[0][i] == '*'])
        visit = level

        while level:
            nextlevel = []
            for (i, j) in level:
                if i == n-1:
                    return True
                nextlevel.extend([(ni, nj) for ni, nj in self.neighborhood(self.cells, i, j) if (ni, nj) not in visit])
            level = set(nextlevel[:])
            visit.update(level)

        return False


class Percolation:
    def __init__(self):
        self.n = 0
        self.samplingNumber = 0
        self.samplingPoint = []
        self.results = {'mean':[], 'std':[]}

    def setSamplingPoint(self, samplingPoint):
        self.samplingPoint = samplingPoint[:]

    def setSamplingNumber(self, samplingNumber):
        self.samplingNumber = samplingNumber;

    def setSize(self, n):
        self.n = n

    def run(self):
        for sp in self.samplingPoint:
            print('Eveluating point ', sp)
            perc = [1 if SquareCells(self.n, sp).isPercolated() else 0 for _ in range(self.samplingNumber)]
            count = sum(perc)
            mean = count/self.samplingNumber
            std = sqrt(count/(self.samplingNumber - 1) * (1 - mean))
            self.results['mean'].append(mean)
            self.results['std'].append(std)

    def visualize(self):
        #plt.errorbar(self.samplingPoint, self.results['mean'], self.results['std'], linestyle='--', marker='+')
        plt.xlabel('Prob (Cell on)')
        plt.ylabel('Prob (Grid on)')
        plt.plot(self.samplingPoint, self.results['mean'], linestyle='--', marker='^')
        plt.show()

if __name__ == '__main__':
    p = Percolation()
    p.setSize(30)
    p.setSamplingNumber(500)
    samplingPoint = [0.1, 0.2, 0.3, 0.4, 0.45] + [0.01 * _ for _  in range(46, 70)] + [0.7, 0.8, 0.9]
    p.setSamplingPoint(samplingPoint)
    p.run()
    p.visualize()
