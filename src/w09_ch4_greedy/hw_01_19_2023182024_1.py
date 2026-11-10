"""그래프 실습: blank(1)~blank(30)를 식 또는 조건으로 바꾸어 완성한다."""

import random

from heapdict import heapdict

RANDOM_SEED = "a01"

def blank(number):
    """각 호출 부분을 채운다. 이 함수 자체는 수정하지 않는다."""
    raise NotImplementedError(f"빈칸 {number:02d}을 채우세요.")


class EdgeList:
    """무방향 간선의 방향과 출력 순서를 통일하는 결과 목록."""
    def __init__(self):
        self.graph=[]
    def append(self,vertex_from,vertex_to,weight):
        if vertex_from>vertex_to:
            vertex_from,vertex_to=vertex_to, vertex_from
        self.graph.append((weight, vertex_from,vertex_to))
        self.graph.sort()
    def __repr__(self):
        return str(self.graph)
    def __eq__(self,other):
        return self.graph==other.graph
    pass

def find_root(parents, vertex):
    """대표를 반환하고, 돌아오면서 경로 압축을 기록한다."""
    # 자기 자신이 부모인 정점이 이 집합의 대표입니다.
    if parents[vertex]==vertex:
        return vertex
    # 바로 위 부모가 아니라 그 부모를 따라간 최종 대표를 구합니다.
    root = find_root(parents, parents[vertex])
    # 리턴하면서 바로 최종 대표를 가리키도록 바꿉니다.
    parents[vertex] = root
    return root


def kruskal(count, edges):
    """연결된 무방향 그래프의 (EdgeList, 총비용)을 반환한다."""
    # 정점 번호는 0부터 count-1까지입니다. 처음에는 모두 독립된 집합입니다.
    parents = [vertex for vertex in range(count)]
    mst = EdgeList()
    total_cost = 0
    # 입력 edges를 직접 정렬하지 않고 새 목록을 만듭니다.
    ordered = sorted(edges, key=lambda edge: edge[2])
    for u, v, weight in ordered:
        root_u = find_root(parents, u)
        root_v = find_root(parents, v)
        # 이미 같은 집합이면 이 간선을 추가할 때 사이클이 생깁니다.
        if root_u==root_v:
            continue
        # append에는 목록 하나가 아니라 세 인자를 따로 전달합니다.
        mst.append(u, v, weight)
        total_cost += weight
        # 대표끼리 합칩니다. 작은 번호의 대표를 남기는 규칙을 사용합니다.
        if root_u < root_v:
            parents[root_v] = parents[root_u]
        else:
            parents[root_u] = parents[root_v]
        # 검사한 간선 수가 아니라 실제 선택한 간선 수로 판단합니다.
        if len(mst.graph) == count-1:
            break
    return mst, total_cost


def make_neighbors(count, edges):
    """각 정점의 이웃과 가중치를 딕셔너리로 만든다."""
    graph = {vertex: {} for vertex in range(count)}
    for u, v, weight in edges:
        # 무방향 간선이므로 양쪽에서 서로를 이웃으로 조회할 수 있어야 합니다.
        graph[u][v] = weight
        graph[v][u] = weight
    return graph


def prim(count, edges, start=0):
    """연결된 무방향 그래프의 (EdgeList, 총비용)을 반환한다."""
    graph = make_neighbors(count, edges)
    completed = set()
    mst = EdgeList()
    total_cost = 0
    # weights[도착 정점] = [연결할 간선의 비용, 출발 정점]
    # heapdict는 value가 최소인 항목을 꺼냅니다. 일반 dict와 구별합니다.
    weights = heapdict()
    # 시작점은 실제 연결 간선 없이 출발합니다. 비용 0, 출발점은 자기 자신입니다.
    weights[start] = [0,start]
    while weights:
        # (key, value)를 받아 정점과 [비용, 출발점]으로 나누어 받습니다.
        vertex, (cost, origin) = weights.popitem()
        completed.add(vertex)
        # 시작점의 가짜 연결은 MST의 간선에 포함하지 않습니다.
        if vertex!=origin:
            mst.append(origin, vertex, cost)
            total_cost += cost
        for neighbor, edge_cost in graph[vertex].items():
            # 이미 트리에 들어간 정점은 후보로 다시 넣지 않습니다.
            if neighbor in completed:
                continue
            # 시작점부터의 누적 거리가 아니라 연결할 간선 하나의 비용입니다.
            candidate_cost = edge_cost
            old_candidate = weights.get(neighbor)
            # 없던 정점은 추가하고, 있던 정점은 더 싸게 연결할 수 있을 때 갱신합니다.
            # or의 단축 평가 덕분에 None일 때 old_candidate[0]을 읽지 않습니다.
            if old_candidate is None or (candidate_cost<old_candidate[0]):
                # 새 value를 대입해야 heapdict가 힙의 위치도 조정합니다.
                weights[neighbor] = [candidate_cost,vertex]
    return mst, total_cost


