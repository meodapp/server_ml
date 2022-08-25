def str_to_int(x):
    return abs(hash(x)) % (10 ** 8)


def to_int(x):
    try:
        return int(x)
    except:
        return 0