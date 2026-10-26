"""Prim의 최소 신장 트리 구현을 위한 실행 구조를 준비한다."""

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


def pop_smallest(weights):
    """비어 있지 않은 후보 딕셔너리에서 최소 비용 후보 하나를 찾아 제거한다."""
    # 딕셔너리를 순회하면 key인 정점 번호가 나옵니다.
    # key 함수는 각 정점에 저장된 value의 첫 항목, 즉 비용을 비교하도록 합니다.
    # min(weights)만 쓰면 비용이 아니라 정점 번호가 가장 작은 후보를 고릅니다.
    vertex = min(weights, key=lambda vertex: weights[vertex][0])
    cost, origin = weights.pop(vertex)
    # 후보를 정점별로 찾고 지우기는 쉬워졌지만 최솟값 탐색은 여전히 O(후보 수)입니다.
    # 호출하는 쪽은 같은 순서로 받을 수 있도록 [비용, 정점, 출발점]을 반환합니다.
    return [cost, vertex, origin]


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
    # 이전 리스트: weights = [[weight, vertex_to, vertex_from], ...]
    # 현재 딕셔너리: weights = {vertex_to: [weight, vertex_from], ...}
    # 도착 정점이 각 원소의 두 번째 항목에서 딕셔너리의 key로 이동했습니다.
    # key는 도착 정점, value는 [연결 비용, 출발 정점]입니다.
    # 정점 번호로 기존 후보를 바로 조회하거나 비용과 출발점을 갱신할 수 있습니다.
    # Prim의 비용은 시작점부터의 누적 거리가 아니라 연결할 간선 하나의 비용입니다.
    weights = {}
    # 시작점은 연결 간선 없이 출발하므로 비용 0, 출발점은 자기 자신으로 둡니다.
    # 이 항목은 실제 간선이 아니며, 시작점은 아직 내륙으로 확정하지 않았습니다.
    weights[start] = [0, start]
    vis.add_candidate(start, 0, start, weights, starting=True)
    # 후보가 남아 있는 동안 가장 저렴하게 연결할 수 있는 정점을 하나씩 꺼냅니다.
    while weights:
        if vis.stopped():
            break
        cost, vertex, origin = pop_smallest(weights)
        # 가장 저렴한 후보를 꺼내면 곧바로 내륙으로 확정합니다.
        completed.add(vertex)
        # 시작점의 비용 0은 실제 간선이 아니므로 간선 목록과 비용 합에서 제외합니다.
        if vertex != origin:
            mst.append((origin, vertex, cost))
            total_cost += cost
        vis.take_candidate(vertex, cost, origin, weights, total_cost)
        # 아직 이웃 검사가 없어 시작점만 확정하고 끝납니다.


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
