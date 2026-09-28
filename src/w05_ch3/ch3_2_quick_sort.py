import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"

vis = va.visualizer("quick_sort")


def quick_sort(array):
    # 전체 배열의 처음과 끝 index를 넘겨 실제 정렬을 시작합니다.
    if len(array) > 0:
        quick_sort_range(array, 0, len(array) - 1)

    return array


def quick_sort_range(array, left, right):
    # 앞으로 이 함수는 left..right 범위를 partition하고, 양쪽을 다시 정렬합니다.
    # 지금은 전체 범위 하나를 대상으로 partition 함수의 역할만 연결합니다.
    vis.push(left, right)
    pivot_index = partition(array, left, right)
    vis.pop()


def partition(array, left, right):
    # partition은 pivot을 제자리로 보내고, 그 index를 반환할 예정입니다.
    # 아직 pivot을 선택하거나 원소를 교환하지 않았으므로 left를 그대로 반환합니다.
    return left


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("퀵 정렬 전:", array)
    print("퀵 정렬 후:", quick_sort(array))
    vis.wait()
