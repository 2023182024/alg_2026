"""Kruskal 알고리즘으로 최소 신장 트리를 만드는 실행 예제."""

import pyvisalgo as va


def kruskal(count, edges):
    """정점 수와 간선 목록을 받아 (선택한 간선 목록, 비용 합)을 반환한다."""
    # 정점 번호는 0부터 count - 1까지입니다.
    # 각 간선 (u, v, weight)는 두 정점과 연결 비용을 나타냅니다.
    # 무방향 간선이므로 (v, u, weight)를 다시 저장하지 않습니다.
    # 정렬과 간선 선택은 다음 단계부터 이 함수 안에 추가합니다.
    # 아직 선택한 간선이 없으므로 빈 목록과 비용 0에서 시작합니다.
    # mst에는 선택한 간선을, total_cost에는 그 가중치 합을 저장합니다.
    mst = []
    total_cost = 0

    # 간선의 세 번째 값인 weight를 기준으로 오름차순 정렬합니다.
    # sorted는 새 목록을 만들므로 원본 데이터의 간선 순서는 바뀌지 않습니다.
    # 같은 가중치를 가진 간선끼리는 원래 입력 순서가 유지됩니다.
    edges = sorted(edges, key=lambda edge: edge[2])
    vis.sort_edges(edges)

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
        # 지금은 초기 상태만 반환합니다. 아직 최소 신장 트리를 구한 것은 아닙니다.
        print("선택한 간선:", mst)
        print("현재 비용:", total_cost)
        # 정점 드래그: 배치 변경, 빈 곳 드래그: 화면 이동, 휠: 확대/축소.
        # H: 설명 숨김, L: 배치 전환, R: 재실행, D: 다음 데이터, Esc: 종료.
        vis.wait()
