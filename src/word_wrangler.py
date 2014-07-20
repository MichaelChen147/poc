"""
Student code for Word Wrangler game
"""

import urllib2
# import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list_wo_duplicates = []
    prev_el = None
    for cur_el in list1:
        if cur_el != prev_el:
            list_wo_duplicates.append(cur_el)
            prev_el = cur_el
    return list_wo_duplicates

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    len1, len2 = len(list1), len(list2)
    index1 = index2 = 0
    intersection = []
    while index1 < len1 and index2 < len2:
        if list1[index1] > list2[index2]:
            index2 += 1
        elif list1[index1] < list2[index2]:
            index1 += 1
        else:
            intersection.append(list1[index1])
            index1 += 1
            index2 += 1
    return intersection

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    len1, len2 = len(list1), len(list2)
    index1 = index2 = 0
    merged = []
    while index1 < len1 and index2 < len2:
        if list1[index1] > list2[index2]:
            merged.append(list2[index2])
            index2 += 1
        elif list1[index1] < list2[index2]:
            merged.append(list1[index1])
            index1 += 1
        else:
            merged.append(list1[index1])
            merged.append(list2[index2])
            index1 += 1
            index2 += 1
    for index in range(index1, len1):
        merged.append(list1[index])
    for index in range(index2, len2):
        merged.append(list2[index])
    return merged


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    mid = len(list1) / 2
    left = merge_sort(list1[:mid])
    right = merge_sort(list1[mid:])
    return merge(left, right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [word]
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    this_strings = []
    for rest_string in rest_strings:
        for letter_idx in range(0, len(rest_string) + 1):
            this_string = rest_string[0:letter_idx] + first + rest_string[letter_idx:]
            this_strings.append(this_string)
    return rest_strings + this_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_file = urllib2.urlopen('http://codeskulptor-assets.commondatastorage.googleapis.com/assets_scrabble_words3.txt')
    return [line.strip() for line in word_file.readlines()]

# def run():
#     """
#     Run game.
#     """
#     words = load_words(WORDFILE)
#     wrangler = provided.WordWrangler(words, remove_duplicates, 
#                                      intersect, merge_sort, 
#                                      gen_all_strings)
#     provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    
