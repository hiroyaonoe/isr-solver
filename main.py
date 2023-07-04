import argparse
from typing import Set, Tuple
import numpy as np

def main():
	col, dat = parse_args()
	graph = read_col(col)
	start, end = read_dat(dat)
	setup(graph, start)
	print(graph)
	print(end)
	solve(graph, end)
	

def parse_args() -> Tuple[str, str]:
	p = argparse.ArgumentParser()
	p.add_argument('col', help='col file path')
	p.add_argument('dat', help='dat file path')
	args = p.parse_args()
	return args.col, args.dat


def read_col(name: str) -> np.ndarray:
	graph = np.empty(0)
	f = open(name, 'r')
	lines = f.readlines()
	for line in lines:
		ls = line.split()
		op = ls[0]
		one = int(ls[1])
		two = int(ls[2])
		if op == 'p':
			graph = np.zeros([one+1, one+1])
		elif op == 'e':
			graph[one, two] = 1
			graph[two, one] = 1
	return graph

def read_dat(name: str) -> Tuple[Set, Set]:
	start = []
	end = []
	f = open(name, 'r')
	lines = f.readlines()
	for line in lines:
		ls = line.split()
		op = ls[0]
		es = set(map(int, ls[1:]))
		if op == 's':
			start = es
		elif op == 't':
			end = es
	return start, end

def setup(graph: np.ndarray, start: Set):
	for e in start:
		graph[0, e] = -1
		graph[e, 0] = -1
		graph[1:, e] *= 2
		graph[e, 1:] *= 2

def solve(graph: np.ndarray, end: Set) -> Tuple:
	if distance(graph, end) == 0:
		return [get_is[graph]]
	
	for l in graph[1:]:
		cnt_one = l.count(1)
		if cnt_one == 0:
			continue
		cnt_two = l.count(2)
		if cnt_two == 1:
			target = l.index(2)


def get_is(graph: np.ndarray) -> Set:
	s = set()
	for i, l in enumerate(graph[0]):
		if l != 0:
			s.add(i)
	return s

def distance(graph: np.ndarray, e: Set) -> int:
	s = get_is(graph)
	diff = s - e
	return len(diff)

if __name__ == "__main__":
	main()
