"""heapq 실습을 시작하기 전에 정수 배열을 준비한다."""

import heapq

import pyvisalgo as va


# Python 3.14부터 heapify_max, heappush_max, heappop_max도 공식 지원합니다.
# 이 예제는 Python 3.13에서도 실행하도록 최소 힙 API만 사용합니다.
if __name__ == "__main__":
    vis = va.visualizer("heap_queue")
    while va.running():
        data = va.next_data(__file__)
        heap = data.array.copy()
        vis.setup(data, heap)
        print("준비:", heap)

        # 배열을 트리 모양으로 배치했을 뿐, 아직 최소 힙으로 만들지는 않았습니다.
        # R: 다시 실행, D: 다음 데이터, +/-: 글씨, Esc: 종료.
        vis.wait()
