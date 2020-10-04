def merge(left_slice, right_slice):
    lindex = 0
    rindex = 0
    result = []
    while lindex != len(left_slice) or rindex != len(right_slice):
        if lindex == len(left_slice):
            result = result + right_slice[rindex:len(right_slice)]
            return result
        elif rindex == len(right_slice):
            result = result + left_slice[lindex:len(left_slice)]
            return result
        elif left_slice[lindex] < right_slice[rindex]:
            result.append(left_slice[lindex])
            lindex = lindex + 1
        elif left_slice[lindex] > right_slice[rindex]:
            result.append(right_slice[rindex])
            rindex = rindex + 1
        else:
            result.append(right_slice[rindex])
            rindex = rindex + 1
            result.append(left_slice[lindex])
            lindex = lindex + 1
    return result

def sort(numbers, executor):
    """merge sort"""
    if len(numbers) == 1:
        return numbers

    left_slice = numbers[0:len(numbers)//2]
    right_slice = numbers[len(numbers)//2:len(numbers)] 
    left_future = executor.submit(sort, left_slice, executor)
    right_future = executor.submit(sort, right_slice, executor)
    left_slice = left_future.result()
    right_slice = right_future.result()
    return merge(left_slice, right_slice)