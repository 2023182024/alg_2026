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
    # 이 예제에서는 맨 왼쪽 원소를 pivot으로 선택합니다.
    # 이후 p와 q가 이 값을 기준으로 반대 방향에서 탐색합니다.
    pivot = array[left]
    vis.set_pivot(left)

    # p는 pivot 다음 원소부터 오른쪽으로, q는 배열 끝에서 왼쪽으로 탐색합니다.
    # 반복문 안에서 먼저 p를 증가시키고 q를 감소시킨 뒤 해당 원소를 확인합니다.
    p = left
    q = right + 1

    # p와 q가 교차할 때까지 양쪽을 탐색하고, 잘못된 쪽의 두 값을 교환합니다.
    while True:
        # p는 pivot 다음부터 오른쪽으로 이동하며 pivot보다 큰 값을 찾습니다.
        # pivot 이하인 값은 왼쪽 부분 배열에 있어도 되므로 그대로 통과합니다.
        while True:
            p += 1
            vis.set_p(p)
            if p > right:
                break
            # p는 오른쪽으로 이동하므로, 비교 표식도 오른쪽 방향으로 애니메이션합니다.
            vis.compare_with_pivot(p, increasing=True)
            if array[p] > pivot:
                break
            vis.accept_left(p)

        # q는 배열 끝에서 왼쪽으로 이동하며 pivot보다 작거나 같은 값을 찾습니다.
        # pivot보다 큰 값은 오른쪽 부분 배열에 있어도 되므로 그대로 통과합니다.
        while True:
            q -= 1
            vis.set_q(q)
            # q는 왼쪽으로 이동하므로, 비교 표식도 왼쪽 방향으로 애니메이션합니다.
            vis.compare_with_pivot(q, increasing=False)
            if array[q] <= pivot:
                break
            vis.accept_right(q)

        # p와 q가 만났거나 교차하면, 더 바꿀 두 원소가 없습니다.
        if p >= q:
            vis.cross(p, q)
            break

        # p의 큰 값은 오른쪽으로, q의 작은 값은 왼쪽으로 보내기 위해 교환합니다.
        vis.swap(p, q)
        array[p], array[q] = array[q], array[p]
        vis.accept_left(p)
        vis.accept_right(q)

    # pivot을 제자리로 옮기는 마지막 교환은 다음 단계에서 처리합니다.
    return left


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("퀵 정렬 전:", array)
    print("퀵 정렬 후:", quick_sort(array))
    vis.wait()
