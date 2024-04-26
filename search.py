import numpy as np

alphabet = 'abcdefghijklmnopqrstuvwxyz'
alpha_mask = [1 << (ord(c) - ord('a')) for c in alphabet]
ord_chart = {c:ord(c) - ord('a') for c in alphabet}
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
            if word not in words:
                words.add(word)
    return list(words)

def combine_words(m1, m2):
    combined_mask = np.bitwise_or.outer(m1, m2)
    overlap_mask = np.bitwise_and.outer(m1, m2)
    combined_allow_mask = overlap_mask == 0
    raveled_allow_mask = combined_allow_mask.ravel()
    allow_mask_indices = np.where(raveled_allow_mask)[0]
    raveled_combined_mask = combined_mask.ravel()
    return allow_mask_indices, raveled_combined_mask

def main():
    print('building initial word list...')
    words = get_words()
    words = sorted(words)
    # words = [i for i in words if random.random() > 0.9]
    print(len(words))

    print('selecting second word...')
    two_words: dict[int, list[tuple[int, ...]]] = {}
    for i, w1 in enumerate(words):
        for w2 in words[i:]:
            # words must have no overlap and must maintain alphabetical order
            if w1 & w2 == 0 and w1 < w2:
                wc = w1 | w2
                if wc not in two_words:
                    two_words[wc] = []
                two_words[wc].append((w1, w2))

    print(len(two_words))
    two_words_keys = list(two_words.keys())
    two_words_values = list(two_words.values())

    print('np selecting third word...')
    three_words: dict[int, list[tuple[int, ...]]] = {}
    two_words_mask = np.array(two_words_keys, dtype='uint32')
    words_mask = np.array(words, dtype='uint32')
    raveled_indices, raveled_mask = combine_words(two_words_mask, words_mask)
    for i in raveled_indices:
        combined_mask = raveled_mask[i]
        two_index = i // len(words)
        third_index = i % len(words)
        two_groups = two_words_values[two_index]
        third_mask = words[third_index]
        for entry in two_groups:
            if entry[-1] < third_mask:
                if combined_mask not in three_words:
                    three_words[combined_mask] = []
                three_words[combined_mask].append(entry + (third_mask,))

    print(len(three_words))

    print('selecting fourth and fifth words...')
    full_mask = 2**26-1
    final_total = 0
    for missing_letter in alphabet:
        missing_letter_mask = numberify(missing_letter)
        for mask, three_entries in three_words.items():
            if missing_letter_mask & mask != 0:
                continue
            fourth_fifth_mask = missing_letter_mask | mask
            inverted = fourth_fifth_mask ^ full_mask
            if inverted in two_words:
                for three_entry in three_entries:
                    for two_entry in two_words[inverted]:
                        if three_entry[-1] < two_entry[0]:
                            final_total += 1

    print('final answer:', final_total)

if __name__ == '__main__':
    main()
