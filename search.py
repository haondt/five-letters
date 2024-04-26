import math
import random
from re import fullmatch
import numpy as np

ord_chart = {c:ord(c) - ord('a') for c in 'abcdefghijklmnopqrstuvwxyz'}
def numberify(word: str):
    bitmask = 0
    for char in word:
        index = ord_chart[char]
        mask = 1 << index # 00000010000 where 1 is shifted left by the index
        bitmask |= mask # or mask onto final bitmask
    return bitmask

def wordify(number: int):
    word = ''
    for i in range(26):
        mask = 1 << i
        if number & mask != 0:
            word += chr(ord('a') + i)
    return word

def get_words_naive():
    words = set()
    with open('words_alpha.txt', 'r') as f:
        for line in f:
            word = line.strip()
            if len(word) != 5:
                continue
            if len(set(word)) != 5:
                continue
            word = ''.join(sorted(word))
            if word not in words:
                words.add(word)
    return list(words)


def get_words():
    words: set[int] = set()
    with open('words_alpha.txt', 'r') as f:
        for line in f:
            word = line.strip()
            if len(word) != 5:
                continue
            if len(set(word)) != 5:
                continue
            word = ''.join(sorted(word))
            word = numberify(word)
            # print(word, mask, bin(mask), wordify(mask))
            if word not in words:
                words.add(word)
    return list(words)

def is_distinct(w1: int, w2: int):
    return w1 & w2 == 0

# def main():
#     words = get_words()
#     print(len(words))
#
#     two_words: dict[int, int] = {}
#     for mask, count in words.items():
#         for mask2, count2 in words.items():
#             # print(bin(mask))
#             # print(bin(mask2))
#             # print(bin(combined_mask), combined_mask, combined_mask == 0)
#             # print('-------------------------')
#             if mask & mask2 == 0: # no overlap
#                 combined_mask = mask | mask2
#                 if combined_mask not in two_words:
#                     two_words[combined_mask] = count * count2
#                 else:
#                     two_words[combined_mask] += count * count2
#     print(len(two_words))
#     # 4.70s
#
# #     three_words: dict[int, int] = {}
#     for mask, count in words.items():
#         for mask2, count2 in two_words.items():
#             # print(bin(mask))
#             # print(bin(mask2))
#             # print(bin(combined_mask), combined_mask, combined_mask == 0)
#             # print('-------------------------')
#             if mask & mask2 == 0: # no overlap
#                 combined_mask = mask | mask2
#                 if combined_mask not in three_words:
#                     three_words[combined_mask] = count * count2
#                 else:
#                     three_words[combined_mask] += count * count2
#     print(len(three_words))

def combine_words(m1, c1, m2, c2):
    combined_mask = np.bitwise_or.outer(m1, m2)

    overlap_mask = np.bitwise_and.outer(m1, m2)
    combined_allow_mask = overlap_mask == 0
    # intersection_mask = np.tri(m1.size, dtype=bool, k=-1)
    # combined_allow_mask = np.logical_and(combined_allow_mask, intersection_mask)

    combined_counts = np.multiply.outer(c1, c2)

    raveled_allow_mask = combined_allow_mask.ravel()
    raveled_counts = combined_counts.ravel()

    allowed_counts = raveled_counts[raveled_allow_mask]
    allowed_masks = combined_mask.ravel()[raveled_allow_mask]

    compression_dict = {}
    for i, v in enumerate(allowed_masks):
        if v not in compression_dict:
            compression_dict[v] = 0
        compression_dict[v] += allowed_counts[i]

    allowed_counts = []
    allowed_masks = []
    for k, v in compression_dict.items():
        allowed_counts.append(v)
        allowed_masks.append(k)
    allowed_counts = np.array(allowed_counts)
    allowed_masks = np.array(allowed_masks)

    return allowed_masks, allowed_counts


