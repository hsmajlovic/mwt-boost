import time


def evaluate_method(exe_method, *args):
    start = time.time()
    solution = exe_method(*args)
    end = time.time()
    return end - start, solution
