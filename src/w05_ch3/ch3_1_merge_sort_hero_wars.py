import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"

vis = va.visualizer("merge_sort_hero_wars")


def merge_sort(array):
    # 전체 배열 범위를 전달하고, 실제 정렬은 범위 함수가 담당하게 합니다.
    merge_sort_range(array, 0, len(array) - 1)

    # 가장 바깥쪽 병합까지 끝나면 전체 배열이 정렬된 상태입니다.
    vis.finish()
    return array


def merge_sort_range(array, left, right):
    # 현재 정렬할 범위를 호출 스택에 쌓아, 재귀적으로 나뉘는 모습을 표시합니다.
    vis.push(left, right)

    # 원소가 하나인 범위는 이미 정렬되어 있으므로 더 나눌 필요가 없습니다.
    if left >= right:
        vis.single(left)
        vis.pop()
        return

    # 가운데를 기준으로 왼쪽과 오른쪽 범위를 각각 더 작은 문제로 나눕니다.
    mid = (left + right) // 2
    vis.split(left, mid, right)
    merge_sort_range(array, left, mid)
    merge_sort_range(array, mid + 1, right)

    # 두 재귀 호출이 끝난 뒤에는 두 절반이 각각 정렬된 상태가 됩니다.
    merge(array, left, mid, right)
    vis.pop()


def merge(array, left, mid, right):
    # 왼쪽은 #left..#mid, 오른쪽은 #mid+1..#right인 두 정렬된 부분 배열입니다.
    vis.start_merge(left, mid, right)
    left_index = left
    right_index = mid + 1

    merged = []
    # 양쪽에 모두 원소가 남아 있을 때만 앞 원소끼리 비교합니다.
    while left_index <= mid and right_index <= right:
        vis.compare(left_index, right_index)
        if array[left_index] <= array[right_index]:
            # 더 약한(작은) 전사가 먼저 결과 줄로 빠져나간다고 생각합니다.
            merged.append(array[left_index])
            vis.add_to_merged(left_index, merged)
            left_index += 1
        else:
            merged.append(array[right_index])
            vis.add_to_merged(right_index, merged)
            right_index += 1

    # 한쪽이 먼저 소진되면 반대쪽의 남은 전사는 이미 정렬된 순서 그대로입니다.
    if left_index <= mid:
        vis.exhausted("right")
        while left_index <= mid:
            merged.append(array[left_index])
            vis.add_to_merged(left_index, merged)
            left_index += 1
    else:
        vis.exhausted("left")
        while right_index <= right:
            merged.append(array[right_index])
            vis.add_to_merged(right_index, merged)
            right_index += 1

    # 완성된 결과 줄을 원래 배열의 병합 구간으로 되돌립니다.
    vis.end_merge()
    vis.copy_back(left, right, merged)
    array[left : right + 1] = merged


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", merge_sort(array))
    vis.wait()
