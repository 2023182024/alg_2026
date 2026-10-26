"""Prim의 최소 신장 트리 구현을 위한 실행 구조를 준비한다."""

from heapdict import heapdict

import pyvisalgo as va


def build_graph(count, edges):
    """무방향 간선 목록을 정점별 이웃과 가중치의 딕셔너리로 바꾼다."""
    # graph[u]는 u의 이웃을 key로, 연결 간선의 가중치를 value로 갖습니다.
    # 간선이 없는 정점도 빈 딕셔너리를 가지며, 정점 번호는 0부터 count-1입니다.
    graph = {u: {} for u in range(count)}
    for u, v, weight in edges:
        # 무방향 간선 하나를 양쪽 정점의 이웃 정보에 모두 등록합니다.
        graph[u][v] = weight
        graph[v][u] = weight
    return graph


def prim(count, edges, start=0):
    """정점 수, 무방향 간선 목록, 시작 정점을 받아 최소 신장 트리를 구성한다."""
    # Prim은 정점 하나를 확정할 때마다 그 정점에 연결된 이웃들을 검사합니다.
    # 전체 간선 목록 대신 graph[vertex].items()로 이웃과 가중치를 얻도록 준비합니다.
    graph = build_graph(count, edges)
    # 내륙은 최소 연결 비용을 확정하여 트리에 포함시킨 정점들의 집합입니다.
    # 같은 정점을 다시 확정하거나 후보로 추가하지 않도록 소속 여부를 검사합니다.
    completed = set()
    # 선택한 간선은 (출발 정점, 도착 정점, 가중치)로 기록합니다.
    # 내륙 정점의 집합과 실제 선택한 간선의 목록은 서로 다른 정보입니다.
    mst = []
    total_cost = 0  # 선택한 간선들의 가중치 합이며, 아직 선택한 간선은 없습니다.
    # 이전 heapq: weights = [[weight, vertex_to, vertex_from], ...]
    # 현재 heapdict: weights[vertex_to] = [weight, vertex_from]
    # 딕셔너리처럼 정점 번호를 key로 등록·조회하면서 value가 최소인 후보를 꺼냅니다.
    # value의 첫 항목인 비용부터 비교하고, 같으면 다음 항목인 출발점을 비교합니다.
    # value 전체가 같을 때 정점 번호나 등록 순서에 따른 추출 순서는 가정하지 않습니다.
    # 현재 후보 수 k에 대해 key 조회는 평균 O(1), 등록·갱신·최소 추출은 O(log k)입니다.
    # 같은 key에 새 value를 대입하면 해당 후보를 교체하고 힙의 위치도 조정합니다.
    # weights[vertex][0]을 직접 수정하면 이 조정이 일어나지 않으므로 피해야 합니다.
    # Prim의 비용은 시작점부터의 누적 거리가 아니라 연결할 간선 하나의 비용입니다.
    weights = heapdict()
    # 시작점은 연결 간선 없이 출발하므로 비용 0, 출발점은 자기 자신으로 둡니다.
    # 이 항목은 실제 간선이 아니며, 시작점은 아직 내륙으로 확정하지 않았습니다.
    weights[start] = [0, start]
    vis.add_candidate(start, 0, start, weights, starting=True)
    # 후보가 남아 있는 동안 가장 저렴하게 연결할 수 있는 정점을 하나씩 꺼냅니다.
    while weights:
        if vis.stopped():
            break
        # popitem()은 최소 value를 가진 (key, value)를 반환하면서 후보를 제거합니다.
        # 일반 dict.popitem()의 마지막 등록 항목 추출과는 의미가 다릅니다.
        # key는 정점 번호, value는 [비용, 출발점]이므로 두 단계로 풀어 받습니다.
        vertex, (cost, origin) = weights.popitem()
        # 가장 저렴한 후보를 꺼내면 곧바로 내륙으로 확정합니다.
        completed.add(vertex)
        # 정점이 확정되면 할 일:
        # 1. 이 정점을 연결한 간선이 있다면 MST에 추가하고 비용을 합산합니다.
        #    시작점은 연결 간선 없이 출발했으므로 추가할 간선이 없습니다.
        # 2. 주위 정점들에 대하여 다음을 수행합니다.
        #    - 이미 내륙인 정점이면 무시합니다.
        #    - 후보에 없는 정점이면 연결 비용과 출발점을 기록하여 새로 등록합니다.
        #    - 기존 후보보다 더 짧게 연결할 수 있으면 비용과 출발점을 갱신합니다.
        #    - 기존 후보와 같거나 더 비싼 연결이면 기존 후보를 유지합니다.
        # 시작점의 비용 0은 실제 간선이 아니므로 간선 목록과 비용 합에서 제외합니다.
        if vertex != origin:
            mst.append((origin, vertex, cost))
            total_cost += cost
        vis.take_candidate(vertex, cost, origin, weights, total_cost)
        vis.show_neighbors(vertex, graph[vertex])
        # graph[vertex]의 key는 이웃 정점, value는 두 정점을 잇는 간선의 가중치입니다.
        # items()로 두 값을 함께 받아 현재 내륙에 연결할 수 있는 이웃들을 검사합니다.
        for neighbor, edge_cost in graph[vertex].items():
            if vis.stopped():
                break
            vis.inspect_edge(vertex, neighbor, edge_cost)
            # 이미 트리에 포함된 정점은 후보로 다시 등록하지 않습니다.
            # 이 간선을 추가하면 내륙의 두 정점을 잇게 되어 사이클이 생깁니다.
            if neighbor in completed:
                vis.ignore_inland(vertex, neighbor)
                continue
            # Prim은 현재 내륙에서 이웃으로 가는 간선 하나의 비용을 비교합니다.
            # 시작점부터의 누적 거리를 구하는 것이 아니므로 cost를 더하지 않습니다.
            candidate_cost = edge_cost
            if neighbor not in weights:
                # 처음 발견한 이웃은 비용과 연결 출발점을 함께 후보로 등록합니다.
                # 아직 내륙은 아니며, 이후 최소 후보로 꺼냈을 때 확정됩니다.
                weights[neighbor] = [candidate_cost, vertex]
                vis.add_candidate(neighbor, candidate_cost, vertex, weights)
            # 다음 단계에서 기존 후보를 더 짧은 연결로 갱신하는 처리를 구현합니다.


if __name__ == "__main__":
    vis = va.visualizer("prim")
    while va.running():
        # 같은 그래프로 Kruskal과 Prim의 진행 과정을 비교합니다.
        data = va.next_data(__file__, data_file="data/ch4_1_mst_kruskal.json")
        count = len(data.vertices)
        start = 0
        vis.setup(data, start)
        vis.msg_action("Prim을 실행할 그래프와 시작점을 준비한다.")
        vis.msg_detail("아직 후보를 등록하거나 간선을 선택하지 않은 상태이다.")
        prim(count, data.edges, start)
        # H: 설명 숨김, L: 배치 전환, 정점 드래그: 배치, 빈 곳 드래그: 이동.
        # 휠: 그래프 확대/축소 또는 오른쪽 후보 배열 스크롤.
        # R: 재실행, D: 다음 데이터, Esc: 종료.
        vis.wait()
