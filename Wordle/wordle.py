from itertools import permutations
all_letters = ['w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h',
               'j', 'k', 'l', 'z', 'c', 'b', 'n', 'm', 'ą', 'ś', 'ę', 'ć', 'ż', 'ź', 'ń', 'ó', 'ł']
letters = {}
length = 5


def check_perm(perm: tuple, letters: set):
    for letter in letters:
        if perm.index(letter) not in letters[letter]:
            return False
    return True


def main(are_in: str, are_not_in: str, letters: dict):
    are_in_list = []
    for letter in are_in:
        are_in_list.append(letter)
    while (len(are_in_list) < length):
        are_in_list.append(0)

    perms = list(set(permutations(are_in_list)))
    valid_perms = []
    for perm in perms:
        if check_perm(perm, letters):
            valid_perms.append(perm)

    possible_letters = []
    for letter in all_letters:
        if letter not in are_not_in and letter not in are_in:
            possible_letters.append(letter)

    to_replace = length-len(are_in)
    to_put = len(possible_letters)
    combinations = to_put**to_replace
    num_of_words = 0
    for perm in valid_perms:
        for i in range(combinations):
            temp_i = i
            pattern = []
            for j in range(to_replace):
                idx = temp_i % to_put
                temp_i = temp_i // to_put
                pattern.append(possible_letters[idx])
            word = []
            for k in range(length):
                if perm[k] != 0:
                    word.append(perm[k])
                else:
                    word.append(pattern[0])
                    del pattern[0]
            print(''.join(word))
            num_of_words+=1
    print(num_of_words)


if __name__ == "__main__":
    # information
    are_not_in = 'łórtuiopasgjkzm'
    are_in = 'blędy'
    letters['b'] = [0]
    letters['l'] = [2,3,4]
    letters['ę'] = [1,3,4]
    letters['d'] = [1,2,4]
    letters['y'] = [1,2,3]

    main(are_in, are_not_in, letters)
