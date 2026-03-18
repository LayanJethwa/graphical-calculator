def frange(start, stop, step): # implements range for floating point numbers
    res, n = start, 1

    while res < stop:
        yield res
        res = start + n * step
        n += 1


class SafeList(list): # extension of list data structure with default value for error handling
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default