def dijkstra(count, edges, start=0):
    """시작점에서 각 정점까지의 (최단 거리 배열, 이전 정점 배열)을 반환한다."""
    # Dijkstra는 가중치가 0 이상인 그래프에서 사용합니다.
    # 이웃 정보는 Prim과 같은 함수를 호출하여 준비합니다.
    graph = make_neighbors(count, edges)
    completed = set()
    distances = [float("inf")] * count
    previous = [None] * count
    # Prim과 같은 후보 형식이지만 비용의 의미가 다릅니다.
    # weights[도착 정점] = [시작점부터의 누적 거리, 이전 정점]
    weights = heapdict()
    weights[start] = [0,start]
    while weights:
        vertex, (cost, origin) = weights.popitem()
        # 음수가 아닌 가중치에서는 최소 누적 비용 후보를 꺼낼 때 거리를 확정합니다.
        completed.add(vertex)
        distances[vertex] = cost
        if vertex != origin:
            # 시작점은 이전 정점이 없으므로 None을 그대로 유지합니다.
            previous[vertex] = origin
        for neighbor, edge_cost in graph[vertex].items():
            if neighbor in completed:
                continue
            # Prim과 비교할 핵심: 현재 정점까지의 누적 거리도 필요합니다.
            candidate_cost = cost + edge_cost
            old_candidate = weights.get(neighbor)
            if old_candidate is None or [candidate_cost<old_candidate[0]]:
                weights[neighbor] = [candidate_cost,vertex]
    # 도달하지 못한 정점은 거리 inf, 이전 정점 None으로 남습니다.
    return distances, previous


def restore_path(distances, previous, destination):
    """이전 정점을 역추적하여 시작점부터 목적지까지의 정점 번호 목록을 만든다."""
    if distances[destination] == float("inf"):
        return []
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path


# 각 데이터는 연결된 단순 무방향 그래프이며, 간선 가중치는 모두 다릅니다.
# MST가 유일하므로 시작점이나 입력 방향이 달라도 같은 간선 집합을 얻습니다.
# 입력 간선은 가중치순으로 정렬되어 있지 않고, 큰 번호가 먼저인 간선도 있습니다.
DATASETS = [
    ("정점 7개: 사이클을 만드는 간선 제외", 7, [
        [3, 1, 11], [4, 6, 15], [2, 0, 7], [5, 3, 6],
        [1, 0, 4], [6, 5, 3], [2, 3, 9], [4, 2, 2],
        [1, 2, 5], [5, 4, 8], [3, 4, 10], [6, 2, 13],
    ]),
    ("정점 8개: 기존 후보를 더 싼 간선으로 갱신", 8, [
        [0, 4, 25], [7, 5, 9], [2, 0, 17], [1, 0, 20],
        [3, 2, 4], [4, 1, 6], [5, 2, 12], [6, 3, 7],
        [7, 6, 2], [2, 1, 3], [5, 4, 5], [6, 5, 11],
        [7, 4, 18], [3, 1, 14], [6, 4, 16], [7, 0, 30],
    ]),
    ("정점 1개: 선택할 간선 없음", 1, []),
]


if __name__ == "__main__":
    randomizer = random.Random(RANDOM_SEED)
    for title, count, edges in DATASETS:
        print(f"\n[{title}]")
        print("입력 간선:", edges)
        kruskal_mst, kruskal_cost = kruskal(count, edges)
        print("Kruskal:", kruskal_mst, "총비용:", kruskal_cost)
        # 난수 생성기는 한 번만 만들고 데이터마다 다음 난수를 사용합니다.
        # 시작점이 달라도 유일한 MST의 간선 집합은 같아야 합니다.
        start = randomizer.randrange(count)
        prim_mst, prim_cost = prim(count, edges, start)
        print(f"Prim(start={start}):", prim_mst, "총비용:", prim_cost)
        # == 연산자가 EdgeList.__eq__를 호출하여 간선 목록을 비교합니다.
        same_mst = kruskal_mst == prim_mst
        same_cost = kruskal_cost == prim_cost
        print("간선 목록 동일 (==):", same_mst)
        print("총비용 동일 (==):", same_cost)
        assert isinstance(kruskal_mst, EdgeList) and isinstance(prim_mst, EdgeList)
        assert len(kruskal_mst.graph) == len(prim_mst.graph) == count - 1
        assert same_mst, "선택한 간선 목록이 다릅니다."
        assert same_cost, "총비용이 다릅니다."
        assert kruskal_cost == sum(w for w, _, _ in kruskal_mst.graph)
        print("두 알고리즘의 간선 목록과 총비용 일치")

        # 시작점을 새로 뽑지 않고 Prim과 같은 시작점으로 최단 경로를 구합니다.
        distances, previous = dijkstra(count, edges, start)
        print(f"Dijkstra(start={start}):", distances)
        graph = make_neighbors(count, edges)
        assert distances[start] == 0 and previous[start] is None
        for destination in range(count):
            path = restore_path(distances, previous, destination)
            print(f"  #{destination}: 거리 {distances[destination]}, 경로 {path}")
            if distances[destination] == float("inf"):
                assert path == []
            else:
                assert path[0] == start and path[-1] == destination
                assert len(path) == len(set(path)), "경로에 사이클이 있습니다."
                assert sum(graph[u][v] for u, v in zip(path, path[1:])) == distances[destination]
        # MST의 비용과 최단 거리들은 서로 다른 값을 뜻하므로 같다고 비교하지 않습니다.
