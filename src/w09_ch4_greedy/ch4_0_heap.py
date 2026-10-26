"""정수 배열을 heapify하여 최소 힙으로 바꾼다."""

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

        # heapify는 리스트 자체를 최소 힙으로 바꾸며, 반환값은 None입니다.
        # heap = heapq.heapify(heap)처럼 반환값을 대입하면 안 됩니다.
        # 모든 부모가 자식보다 작거나 같고, 루트 heap[0]에는 최솟값이 있습니다.
        # 형제 사이의 순서까지 정해지는 것은 아니므로 전체 정렬과는 다릅니다.
        heapq.heapify(heap)
        vis.heapify(heap)
        print("heapify:", heap)

        # Space: 일시정지, .: 한 단계, Enter: 현재 연산까지 빠르게 진행.
        # R: 다시 실행, D: 다음 데이터, 1-9: 속도, +/-: 글씨, Esc: 종료.
        vis.wait()
