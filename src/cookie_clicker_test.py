from poc_simpletest import TestSuite
from cookie_clicker import ClickerState


class ClickerStateTest(TestSuite):

    def __init__(self):
        TestSuite.__init__(self)

    def run(self):
        self.test_time_until()
        self.test_wait()
        self.test_buy_item()
        self.report_results()

    def get_state_vector(self, state):
        return (state.get_time(), state.get_cookies(), state.get_cps())

    def test_time_until(self):
        state = ClickerState()
        self.run_test(state.time_until(10), 10, 'Time until 10 cookies')
        self.run_test(state.time_until(100), 100, 'Time until 100 cookies')
        self.run_test(state.time_until(23.75), 24, 'Time until 23.75 cookies')
        self.run_test(state.time_until(23.01), 24, 'Time until 23.01 cookies')
        self.run_test(state.time_until(0), 0, 'Time until 0 cookies')

    def test_wait(self):
        state = ClickerState()
        state.wait(0)
        self.run_test(self.get_state_vector(state),
                      (0, 0, 1), 'State after waiting 0 seconds')
        state.wait(1)
        self.run_test(self.get_state_vector(state),
                      (1, 1, 1), 'State after waiting 1 seconds')
        state.wait(2.3)
        self.run_test(self.get_state_vector(state),
                      (3.3, 3.3, 1), 'State after waiting 3.3 seconds')
        state.wait(0)
        self.run_test(self.get_state_vector(state),
                      (3.3, 3.3, 1), 'State after still waiting 3.3 seconds')

    def test_buy_item(self):
        state = ClickerState()
        state.wait(1)
        state.buy_item('Cursor', 5, 1)
        self.run_test(self.get_state_vector(state),
                      (1, 1, 1), 'Cannot buy - not enough cookies')
        state.wait(9)
        state.buy_item('Cursor', 5, 1)
        self.run_test(self.get_state_vector(state),
                      (10, 5, 2), 'Bought cursor for 5 cookies')
        self.run_test(len(state.get_history()), 2, 'Buy event in history')
        state.wait(10)
        self.run_test(self.get_state_vector(state),
                      (20, 25, 2), 'State after 20 seconds with cursor')
        state.buy_item('Grandma', 10, 5)
        self.run_test(self.get_state_vector(state),
                      (20, 15, 7), 'Bought grandma for 10 cookies')
        state.wait(10)
        self.run_test(self.get_state_vector(state),
                      (30, 85, 7), 'State after 30 seconds with cursor and grandma')


if __name__ == '__main__':
    test = ClickerStateTest()
    test.run()