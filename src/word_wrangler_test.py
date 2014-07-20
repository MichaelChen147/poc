from poc_simpletest import TestSuite
from word_wrangler import remove_duplicates, intersect, \
    merge, merge_sort, gen_all_strings

class WordWranglerTest(TestSuite):

    def __init__(self):
        TestSuite.__init__(self)

    def run(self):
        self.test_remove_duplicates()
        self.test_intersect()
        self.test_merge()
        self.test_merge_sort()
        self.test_gen_all_strings()
        self.report_results()
        
    def test_remove_duplicates(self):
        self.run_test(remove_duplicates([1, 2, 3, 4, 5]), 
                      [1, 2, 3, 4, 5], 'No duplicates')
        self.run_test(remove_duplicates([1, 2, 2, 3, 4, 4, 4, 5]),
                      [1, 2, 3, 4, 5], 'Some duplicates')
        self.run_test(remove_duplicates([1, 1, 1, 1, 1]), 
                      [1], 'All duplicates')
        
    def test_intersect(self):
        self.run_test(intersect(
                                [1, 2, 3, 4, 5],
                                [2, 3, 4]),
                      [2, 3, 4], 'Second is a subset of first')
        self.run_test(intersect(
                                [3, 4, 5],
                                [1, 2, 3, 4, 5]),
                      [3, 4, 5], 'First is a subset of second')
        self.run_test(intersect(
                                [1, 2, 3, 4, 5],
                                []),
                      [], 'Second is empty')
        self.run_test(intersect(
                                [1, 2, 3, 4, 5],
                                [1, 2, 3, 4, 5]),
                      [1, 2, 3, 4, 5], 'Lists are equal')

    def test_merge(self):
        self.run_test(merge(
                                [],
                                []),
                      [], 'Empty arrays')
        self.run_test(merge(
                                [1, 2, 3, 4, 5],
                                [2, 3, 4]),
                      [1, 2, 2, 3, 3, 4, 4, 5], 'Second is a subset of first')
        self.run_test(merge(
                                [3, 4, 5],
                                [1, 2, 3, 4, 5]),
                      [1, 2, 3, 3, 4, 4, 5, 5], 'First is a subset of second')
        self.run_test(merge(
                                [1, 2, 3, 4, 5],
                                []),
                      [1, 2, 3, 4, 5], 'Second is empty')
        self.run_test(merge(
                                [1, 2, 3, 4, 5],
                                [1, 2, 3, 4, 5]),
                      [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 'Lists are equal')        

    def test_merge_sort(self):
        self.run_test(merge_sort([]), 
                      [], 'Empty array')
        self.run_test(merge_sort([1, 2, 3, 4, 5]), 
                      [1, 2, 3, 4, 5], 'Already sorted')
        self.run_test(merge_sort([1, 2, 4, 3, 5]), 
                      [1, 2, 3, 4, 5], 'Partially sorted')
        self.run_test(merge_sort([3, 2, 2, 1, 5, 4, 4, 4]),
                      [1, 2, 2, 3, 4, 4, 4, 5], 'With duplicates')
        self.run_test(merge_sort([1, 1, 1, 1, 1]), 
                      [1, 1, 1, 1, 1], 'All duplicates')
        
    def test_gen_all_strings(self):
        self.run_test(gen_all_strings('a'), 
                      ['', 'a'], 'Single letter')
        self.run_test(gen_all_strings('ab'), 
                      ['', 'b', 'a', 'ab', 'ba'], 'Two letters')
        self.run_test(gen_all_strings('aab'), 
                      ["", "b", "a", "ab", "ba", "a", "ab", "ba", "aa", "aa", "aab", "aab", "aba", "aba", "baa", "baa"],
                      'Three letters')

if __name__ == '__main__':
    WordWranglerTest().run()