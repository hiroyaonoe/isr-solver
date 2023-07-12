import sys
import argparse
from typing import Set, List, Tuple
import numpy as np

sys.setrecursionlimit(20000000)

REV_LIMIT = 0
DIST_LIMIT = 1<<32

def main():
	col, dat = parse_args()
	graph = read_col(col)
	start, end = read_dat(dat)
	memo = setup(graph, start)
	print(graph)
	print("s:", start)
	print("t:", end)
	ans = solve(graph, end, 0, memo)
	if len(ans) == 0:
		print("NO")
	else:
		print("YES")
		for i in range(len(ans)):
			print(i+1, ":", ans[-i])

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
		if op not in ('p', 'e'):
			continue
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

def setup(graph: np.ndarray, start: Set) -> np.ndarray:
	for i in start:
		put(graph, i)
	memo = graph.copy()
	memo[:, :] = 0
	return memo

def solve(graph: np.ndarray, end: Set, limit: int, memo: np.ndarray) -> List:
	if limit > DIST_LIMIT:
		return []
	dist = distance(graph, end)
	if dist == 0:
		ret = [get_ids(graph)]
		return ret
	
	for j, l in enumerate(graph[1:]):
		two_index = np.where(l == 2)[0]
		if len(two_index) == 0:
			ids = get_ids(graph)
			for i in ids:
				ret = move_and_solve(graph, i, j+1, end, dist, limit, memo)
				if len(ret) > 0:
					ret.append(get_ids(graph))
					return ret

		if len(two_index) == 1:
			i = two_index[0]
			ret = move_and_solve(graph, i, j+1, end, dist, limit, memo)
			if len(ret) > 0:
				ret.append(get_ids(graph))
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

def move_and_solve(graph: np.ndarray, i: int, j: int, end: Set, dist: int, limit: int, memo: np.ndarray) -> List:
	if memo[i, j] > REV_LIMIT:
		return []
	new_memo = memo.copy()
	new_memo[i, j] = +2
	new_memo[j, i] = +1
	new_graph = graph.copy()
	move(new_graph, i, j)
	if distance(new_graph, end) < dist:
		return solve(new_graph, end, limit, new_memo)
	if distance(new_graph, end) == dist:
		return solve(new_graph, end, limit+1, new_memo)
	if distance(new_graph, end) > dist:
		return solve(new_graph, end, limit+2, new_memo)
	return []

if __name__ == "__main__":
	main()
