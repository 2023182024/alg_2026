
def bubble_sort(array):

    for i in range(1,len(array)-1):
        for j in range(1, len(array)-i):
            if(array[j-1]>array[j]):
                array[j-1],array[j]=array[j],array[j-1]

    pass

def selection_sort(array):
    
    for i in range(0,len(array)-2):
        min=i
        for j in range(i+1,len(array)-1):
            if(array[j]<array[min]):
                min=j
        array[i],array[min]=array[min],array[i]
                       
    pass

def insertion_sort(array):

    for i in range(1,len(array)-1):
        index=array[i]
        j=i-1
        while(j>=0 and array[j]>index):
            array[j+1]=array[j]
            j=j-1
        array[j+1]=index

    pass

if __name__ == "__main__":

    data = [17, 12, 10, 30, 22, 29, 20, 11, 30, 28, 26, 30]

 

    bubble_data = list(data)

    print("Bubble Sort")

    print("정렬 전:", bubble_data)

    bubble_sort(bubble_data)

    print("정렬 후:", bubble_data)

    print()

 

    selection_data = list(data)

    print("Selection Sort")

    print("정렬 전:", selection_data)

    selection_sort(selection_data)

    print("정렬 후:", selection_data)

    print()

 

    insertion_data = list(data)

    print("Insertion Sort")

    print("정렬 전:", insertion_data)

    insertion_sort(insertion_data)

    print("정렬 후:", insertion_data)

