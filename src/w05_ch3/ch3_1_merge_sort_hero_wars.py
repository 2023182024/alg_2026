import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"

vis = va.visualizer("merge_sort_hero_wars")


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


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", merge_sort(array))
    vis.wait()
