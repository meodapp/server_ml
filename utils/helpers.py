def most_common(lst):
    return max(set(lst), key=lst.count)

def count_corrects(lst):
    c = lst.count(most_common(lst))
    return c

def most_com(lst):
    c = most_common(lst)
    return c
