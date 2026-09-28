import perf


INSERTION_SORT_THRESHOLD = 8
# 작은 partition에는 median-of-three를, 큰 partition에는 ninther를 사용합니다.
# LLVM libc++ std::sort는 128개 초과 구간부터 ninther를 선택하며,
# 이 수업의 성능 측정 버전은 경계값도 포함해 128개 이상에서 적용합니다.
NINTHER_THRESHOLD = 128


def quick_sort(array):
    # 성능 측정용 기본 Quick Sort는 배열 전체를 재귀적으로 partition합니다.
    if len(array) > 0:
        quick_sort_range(array, 0, len(array) - 1)
    return array


def quick_sort_range(array, left, right):
    # 원소가 하나 이하인 범위는 이미 정렬되어 있습니다.
    if left >= right:
        return

    pivot_index = partition(array, left, right)
    quick_sort_range(array, left, pivot_index - 1)
    quick_sort_range(array, pivot_index + 1, right)


def quick_sort_final_insertion(array):
    # 작은 구간을 남긴 상태까지 partition한 뒤, 배열 전체를 한 번 삽입 정렬합니다.
    if len(array) > 0:
        quick_sort_range_until(array, 0, len(array) - 1)
        insertion_sort(array, 0, len(array) - 1)
    return array


def quick_sort_range_until(array, left, right):
    # 임계값 이하의 작은 구간은 정렬하지 않고 그대로 남겨 둡니다.
    if right - left + 1 <= INSERTION_SORT_THRESHOLD:
        return

    pivot_index = partition(array, left, right)
    quick_sort_range_until(array, left, pivot_index - 1)
    quick_sort_range_until(array, pivot_index + 1, right)


def partition(array, left, right):
    # partition을 수행하는 구간에서는 먼저 median-of-three 또는 ninther로 pivot을 고릅니다.
    # 선택된 값을 맨 왼쪽으로 옮긴 뒤 기존 p/q 탐색 규칙을 그대로 적용합니다.
    pivot_index = choose_pivot(array, left, right)
    if pivot_index != left:
        array[left], array[pivot_index] = array[pivot_index], array[left]

    pivot = array[left]
    p = left
    q = right + 1

    while True:
        while True:
            p += 1
            if p > right or array[p] > pivot:
                break

        while True:
            q -= 1
            if array[q] <= pivot:
                break

        if p >= q:
            break

        array[p], array[q] = array[q], array[p]

    array[left], array[q] = array[q], array[left]
    return q


def choose_pivot(array, left, right):
    """구간 크기에 맞춰 median-of-three 또는 ninther pivot의 index를 고른다."""
    count = right - left + 1
    middle = (left + right) // 2

    # 최종 삽입 정렬을 사용하는 현재 버전에서는 partition되는 구간이 항상 9개 이상입니다.
    # 따라서 128개 미만 구간에서는 양 끝과 가운데의 median-of-three면 충분합니다.
    if count < NINTHER_THRESHOLD:
        return median_of_three_index(array, left, middle, right)

    # ninther는 구간 전체에 고르게 퍼진 9개 표본을 세 묶음으로 나눕니다.
    # 각 묶음의 median 3개를 다시 비교해 최종 pivot을 고릅니다.
    step = (right - left) // 8
    first_median = median_of_three_index(array, left, left + step, left + step * 2)
    second_median = median_of_three_index(array, middle - step, middle, middle + step)
    third_median = median_of_three_index(array, right - step * 2, right - step, right)
    return median_of_three_index(array, first_median, second_median, third_median)


def median_of_three_index(array, first, second, third):
    """세 원소를 교환하지 않고 값의 중간인 원소의 index를 반환한다."""
    if array[first] > array[second]:
        first, second = second, first
    if array[second] > array[third]:
        second, third = third, second
    if array[first] > array[second]:
        first, second = second, first
    return second


def insertion_sort(array, left, right):
    # partition을 마친 배열은 거의 정렬되어 있으므로, 한 번의 삽입 정렬로 마무리합니다.
    for index in range(left + 1, right + 1):
        value = array[index]
        position = index - 1

        while position >= left and array[position] > value:
            array[position + 1] = array[position]
            position -= 1

        array[position + 1] = value


if __name__ == "__main__":
    perf.test(quick_sort_final_insertion, 10_000_000)

    # 실행 예:
    # python src/w05_ch3/ch3_2_quick_sort_performance.py
    # python src/w05_ch3/ch3_2_quick_sort_performance.py nearly
    # python src/w05_ch3/ch3_2_quick_sort_performance.py reversed


'''
Test Results: (Threshold = 8, Final Insertion Sort)
T1: 맨 왼쪽 원소를 pivot으로 선택한 기존 버전
T2: 128개 미만은 median-of-three, 128개 이상은 ninther를 선택한 버전

   Count       T1       T2
    1000    0.001    0.000
    5000    0.003    0.003
   10000    0.006    0.005
   50000    0.033    0.027
  100000    0.066    0.057
  200000    0.129    0.142
  500000    0.359    0.345
  750000    0.593    0.535
 1000000    0.817    0.746
 5000000    5.401    5.027
 7500000    8.684    8.035
10000000   11.994   11.121

위 결과는 랜덤 데이터로 측정했다.
이미 정렬되었거나 역순처럼 pivot이 한쪽으로 치우치기 쉬운 입력에서는
median-of-three와 ninther가 더 균형 잡힌 partition을 만들어 더 빨라질 수도 있다.
'''
