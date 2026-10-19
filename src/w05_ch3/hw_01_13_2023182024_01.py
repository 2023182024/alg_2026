"""실습 과제 13: Merge Sort, Quick Sort, Selection을 구현한다."""

import random


RANDOM_SEED = "EX_01"
ARRAY_SIZE = 30



def merge_sort(array):
    """array를 오름차순으로 직접 정렬한다."""
    # TODO: Merge Sort를 구현한다.
    # 함수는 새 정렬 결과를 반환하지 않고, 전달받은 array를 직접 정렬해야 한다.

    merge_sort_range(array,0,len(array)-1)
    return array
    pass

def merge_sort_range(array, left, right):   # left와 right를 포함함

    if left >= right:
        return


    mid = (left + right) // 2
    '''left에서 mid까지, mid+1부터 right까지 분할하여 재귀 호출'''
    merge_sort_range(array,left,mid)
    merge_sort_range(array,mid+1,right)


    #left~mid, mid+1~right를 병합
    left_index = left
    right_index=mid +1
    temp=[]

    while left_index<=mid and right_index<=right:
        if array[left_index]<=array[right_index]:
            temp.append(array[left_index])
            left_index+=1
        else:
            temp.append(array[right_index])
            right_index+=1

    if left_index<=mid:
        while left_index<=mid:
            temp.append(array[left_index])
            left_index+=1
    else:
        while right_index<=right:
            temp.append(array[right_index])
            right_index+=1

    array[left:right+1]=temp
    pass



def quick_sort(array):
    """array를 오름차순으로 직접 정렬한다."""
    # TODO: Quick Sort를 구현한다.
    # 함수는 새 정렬 결과를 반환하지 않고, 전달받은 array를 직접 정렬해야 한다.

    if len(array) > 0:
        quick_sort_range(array, 0, len(array) - 1)

    return array
    pass

def quick_sort_range(array,left,right):

    if left >= right:
        return

    '''partition 으로 index를 만들고, 좌측 끝부터 index-1까지, index+1부터 오른쪽 끝까지 정렬한다'''
    pivot_index=partition(array,left,right)
    quick_sort_range(array,left,pivot_index-1)
    quick_sort_range(array,pivot_index+1,right)

    pass

def partition(array,left,right):    #left와 right를 모두 포함한다

    pivot=array[left]
    i=left
    j=right

    while True:
        while(i<=right and array[i]<=pivot):
            i+=1
        while(array[j]>pivot):
            j-=1

        if(i>=j):
            break

        array[i],array[j]=array[j],array[i]

    if left != j:
        array[left], array[j] = array[j], array[left]

    return j    #정렬된 최종 위치에 해당하는 pivot을 반환 


def selection(array, n):
    """array에서 n번째로 작은 값을 반환한다. n은 1부터 시작한다."""
    # TODO: Selection 알고리즘을 구현한다.
    # partition 과정에서 array의 원소 위치가 바뀌어도 된다.

    if not 1<=n<=len(array):
        return None

    return selection_range(array,0,len(array)-1,n)
    pass

def selection_range(array,left,right,n):

    pivot_index=partition(array,left,right) #left와 right를 모두 포함한다
    pivot_rank=pivot_index-left+1

    if(n==pivot_rank):
        return array[pivot_index]

    if(n<pivot_rank):
        return selection_range(array,left,pivot_index-1,n)  #배열의 가장 왼쪽 값부터 partition으로 생성한 기준값-1

    next_rank=n-pivot_rank
    return selection_range(array,pivot_index+1,right,next_rank) #partition으로 생성한 기준값+1 부터 right까지

    pass

def make_random_array(randomizer):
    """1부터 99 사이의 값 ARRAY_SIZE 개를 가진 새 배열을 만든다."""
    return [randomizer.randint(1, 99) for _ in range(ARRAY_SIZE)]


if __name__ == "__main__":
    randomizer = random.Random(RANDOM_SEED)

    # 정렬 두 개는 서로 다른 무작위 배열을 사용한다.
    merge_data = make_random_array(randomizer)
    quick_data = make_random_array(randomizer)

    print("Merge Sort")
    print("정렬 전:", merge_data)
    merge_sort(merge_data)
    print("정렬 후:", merge_data)
    print()

    print("Quick Sort")
    print("정렬 전:", quick_data)
    quick_sort(quick_data)
    print("정렬 후:", quick_data)
    print()

    # Selection은 하나의 30개 배열에서 서로 다른 두 순위를 찾는다.
    selection_data = make_random_array(randomizer)
    first_n = randomizer.randint(10, 24)
    second_n = randomizer.randint(10, 24)

    print("Selection")
    print("배열:", selection_data)
    print(f"{first_n}번째로 작은 값은:", selection(selection_data, first_n))
    print(f"{second_n}번째로 작은 값은:", selection(selection_data, second_n))
