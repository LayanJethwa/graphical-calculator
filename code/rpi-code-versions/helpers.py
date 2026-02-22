def frange(start, stop, step):
    res, n = start, 1

    while res < stop:
        yield res
        res = start + n * step
        n += 1


class SafeList(list):
    def get(self, index, default=None):
        try:
            return self[index]
        except IndexError:
            return default
        

def safe_chr(key):
    try:
        return chr(key)
    except (ValueError, OverflowError):
        return None