# def main2():
#     words = get_words()
#     words_tup = [(k, v) for k, v in words.items()]
#     words_masks = np.array([i[0] for i in words_tup])
#     words_masksT = np.transpose(words_masks)
#     words_counts = np.array([i[1] for i in words_tup])
#     print(len(words))
#
#     two_words = np.zeros(len(words))
#
#     combined_mask = np.bitwise_or.outer(words_masks, words_masksT)
#
#     overlap_mask = np.bitwise_and.outer(words_masks, words_masksT)
#     combined_allow_mask = overlap_mask == 0
#     intersection_mask = np.tri(words_masks.size, dtype=bool, k=-1)
#     combined_allow_mask = np.logical_and(combined_allow_mask, intersection_mask)
#
#     combined_counts = np.multiply.outer(words_masks, words_masksT)
#
#     raveled_allow_mask = combined_allow_mask.ravel()
#     raveled_counts = combined_counts.ravel()
#
#     allowed_counts = raveled_counts[raveled_allow_mask]
#     allowed_masks = combined_mask.ravel()[raveled_allow_mask]
#
#     compressed_allowed_counts = []
#     compressed_allowed_masks = []
#
#     compression_dict = {}
#     for i, v in enumerate(allowed_masks):
#         if v not in compression_dict:
#             compression_dict[v] = 0
#         compression_dict[v] += allowed_counts[i]
#
#     allowed_counts = []
#     allowed_masks = []
#     for k, v in compression_dict.items():
#         allowed_counts.append(k)
#         allowed_masks.append(v)
#     allowed_counts = np.array(allowed_counts)
#     allowed_masks = np.array(allowed_masks)
#
#
#     print(len(compression_dict))
#
#
#
#     # overlap = np.bitwise_and(words_masks, words_masksT) == 0
#     # overlap = (words_masks[:, np.newaxis] & words_masks[np.newaxis, :])
#     # np.set_printoptions(threshold=100000000)
#
#

# def main3():
#     words = get_words()
#     words_tup = [(k, v) for k, v in words.items()]
#     words_masks = np.array([i[0] for i in words_tup])
#     words_masksT = np.transpose(words_masks)
#     words_counts = np.array([i[1] for i in words_tup])
#     print(len(words))
#
#     m2, c2 = combine_words(words_masks, words_counts, words_masks, words_counts)
#     print(len(m2))
#     m3, c3 = combine_words(words_masks, words_counts, m2, c2)
#     print(len(m3))

class Node:
    def __init__(self):
        self.zero: Node | None = None
        self.one: Node | None = None

alphabet = 'abcdefghijklmnopqrstuvwxyz'
alpha_mask = [1 << (ord(c) - ord('a')) for c in alphabet]
print(alpha_mask)

def iterate_word(word: int):
    remaining_bytes = 26
    remaining_word = word
    def itr():
        nonlocal remaining_bytes
        nonlocal remaining_word
        if remaining_bytes == 0:
            return None
        mask = 1
        bit = mask & remaining_word
        remaining_word >>= 1
        remaining_bytes -= 1
        return bit
    return itr

def build_tree(wordlist: list[int]):
    root = Node()
    current = root
    for word in wordlist:
        itr = iterate_word(word)
        while True:
            next = itr()
            if next is None:
                break
            if next == 1:
                if current.one is None:
                    current.one = Node()
                current = current.one
            else:
                if current.zero is None:
                    current.zero = Node()
                current = current.zero
        current = root
    return root

def is_unlovable_recurse(itr, current: Node):
    next = itr()
    if next == None:
        return False
    elif next == 1:
        if current.zero is None: # we are one, so we want to ensure a 0 exists
            return True
        else:
            return is_unlovable_recurse(itr, current.zero)
    else: # we are a zero, so we don't care what the next is
        if current.one is not None:
            if is_unlovable_recurse(itr, current.one):
                return True
        if current.zero is not None:
            if is_unlovable_recurse(itr, current.zero):
                return True
    return False


def is_unlovable(word: int, tree: Node):
    itr = iterate_word(word)
    return is_unlovable_recurse(itr, tree)


