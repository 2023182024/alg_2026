import sys
from random import Random
from time import perf_counter


PERFORMANCE_COUNTS = [
    1000,
    5000,
    10000,
    50000,
    100000,
    200000,
    500000,
    750000,
    1000000,
    5000000,
    7500000,
    10000000,
]


def random_values(count, seed="Hello", low=1, high=None):
    # seed를 고정하면 매번 같은 입력이 만들어져 알고리즘을 공정하게 비교할 수 있습니다.
    rng = Random(seed)
    high = high or count * 10
    return [rng.randint(low, high) for _ in range(count)]


def limited_random_values(count, value_count, seed="Hello"):
    # 값의 종류가 제한된 입력을 만들 때 사용합니다.
    if value_count < 1:
        raise ValueError("value_count must be at least 1")

    rng = Random(seed)
    values = list(range(value_count))
    return [values[rng.randrange(value_count)] for _ in range(count)]


def reversed_values(count):
    # 단순 교환 기반 정렬에서 많은 이동이 필요한 입력입니다.
    return list(range(count, 0, -1))


def sorted_values(count):
    return list(range(1, count + 1))


def nearly_sorted_values(count, seed="Hello", window=100):
    # 정렬된 데이터를 만든 뒤 가까운 위치끼리 섞어, 값이 대체로 제자리 근처에 남게 합니다.
    values = sorted_values(count)
    if count <= 1:
        return values

    rng = Random(seed)
    window = max(1, min(window, count))
    for index in range(count):
        other = index + rng.randrange(window)
        if other >= count:
            other -= window
        values[index], values[other] = values[other], values[index]
    return values


DATA_FUNCS = {
    "random": random_values,
    "nearly": nearly_sorted_values,
    "sorted": sorted_values,
    "reversed": reversed_values,
}


def selected_data_func():
    # 실행할 때 데이터 종류를 지정하지 않으면 일반 random 데이터를 사용합니다.
    data_name = sys.argv[1] if len(sys.argv) > 1 else "random"
    if data_name not in DATA_FUNCS:
        names = ", ".join(DATA_FUNCS.keys())
        raise ValueError(f"unknown data: {data_name} (use: {names})")
    return DATA_FUNCS[data_name]


def test(sort_func, max_count, data_func=None, measure_creation=False):
    # sort_func는 전달받은 리스트를 직접 바꾸거나 새 정렬 리스트를 반환할 수 있습니다.
    if data_func is None:
        data_func = selected_data_func()

    counts = [count for count in PERFORMANCE_COUNTS if count <= max_count]
    if measure_creation:
        print(f"{'Count':>8} {'Create':>10} {'Elapsed':>10}")
    else:
        print(f"{'Count':>8} {'Elapsed':>10}")

    for count in counts:
        create_started_at = perf_counter()
        original = data_func(count)
        create_elapsed = perf_counter() - create_started_at
        array = list(original)

        started_at = perf_counter()
        result = sort_func(array)
        elapsed = perf_counter() - started_at

        sorted_array = array if result is None else result
        if sorted_array != sorted(original):
            raise ValueError(f"{sort_func.__name__} failed to sort {count} values")

        if measure_creation:
            print(f"{count:8d} {create_elapsed:10.3f} {elapsed:10.3f}")
        else:
            print(f"{count:8d} {elapsed:10.3f}")


def test_generated(sort_func, counts, data_func, value_count_func):
    # 큰 입력은 원본 배열을 별도로 복사하지 않아 메모리 사용량을 줄입니다.
    print(f"{'Count':>10} {'Values':>8} {'Create':>10} {'Elapsed':>10}")
    for count in counts:
        create_started_at = perf_counter()
        array = data_func(count)
        create_elapsed = perf_counter() - create_started_at

        started_at = perf_counter()
        result = sort_func(array)
        elapsed = perf_counter() - started_at

        sorted_array = array if result is None else result
        if not _is_sorted(sorted_array):
            raise ValueError(f"{sort_func.__name__} failed to sort {count} values")

        value_count = value_count_func(count)
        print(f"{count:10d} {value_count:8d} {create_elapsed:10.3f} {elapsed:10.3f}")


def _is_sorted(values):
    # values[1:]처럼 큰 임시 배열을 만들지 않고 오름차순 여부를 확인합니다.
    iterator = iter(values)
    try:
        previous = next(iterator)
    except StopIteration:
        return True

    for value in iterator:
        if previous > value:
            return False
        previous = value
    return True
