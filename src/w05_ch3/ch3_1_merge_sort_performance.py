import perf


def merge_sort(array):
    # 전체 배열 범위를 전달하고, 실제 정렬은 범위 함수가 담당하게 합니다.
    merge_sort_range(array, 0, len(array) - 1)
    return array


def merge_sort_range(array, left, right):
    # 원소가 하나인 범위는 이미 정렬되어 있으므로 더 나눌 필요가 없습니다.
    if left >= right:
        return

    # 2~4개처럼 작은 구간은 다시 반으로 나누고 병합하는 대신 삽입 정렬로 끝냅니다.
    if right - left + 1 <= 16:
        insertion_sort(array, left, right)
        return

    # 가운데를 기준으로 왼쪽과 오른쪽 범위를 각각 더 작은 문제로 나눕니다.
    mid = (left + right) // 2
    merge_sort_range(array, left, mid)
    merge_sort_range(array, mid + 1, right)

    # 두 재귀 호출이 끝난 뒤에는 두 절반이 각각 정렬된 상태가 됩니다.
    merge(array, left, mid, right)


def insertion_sort(array, left, right):
    """array의 left..right 구간을 삽입 정렬한다. right도 정렬 범위에 포함한다."""
    # #left 하나만 있는 구간은 이미 정렬되어 있으므로, 다음 원소부터 삽입합니다.
    for index in range(left + 1, right + 1):
        value = array[index]
        position = index - 1

        # value보다 큰 값을 한 칸씩 오른쪽으로 밀어 value가 들어갈 자리를 만듭니다.
        while position >= left and array[position] > value:
            array[position + 1] = array[position]
            position -= 1

        # 비어 있는 position + 1 위치에 처음에 빼 둔 값을 넣습니다.
        array[position + 1] = value


def merge(array, left, mid, right):
    # 왼쪽은 #left..#mid, 오른쪽은 #mid+1..#right인 두 정렬된 부분 배열입니다.
    left_index = left
    right_index = mid + 1

    merged = []
    # 양쪽에 모두 원소가 남아 있을 때만 앞 원소끼리 비교합니다.
    while left_index <= mid and right_index <= right:
        if array[left_index] <= array[right_index]:
            # 값이 같을 때도 왼쪽을 먼저 복사하면 기존 순서가 유지됩니다.
            merged.append(array[left_index])
            left_index += 1
        else:
            merged.append(array[right_index])
            right_index += 1

    # 한쪽이 먼저 소진되면 반대쪽의 남은 원소는 이미 정렬된 순서 그대로입니다.
    if left_index <= mid:
        while left_index <= mid:
            merged.append(array[left_index])
            left_index += 1
    else:
        while right_index <= right:
            merged.append(array[right_index])
            right_index += 1

    # 완성된 임시 배열을 원래 배열의 병합 구간으로 되돌립니다.
    array[left : right + 1] = merged


if __name__ == "__main__":
    perf.test(merge_sort, 10_000_000)

    # 실행 예:
    # python src/w05_ch3/ch3_1_merge_sort_performance.py
    # python src/w05_ch3/ch3_1_merge_sort_performance.py nearly
    # python src/w05_ch3/ch3_1_merge_sort_performance.py reversed


'''
Performance test results (seconds):
   Count  Threshold 4  Threshold 16
    1000        0.001         0.001
    5000        0.004         0.003
   10000        0.013         0.006
   50000        0.037         0.047
  100000        0.074         0.073
  200000        0.159         0.146
  500000        0.423         0.412
  750000        0.661         0.614
 1000000        0.894         0.863
 5000000        6.121         5.746
 7500000        9.643         9.362
10000000       13.737        13.038
'''
