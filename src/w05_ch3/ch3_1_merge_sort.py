import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"

vis = va.visualizer("merge_sort")


def merge_sort(array):
    # 다음 커밋부터 두 정렬된 부분 배열을 병합하는 과정을 추가합니다.
    return array


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", merge_sort(array))
    vis.wait()
