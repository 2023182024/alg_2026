import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"

vis = va.visualizer("merge_sort")


def merge_sort(array):
    # Merge Sort의 병합 단계에서는 두 절반이 이미 정렬되어 있다고 가정합니다.
    count = len(array)
    mid = count // 2
    array[:mid] = sorted(array[:mid])
    array[mid:] = sorted(array[mid:])

    # 왼쪽 #0..#mid-1와 오른쪽 #mid..#count-1를 병합할 준비를 합니다.
    vis.prepare_merge(0, mid - 1, count - 1)
    merge(array, 0, mid - 1, count - 1)

    return array


def merge(array, left, mid, right):
    # 왼쪽은 #left..#mid, 오른쪽은 #mid+1..#right인 두 정렬된 부분 배열입니다.
    vis.start_merge(left, mid, right)
    left_index = left
    right_index = mid + 1

    # 두 부분 배열의 가장 앞 원소부터 비교를 시작합니다.
    vis.compare(left_index, right_index)
    merged = []
    if array[left_index] <= array[right_index]:
        # 값이 같을 때도 왼쪽을 먼저 복사하면 기존 순서가 유지됩니다.
        merged.append(array[left_index])
        vis.add_to_merged(left_index, merged)
        left_index += 1
    else:
        merged.append(array[right_index])
        vis.add_to_merged(right_index, merged)
        right_index += 1


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", merge_sort(array))
    vis.wait()
