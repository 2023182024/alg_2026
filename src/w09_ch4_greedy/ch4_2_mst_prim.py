"""Prim의 최소 신장 트리 구현을 위한 실행 구조를 준비한다."""

import pyvisalgo as va


def prim(count, edges, start=0):
    """정점 수, 무방향 간선 목록, 시작 정점을 받아 최소 신장 트리를 구성한다."""
    # 이후 단계에서 후보 등록, 최소 비용 후보 선택, 이웃 검사를 구현합니다.
    pass


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
