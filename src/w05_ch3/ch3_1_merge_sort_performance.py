import perf


def merge_sort(array):
    # 원래 배열과 같은 내용의 보조 배열을 한 번만 준비합니다.
    # 일반 병합 정렬은 merge()가 만든 결과를 다시 원래 배열로 복사합니다.
    # 여기서는 두 배열의 입력/출력 역할을 재귀마다 바꿔 그 복사를 없앱니다.
    copied = list(array)

    # 호출이 끝나면 array 전체에 정렬 결과가 있어야 하므로, copied에서 읽어 array에 씁니다.
    merge_sort_range(copied, array, 0, len(array) - 1)
    return array


def merge_sort_range(source, target, left, right):
    # 이 함수의 약속:
    # - source[left..right]에는 아직 정렬할 값이 있다.
    # - 호출이 끝나면 target[left..right]에 정렬 결과를 쓴다.
    # 이 약속 덕분에 현재 병합 결과를 다시 source로 복사할 필요가 없습니다.

    # 원소가 하나인 범위는 이미 정렬되어 있으므로 더 나눌 필요가 없습니다.
    if left >= right:
        return

    # 2~16개처럼 작은 구간은 source에서 target으로 복사한 뒤 삽입 정렬로 끝냅니다.
    if right - left + 1 <= 16:
        # 이번 호출의 출력 위치는 target이므로, 삽입 정렬 전에 source 값을 옮겨야 합니다.
        target[left : right + 1] = source[left : right + 1]
        insertion_sort(target, left, right)
        return

    # 가운데를 기준으로 왼쪽과 오른쪽 범위를 각각 더 작은 문제로 나눕니다.
    mid = (left + right) // 2
    # 자식 호출은 source와 target을 뒤바꿉니다.
    # 자식이 끝나면 두 정렬 결과는 현재 호출의 source에 놓이므로, 아래 merge()가 읽을 수 있습니다.
    merge_sort_range(target, source, left, mid)
    merge_sort_range(target, source, mid + 1, right)

    # source의 두 정렬 구간을 target에 바로 병합합니다.
    # 병합 결과를 원래 배열에 다시 복사하는 단계는 더 이상 필요하지 않습니다.
    merge(source, target, left, mid, right)


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


def merge(source, target, left, mid, right):
    # source의 #left..#mid, #mid+1..#right 두 정렬 구간을 target에 병합합니다.
    left_index = left
    right_index = mid + 1
    target_index = left

    # 별도의 merged 리스트를 만들지 않고 target의 다음 빈 위치에 바로 기록합니다.
    # C/C++처럼 배열 대입 비용이 낮고 보조 배열을 재사용하는 환경에서는 이 방식이
    # 매 병합 뒤 복사하는 방식보다 더 좋은 성능으로 이어지는 경우가 많습니다.
    # Python에서는 리스트 슬라이스, 참조 수 관리 등의 비용 때문에 이득이 작을 수 있습니다.
    # 양쪽에 모두 원소가 남아 있을 때만 앞 원소끼리 비교합니다.
    while left_index <= mid and right_index <= right:
        if source[left_index] <= source[right_index]:
            # 값이 같을 때도 왼쪽을 먼저 복사하면 기존 순서가 유지됩니다.
            target[target_index] = source[left_index]
            left_index += 1
        else:
            target[target_index] = source[right_index]
            right_index += 1
        target_index += 1

    # 한쪽이 먼저 소진되면 반대쪽의 남은 원소는 이미 정렬된 순서 그대로입니다.
    if left_index <= mid:
        target[target_index : right + 1] = source[left_index : mid + 1]
    else:
        target[target_index : right + 1] = source[right_index : right + 1]


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


'''
Ping-pong merge sort results with insertion sort threshold = 16 (seconds):
   Count    Elapsed
    1000      0.001
    5000      0.003
   10000      0.007
   50000      0.042
  100000      0.076
  200000      0.156
  500000      0.432
  750000      0.655
 1000000      0.916
 5000000      6.141
 7500000      9.795
10000000     13.661
'''
