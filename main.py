import argparse
from typing import Set, Tuple
import numpy as np

LIMIT = 5

def main():
	col, dat = parse_args()
	graph = read_col(col)
	start, end = read_dat(dat)
	setup(graph, start)
	print(graph)
	print(end)
	ans = solve(graph, end, 0)
	print(ans)

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
	for i in start:
		put(graph, i)

def solve(graph: np.ndarray, end: Set, limit: int) -> Tuple:
	if limit > LIMIT:
		print("-2: ", graph, [])
		return []
	dist = distance(graph, end)
	if dist == 0:
		ret = [get_ids(graph)]
		print("-1: ", graph, ret)
		return ret
	
	for j, l in enumerate(graph[1:]):
		two_index = np.where(l == 2)[0]
		if len(two_index) == 0:
			ids = get_ids(graph)
			for i in ids:
				ret = move_and_solve(graph, i, j+1, end, dist, limit)
				if len(ret) > 0:
					print("0: ", graph, ret)
					return ret

		if len(two_index) == 1:
			i = two_index[0]
			ret = move_and_solve(graph, i, j+1, end, dist, limit)
			if len(ret) > 0:
				print("1: ", graph, ret)
				return ret

	return []


def get_ids(graph: np.ndarray) -> Set:
	s = set()
	for i, l in enumerate(graph[0]):
		if l != 0:
			s.add(i)
	return s

def distance(graph: np.ndarray, e: Set) -> int:
	s = get_ids(graph)
	diff = s - e
	return len(diff)

def put(graph: np.ndarray, i: int):
	graph[0, i] = -1
	graph[i, 0] = -1
	graph[1:, i] *= 2
	graph[i, 1:] *= 2

def remove(graph: np.ndarray, i: int):
	graph[0, i] = 0
	graph[i, 0] = 0
	graph[1:, i] //= 2
	graph[i, 1:] //= 2

def move(graph: np.ndarray, i: int, j: int) -> np.ndarray:
	remove(graph, i)
	put(graph, j)

def move_and_solve(graph: np.ndarray, i: int, j: int, end: Set, dist: int, limit: int) -> Tuple:
	new_graph = graph.copy()
	move(new_graph, i, j)
	if distance(new_graph, end) < dist:
		return solve(new_graph, end, limit)
	if distance(new_graph, end) == dist:
		return solve(new_graph, end, limit+1)
	if distance(new_graph, end) > dist:
		return solve(new_graph, end, limit+2)
	return []

if __name__ == "__main__":
	main()
