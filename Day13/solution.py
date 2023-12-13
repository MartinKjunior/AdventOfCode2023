#personal setup
import os
from icecream import ic

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
#solution
with open('mirrors.txt') as f:
    data = f.read().splitlines()

class Valley:
    def __init__(self, l):
        self.valley = l
        self.patterns = self.split_valley()
        self.reflection_found = False
        self.summary = []
    
    def print_valley(self):
        for row in self.valley:
            print(row)
    
    def print_patterns(self):
        for pattern in self.patterns:
            for row in pattern:
                print(row)
            print()
    
    def split_valley(self):
        #split input into a list of patterns
        split_valley = []
        temp = []
        for row in self.valley:
            if not row:
                split_valley.append(temp)
                temp = []
            else:
                temp.append(row)
        split_valley.append(temp)
        return split_valley
    
    @staticmethod
    def get_col(arr, col):
        return ''.join([row[col] for row in arr])
    
    @staticmethod
    def get_row(arr, row):
        return arr[row]
    
    @staticmethod
    def size(arr):
        # height, width
        return len(arr), len(arr[0])
    
    def check_rows_cols(self, pattern):
        #checks rows then columns for reflections
        self.reflection_found = False
        for fun, length in zip((self.get_row, self.get_col), self.size(pattern)):
            seen = [fun(pattern, 0)]
            for i in range(1, length):
                seen.append(fun(pattern, i))
                if seen[i - 1] == seen[i]:
                    #if found, find length of reflection
                    ref_length = self.verify_reflection(pattern, i - 1, seen[:-1], length, fun)
                    if self.reflection_found and ref_length:
                        self.get_result(fun, ref_length)
                        break
    
    def get_result(self, fun, n):
        if fun.__name__ == 'get_row':
            n *= 100
        self.summary.append(n)
    
    def verify_reflection(self, pattern, i, seen, length, fun):
        #reflection is invalid if it ends before the edge
        size = 1
        start = i + 1
        if i == 0:
            self.reflection_found = True
            return size
        if i == length - 2:
            self.reflection_found = True
            return start
        j = i + 2 #forward
        i -= 1 #backward
        while i >= 0 and j < length:
            if seen[i] != fun(pattern, j):
                return None
            size += 1
            i -= 1
            j += 1
        self.reflection_found = True
        if start > length / 2:
            size = start
        return size
    
    def solve(self):
        for pattern in self.patterns:
            self.check_rows_cols(pattern)
        ic(sum(self.summary))

V = Valley(data)
V.solve()