def main4():
    print('building initial word list...')
    words = get_words()
    words = sorted(words)
    # words = [i for i in words if random.random() > 0.8]

    print(len(words))
    print('building base word tree')
    one_word_tree = build_tree(words)
    print('pruning one word tree...')
    print(len(words))
    new_words = []
    for word in words:
        if not is_unlovable(word, one_word_tree):
            new_words.append(word)
    # words = new_words
    print(len(words))



    print('selecting second word...')
    two_words: dict[int, list[tuple[int, ...]]] = {}
    for i, w1 in enumerate(words):
        for w2 in words[i:]:
        # for w2 in words:
            # words must have no overlap and must maintain alphabetical order
            if w1 & w2 == 0 and w1 < w2:
                wc = w1 | w2
                if wc not in two_words:
                    two_words[wc] = []
                two_words[wc].append((w1, w2))
                # two_words[wc] = 1

    print(len(two_words))
    # print(sum([len(i) for i in two_words.values()]))
    print('building two word tree...')
    two_word_tree = build_tree(list(two_words.keys()))
    print('pruning two word tree..')
    new_two_words = {}
    for two_word, v in two_words.items():
        if not is_unlovable(two_word, two_word_tree):
            new_two_words[two_word] = v
    # two_words = new_two_words
    print(len(two_words))



    print('selecting third word...')
    
    three_words: dict[int, list[tuple[int, ...]]] = {}
    last_completion = None
    for i, third_mask in enumerate(words):
        completion = i/len(words)
        if last_completion is None or completion - last_completion > 0.01:
            last_completion = completion
            print(f'\r{round(completion*100,2)}%', end='')

        for two_mask, two_groups in two_words.items():
            if two_mask & third_mask == 0:
                for entry in two_groups:
                    if entry[-1] < third_mask:
                        combined_mask = two_mask | third_mask
                        if combined_mask not in three_words:
                            three_words[combined_mask] = []
                        three_words[combined_mask].append(entry + (third_mask,))
    print()

    print(len(three_words))
    # print('pruning three word tree..')
    # new_three_words = {}
    # for three_word, v in three_words.items():
    #     if not is_unlovable(three_word, two_word_tree):
    #         new_three_words[three_word] = v
    # three_words = new_three_words
    # print(len(three_words))


    print('selecting fourth and fifth words...')
    full_mask = 2**26-1
    final_total = 0
    for missing_letter in 'abcdefghijklmnopqrstuvwxyz':
        missing_letter_mask = numberify(missing_letter)
        for mask, three_entries in three_words.items():
            if missing_letter_mask & mask != 0:
                continue
            fourth_fifth_mask = missing_letter_mask | mask
            # print(bin(fourth_fifth_mask))
            inverted = fourth_fifth_mask ^ full_mask
            # print(str(bin(inverted)).rjust(28))
            # print('---------------------------------------------')
            if inverted in two_words:
                # print(bin(inverted).rjust(30))
                # print(bin(mask).rjust(30))
                # print(bin(missing_letter_mask).rjust(30))
                # print('----------------')
                for three_entry in three_entries:
                    for two_entry in two_words[inverted]:
                        if three_entry[-1] < two_entry[0]:
                            final_total += 1
                # final_total += 1

    print('final answer:', final_total)

    # naive_total = 0
    # naive_words = get_words_naive()
    # for i, t in enumerate(words.items()):
    #     m1, c1 = t
    #     for m2, c2 in words.items():
    #         if m2 & m1 != 0:
    #             continue
    #         m2 |= m1
    #         for m3, c3 in words.items():
    #             if m3 & m2 != 0:
    #                 continue
    #             m3 |= m2
    #             for m4, c4 in words.items():
    #                 if m4 & m3 != 0:
    #                     continue
    #                 m4 |= m3
    #                 for m5, c5 in words.items():
    #                     if m5 & m4 != 0:
    #                         continue
    #                     naive_total += c1 * c2 * c3 * c4 * c5
    #
    # print('naive answer:', naive_total)







if __name__ == '__main__':
    main4()
