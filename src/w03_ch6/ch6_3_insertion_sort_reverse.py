import pyvisalgo as va


DATA_FILE = "data/elementary_sort.json"

vis = va.visualizer("insertion_sort")


def insertion_sort(array):
    # 정렬 함수는 전달받은 리스트를 직접 바꿉니다.
    # 삽입 정렬은 왼쪽의 정렬된 구간에 새 값을 알맞은 위치로 끼워 넣습니다.
    n = len(array)

    # 두 번째 값부터 차례로 왼쪽의 정렬된 구간에 삽입합니다.
    right = 1
    while right < n:
        insert_value = array[right]
        vis.mark_end(right, pick=True)

        # 정렬된 구간을 왼쪽(작은 값)부터 오른쪽(큰 값) 순서로 비교하며
        # insert_value보다 큰 값이 처음 나오는 위치를 찾습니다.
        insert_at = 0
        while insert_at < right:
            vis.compare(insert_at, right)
            if array[insert_at] > insert_value:
                break
            insert_at += 1

        # insert_at부터 right-1까지의 값들을 오른쪽으로 한 칸씩 밀어냅니다.
        j = right
        while j > insert_at:
            vis.shift(j - 1, j)
            array[j] = array[j - 1]
            j -= 1

        # 밀어내기가 끝나면 비워진 위치에 후보 값을 넣습니다.
        vis.shift(right, insert_at, pick=True)
        array[insert_at] = insert_value
        right += 1

    return array


while va.running():
    data = va.next_data(__file__, data_file=DATA_FILE)
    array = list(data.array)

    vis.setup(data)
    print("정렬 전:", array)
    print("정렬 후:", insertion_sort(array))
    vis.finish()
    vis.wait()