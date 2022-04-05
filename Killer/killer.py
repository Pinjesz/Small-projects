from itertools import combinations

def main(range_bounds: list, num_of_nums: int, num_sum:int, unavailable: list) -> list:
    numbers = set(range(range_bounds[0], range_bounds[1] + 1)) - set(unavailable)
    pre_result = list(combinations(numbers, num_of_nums))
    result = []
    for prop in pre_result:
        if sum(prop) == num_sum:
            result.append(prop)
    return result

if __name__ == '__main__':
    range_bounds = [1, 9]
    num_of_nums = 3
    num_sum = 16
    unavailable = [7,3, 9]
    result = main(range_bounds, num_of_nums, num_sum, unavailable)
    print(result)

