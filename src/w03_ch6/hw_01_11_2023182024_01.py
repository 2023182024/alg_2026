
def heap_sort(array):

    pass

def count_sort(array):
    counts= [0] * (max(array)+1)
    for value in enumerate(array):
        counts[value]+=1
        
    for right in range(1,len(counts)):
        left=right-1
        counts[right]+=counts[left]

        answer = [None] * len(array)

        for index in range(len(array)-1,-1,-1):
            value=array[index]

            counts[value]-=1
            answer[counts[value]]=value

    return array

if __name__=="__main__":

    data = [17, 12, 10, 30, 22, 29, 20, 11, 30, 28, 26, 30]

    count_data = list(data)
    
    print("count Sort")
    
    print("정렬 전:", count_data)
    
    count_sort(count_data)
    
    print("정렬 후:", count_data)
    
    print()