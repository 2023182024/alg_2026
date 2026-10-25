"""Kruskal 알고리즘으로 최소 신장 트리를 만드는 실행 예제."""

import pyvisalgo as va


def kruskal(count, edges):
    """정점 수와 간선 목록을 받아 (선택한 간선 목록, 비용 합)을 반환한다."""
    global roots
    # 정점 번호는 0부터 count - 1까지입니다.
    # 각 간선 (u, v, weight)는 두 정점과 연결 비용을 나타냅니다.
    # 무방향 간선이므로 (v, u, weight)를 다시 저장하지 않습니다.
    # 사이클 검사는 다음 단계에서 추가합니다.
    # 아직 선택한 간선이 없으므로 빈 목록과 비용 0에서 시작합니다.
    # mst에는 선택한 간선을, total_cost에는 그 가중치 합을 저장합니다.
    mst = []
    total_cost = 0

    # 처음에는 간선을 선택하지 않았으므로 각 정점이 독립된 집합입니다.
    # 자기 자신을 가리키는 정점이 집합의 대표(루트)입니다.
    # 이후 getRoot와 union에서 함께 사용할 수 있도록 전역 배열로 준비합니다.
    # 이 부모 관계는 집합 관리용이며, 실제 선택 간선 목록인 mst와는 다릅니다.
    roots = [i for i in range(count)]
    vis.start(roots)

    # 간선의 세 번째 값인 weight를 기준으로 오름차순 정렬합니다.
    # sorted는 새 목록을 만들므로 원본 데이터의 간선 순서는 바뀌지 않습니다.
    # 같은 가중치를 가진 간선끼리는 원래 입력 순서가 유지됩니다.
    edges = sorted(edges, key=lambda edge: edge[2])
    vis.sort_edges(edges)

    # 이번에는 가장 가벼운 간선을 정점 수만큼 선택해 봅니다.
    # for문에서 각 간선의 두 끝점과 가중치를 나누어 받습니다.
    # 정점 n개의 사이클 없는 그래프는 간선이 최대 n-1개입니다.
    # 따라서 n개를 무조건 선택하면 사이클이 생깁니다. 이 코드는 아직 정답이 아닙니다.
    # 가벼운 순서만으로는 부족하며, 선택 전에 두 루트를 비교해야 합니다.
    for u, v, weight in edges[:count]:
        if vis.stopped():
            break
        vis.begin_edge(u, v)
        # 선택한 간선은 두 끝점과 가중치를 함께 기록합니다.
        # 완성된 구현에서는 먼저 두 루트를 비교해 같은 집합의 간선은 제외합니다.
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
        # 사이클을 검사하지 않은 중간 결과입니다. 최소 신장 트리가 아닐 수 있습니다.
        print("선택한 간선:", mst)
        print("현재 비용:", total_cost)
        # 정점 드래그: 배치 변경, 빈 곳 드래그: 화면 이동, 휠: 확대/축소.
        # H: 설명 숨김, L: 배치 전환, R: 재실행, D: 다음 데이터, Esc: 종료.
        vis.wait()
