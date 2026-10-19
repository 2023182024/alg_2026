import pyvisalgo as va


DATA_FILE = "data/count_sort.json"

vis = va.visualizer("count_sort")


def count_sort(array):
    # 계수 정렬은 값을 서로 비교하지 않고 각 값의 개수를 세어 정렬합니다.
    # 값 v를 counts[v]에 기록할 수 있도록 최댓값까지의 칸을 준비합니다.
    counts = [0] * (max(array) + 1)
    vis.init_counts(counts)

    # 배열을 왼쪽부터 한 번 훑으며, 값마다 대응하는 counts 칸을 증가시킵니다.
    for index, value in enumerate(array):
        counts[value] += 1
        vis.count_value(index, value, counts)

    # 이제 counts[v]에는 값 v가 입력 배열에 등장한 횟수가 기록되어 있습니다.
    vis.finish_counting()

    # 원본 배열과 같은 길이의 결과 배열을 비어 있는 칸으로 준비합니다.
    result = [None] * len(array)
    vis.init_result(result)

    # 누적합 없이, counts를 값 0부터 차례로 훑으면서 채웁니다.
    # counts[n]이 1 이상이면 n을 result에 채우고 counts[n]을 1 감소시키며,
    # counts[n]이 0이 되면 다음 값 n으로 넘어갑니다.
    n = 0
    at = 0
    while at < len(result):
        if counts[n] >= 1:
            result[at] = n
            counts[n] -= 1
            vis.place_value(at, n, at, counts, result)
            at += 1
        else:
            n += 1

    # result에 완성된 오름차순 결과를 원본 배열에 반영합니다.
    array[:] = result
    vis.finish()
    return array


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", count_sort(array))
    vis.wait()