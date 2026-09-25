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

    return array


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", merge_sort(array))
    vis.wait()
