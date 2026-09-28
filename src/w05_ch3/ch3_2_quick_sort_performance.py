import perf


INSERTION_SORT_THRESHOLD = 4


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
    # 맨 왼쪽 원소를 pivot으로 두고, p와 q가 양쪽에서 경계를 찾습니다.
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
    perf.test(quick_sort, 1_000_000)

    # 실행 예:
    # python src/w05_ch3/ch3_2_quick_sort_performance.py
    # python src/w05_ch3/ch3_2_quick_sort_performance.py nearly
    # python src/w05_ch3/ch3_2_quick_sort_performance.py reversed
