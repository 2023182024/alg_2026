"""Kruskal 알고리즘으로 최소 신장 트리를 만드는 실행 예제."""

import pyvisalgo as va


def kruskal(count, edges):
    """정점 수와 간선 목록을 받아 (선택한 간선 목록, 비용 합)을 반환한다."""
    # 정점 번호는 0부터 count - 1까지입니다.
    # 각 간선 (u, v, weight)는 두 정점과 연결 비용을 나타냅니다.
    # 무방향 간선이므로 (v, u, weight)를 다시 저장하지 않습니다.
    # 반복 선택과 사이클 검사는 다음 단계에서 추가합니다.
    # 아직 선택한 간선이 없으므로 빈 목록과 비용 0에서 시작합니다.
    # mst에는 선택한 간선을, total_cost에는 그 가중치 합을 저장합니다.
    mst = []
    total_cost = 0

    # 간선의 세 번째 값인 weight를 기준으로 오름차순 정렬합니다.
    # sorted는 새 목록을 만들므로 원본 데이터의 간선 순서는 바뀌지 않습니다.
    # 같은 가중치를 가진 간선끼리는 원래 입력 순서가 유지됩니다.
    edges = sorted(edges, key=lambda edge: edge[2])
    vis.sort_edges(edges)

    # 정렬된 목록의 첫 간선이 가장 가벼운 후보입니다.
    # 세 값을 각각 두 끝점 u, v와 가중치 weight로 나누어 받습니다.
    # 목록에서 삭제하는 것이 아니라 첫 후보를 읽는 것입니다.
    u, v, weight = edges[0]
    vis.begin_edge(u, v)

    # 선택한 간선은 두 끝점과 가중치를 함께 기록합니다.
    # 지금은 선택한 간선이 없으므로 첫 간선 하나만으로는 사이클이 생기지 않습니다.
    # 따라서 이번 단계에서만 루트 비교를 생략합니다.
    # 반복 선택을 구현할 때는 두 끝점의 루트를 먼저 비교해야 합니다.
    # 같으면 제외하고, 다르면 목록에 추가하고 비용을 누적한 뒤 union합니다.
    mst.append((u, v, weight))
    # 선택을 확정한 간선의 가중치만 총비용에 더합니다.
    total_cost += weight
    vis.select_edge(u, v, weight, total_cost)

    return mst, total_cost


if __name__ == "__main__":
    vis = va.visualizer("kruskal")
    while va.running():
        data = va.next_data(__file__)
        count = len(data.vertices)
        print("정점 수:", count)
        print("간선 목록:", data.edges)
        # positions는 그림을 배치하는 좌표일 뿐입니다.
        # Kruskal은 선의 화면상 길이가 아니라 weight를 비교합니다.
        vis.setup(data)
        mst, total_cost = kruskal(count, data.edges)
        # 지금은 간선 하나만 선택합니다. 아직 최소 신장 트리를 완성한 것은 아닙니다.
        print("선택한 간선:", mst)
        print("현재 비용:", total_cost)
        # 정점 드래그: 배치 변경, 빈 곳 드래그: 화면 이동, 휠: 확대/축소.
        # H: 설명 숨김, L: 배치 전환, R: 재실행, D: 다음 데이터, Esc: 종료.
        vis.wait()
