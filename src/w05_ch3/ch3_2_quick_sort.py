import random

import pyvisalgo as va


DATA_FILE = "data/n_log_n_sort.json"
INSERTION_SORT_THRESHOLD = 4

vis = va.visualizer("quick_sort")


def quick_sort(array):
    # 전체 배열의 처음과 끝 index를 넘겨 실제 정렬을 시작합니다.
    if len(array) > 0:
        quick_sort_range(array, 0, len(array) - 1)

        # 작은 구간은 아직 정렬하지 않았으므로, 마지막에 배열 전체를 삽입 정렬합니다.
        # partition을 충분히 거친 배열에서는 삽입 정렬이 짧은 이동만 수행하게 됩니다.
        insertion_sort(array, 0, len(array) - 1)

    # 가장 바깥쪽 재귀 호출까지 끝나면 배열 전체가 정렬된 상태입니다.
    vis.finish()
    return array


def quick_sort_range(array, left, right):
    # 앞으로 이 함수는 left..right 범위를 partition하고, 양쪽을 다시 정렬합니다.
    # 지금은 전체 범위 하나를 대상으로 partition 함수의 역할만 연결합니다.
    # 작은 구간은 partition하지 않고 남겨 둡니다.
    # 모든 큰 구간의 partition이 끝난 뒤 배열 전체를 삽입 정렬해 마무리합니다.
    if right - left + 1 <= INSERTION_SORT_THRESHOLD:
        return

    vis.push(left, right)
    pivot_index = partition_random(array, left, right)

    # pivot은 제자리가 확정되었으므로, 양쪽 범위만 다시 quick sort 합니다.
    quick_sort_range(array, left, pivot_index - 1)
    quick_sort_range(array, pivot_index + 1, right)

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

    # q의 위치는 pivot이 들어갈 경계입니다. pivot을 q와 교환해 제자리에 놓습니다.
    if left != q:
        vis.swap(left, q, pivot=True)
        array[left], array[q] = array[q], array[left]

    # pivot 왼쪽은 pivot 이하, 오른쪽은 pivot보다 큰 값으로 partition이 끝났습니다.
    vis.fix(q)
    return q


def partition_random(array, left, right):
    """left..right 범위에서 임의로 고른 원소를 pivot으로 삼아 partition한다."""
    # 입력 배열이 이미 정렬되어 있더라도 특정 위치만 pivot으로 고르면 한쪽으로 치우칠 수 있습니다.
    # 매 호출마다 범위 안의 임의 위치를 선택하면 그런 최악의 입력을 만날 가능성을 낮출 수 있습니다.
    pivot_index = random.randint(left, right)
    vis.set_pivot(pivot_index)

    # partition()은 pivot이 left에 있다고 가정하므로 선택한 원소를 먼저 왼쪽으로 옮깁니다.
    vis.move_pivot_to_left(pivot_index, left)
    if pivot_index != left:
        array[left], array[pivot_index] = array[pivot_index], array[left]

    # 이후 p와 q를 움직이며 양쪽을 나누는 과정은 기존 partition()을 그대로 사용합니다.
    return partition(array, left, right)


def insertion_sort(array, left, right):
    """array의 left..right 범위를 삽입 정렬한다. right도 정렬 범위에 포함한다."""
    vis.start_insertion(left, right)

    # #left 하나만 있는 구간은 이미 정렬되어 있으므로, 다음 원소부터 삽입합니다.
    for index in range(left + 1, right + 1):
        value = array[index]
        vis.mark_end(index, pick=True)
        position = index

        # value보다 큰 값을 한 칸씩 오른쪽으로 밀어 value가 들어갈 자리를 만듭니다.
        while position > left:
            vis.compare_for_insertion(position - 1, value)
            if array[position - 1] <= value:
                break
            vis.shift(position - 1, position)
            array[position] = array[position - 1]
            position -= 1

        # 비어 있는 position 위치에 처음에 빼 둔 값을 넣습니다.
        vis.shift(index, position, pick=True)
        array[position] = value

    vis.finish_insertion(left, right)


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("퀵 정렬 전:", array)
    print("퀵 정렬 후:", quick_sort(array))
    vis.wait()
