import pyvisalgo as va


DATA_FILE = "data/elementary_sort.json"

vis = va.visualizer("selection_sort")


def selection_sort(array):
    # 정렬 함수는 전달받은 리스트를 직접 바꿉니다.
    # 선택 정렬은 아직 정렬되지 않은 구간에서 가장 작은 값을 찾아 앞쪽으로 옮깁니다.
    # 최솟값과 같은 값이 여러 개 있으면 리스트1에 위치를 저장해 두었다가,
    # 최솟값 바로 다음 위치들로 한꺼번에 옮깁니다.
    n = len(array)

    # left는 이번 pass에서 값을 확정할 위치입니다.
    # 같은 값이 함께 확정되면 left가 한 번에 여러 칸 이동하므로 while을 사용합니다.
    left = 0
    while left < n:
        # 처음에는 left 위치의 값을 최솟값 후보로 둡니다.
        min_at = left
        vis.selection(min_at)

        # left 오른쪽의 아직 정렬되지 않은 값들을 끝까지 비교합니다.
        for right in range(left + 1, n):
            vis.compare(min_at, right)
            if array[min_at] > array[right]:
                min_at = right
                vis.selection(min_at)

        # 리스트1: 최솟값과 같은 값의 위치들 (최솟값 자신의 위치는 제외)
        min_value = array[min_at]
        list1 = [i for i in range(left, n) if array[i] == min_value and i != min_at]
        for pos in list1:
            vis.selection(pos)

        # 남은 구간에서 찾은 최솟값을 left 위치로 옮깁니다.
        vis.swap(left, min_at)
        array[left], array[min_at] = array[min_at], array[left]
        vis.mark_sorted(left)

        # 리스트1의 값들을 최솟값 바로 다음 위치(left+1, left+2, ...)로 옮깁니다.
        for k, pos in enumerate(list1):
            target = left + 1 + k
            if target != pos:
                vis.swap(target, pos)
                array[target], array[pos] = array[pos], array[target]
            vis.mark_sorted(target)

        # 최솟값 1개 + 같은 값 len(list1)개가 확정되었으므로 그만큼 건너뜁니다.
        left += 1 + len(list1)

    return array


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", selection_sort(array))
    vis.finish()
    vis.wait()