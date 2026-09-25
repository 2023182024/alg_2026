import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"

vis = va.visualizer("merge_sort")


def merge_sort(array):
    # 전체 배열 범위를 전달하고, 실제 정렬은 범위 함수가 담당하게 합니다.
    merge_sort_range(array, 0, len(array) - 1)

    return array


def merge_sort_range(array, left, right):
    # 현재는 병합 단계를 설명하기 위해 두 절반이 이미 정렬되었다고 가정합니다.
    mid = (left + right) // 2
    array[left : mid + 1] = sorted(array[left : mid + 1])
    array[mid + 1 : right + 1] = sorted(array[mid + 1 : right + 1])

    # 왼쪽 #left..#mid와 오른쪽 #mid+1..#right를 병합할 준비를 합니다.
    vis.prepare_merge(left, mid, right)
    merge(array, left, mid, right)


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
            # 값이 같을 때도 왼쪽을 먼저 복사하면 기존 순서가 유지됩니다.
            merged.append(array[left_index])
            vis.add_to_merged(left_index, merged)
            left_index += 1
        else:
            merged.append(array[right_index])
            vis.add_to_merged(right_index, merged)
            right_index += 1

    # 한쪽이 먼저 소진되면 반대쪽의 남은 원소는 이미 정렬된 순서 그대로입니다.
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

    # 완성된 임시 배열을 원래 배열의 병합 구간으로 되돌립니다.
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
