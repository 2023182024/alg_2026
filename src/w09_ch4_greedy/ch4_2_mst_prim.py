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
    # 이후 단계에서 후보 등록, 최소 비용 후보 선택, 이웃 검사를 구현합니다.


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
