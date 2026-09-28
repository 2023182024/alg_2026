import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"

vis = va.visualizer("quick_sort")


def quick_sort(array):
    # Quick Sort는 pivot을 기준으로 배열을 둘로 나누고, 각 부분을 다시 정렬합니다.
    # 첫 단계에서는 실행 구조와 사용할 데이터만 준비합니다.
    return array


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("퀵 정렬 전:", array)
    print("퀵 정렬 후:", quick_sort(array))
    vis.wait()
