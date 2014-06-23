"""
Cookie Clicker Simulator
"""

import math


# Constants
SIM_TIME = 10000000000.0


"""
Cookie Clicker Simulator Build Information
"""

BUILD_GROWTH = 1.15


class BuildInfo:
    """
    Class to track build information.
    """

    def __init__(self, build_info = None, growth_factor = BUILD_GROWTH):
        self._build_growth = growth_factor
        if build_info == None:
            self._info = {"Cursor": [15.0, 0.1],
                          "Grandma": [100.0, 0.5],
                          "Farm": [500.0, 4.0],
                          "Factory": [3000.0, 10.0],
                          "Mine": [10000.0, 40.0],
                          "Shipment": [40000.0, 100.0],
                          "Alchemy Lab": [200000.0, 400.0],
                          "Portal": [1666666.0, 6666.0],
                          "Time Machine": [123456789.0, 98765.0],
                          "Antimatter Condenser": [3999999999.0, 999999.0]}
        else:
            self._info = {}
            for key, value in build_info.items():
                self._info[key] = list(value)

    def build_items(self):
        """
        Get a list of buildable items
        """
        return self._info.keys()

    def get_cost(self, item):
        """
        Get the current cost of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][0]

    def get_cps(self, item):
        """
        Get the current CPS of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][1]

    def update_item(self, item):
        """
        Update the cost of an item by the growth factor
        Will throw a KeyError exception if item is not in the build info.
        """
        cost, cps = self._info[item]
        self._info[item] = [cost * self._build_growth, cps]

    def clone(self):
        """
        Return a clone of this BuildInfo
        """
        return BuildInfo(self._info, self._build_growth)


class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._cookies = 0.0
        self._current_time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        return 'Time: %f\nCurrent cookies: %f\nCPS: %f\nTotal cookies %f' % \
               (self._current_time, self._cookies, self._cps, self._total_cookies)

    def print_history(self):
        """
        Print history in a human-readable way
        """
        for record in self._history:
            print record

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._cookies

    def get_total(self):
        """
        Return total number of cookies
        """
        return self._total_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        return math.ceil((cookies - self._cookies) / self._cps) \
            if cookies > self._cookies else 0.0

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        cookies_produced = time * self._cps
        self._cookies += cookies_produced
        self._total_cookies += cookies_produced
        self._current_time += time
        # self._history.append((self._current_time, None, 0.0, self._total_cookies))

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies < cost:
            return
        self._cookies -= cost
        self._cps += additional_cps
        self._history.append((self._current_time, item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    state = ClickerState()
    info = build_info.clone()
    time_to_wait = 0.0
    while state.get_time() <= duration:
        while True:
            purchase = strategy(state.get_cookies(), state.get_cps(), duration - state.get_time(), info)
            # nothing to buy, should just wait to the end of game
            if not purchase:
                time_to_wait = duration - state.get_time()
                break
            purchase_cost = info.get_cost(purchase)
            # cannot buy at this time, should wait until have enough cookies
            if state.time_until(purchase_cost) > 0:
                time_to_wait = min(state.time_until(purchase_cost), \
                                   duration - state.get_time())
                break
            # enough cookies, lets buy
            state.buy_item(purchase, purchase_cost, info.get_cps(purchase))
            info.update_item(purchase)

        if time_to_wait == 0:
            break
        state.wait(time_to_wait)
    return state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!
    """
    return "Cursor"


def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None
    """
    return None


def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always pick the cheapest item available
    """
    items = build_info.build_items()
    item_to_purchase = None
    min_cost = float('inf')
    for item in items:
        cost = build_info.get_cost(item)
        if cost < min_cost:
            min_cost = cost
            item_to_purchase = item
    if min_cost > cookies + cps*time_left:
        item_to_purchase = None
    return item_to_purchase


def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always pick the most expensive item we can afford
    """
    items = build_info.build_items()
    item_to_purchase = None
    max_cost = 0
    for item in items:
        cost = build_info.get_cost(item)
        # pick most expensive across all we can afford in given time
        if cost > max_cost and cost <= cookies + cps*time_left:
            max_cost = cost
            item_to_purchase = item
    if max_cost == 0:
        item_to_purchase = None
    return item_to_purchase


def strategy_best(cookies, cps, time_left, build_info):
    """
    Pick item with best cost/cps ratio
    """
    items = build_info.build_items()
    item_to_purchase = None
    min_cost = float('inf')
    for item in items:
        cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        ratio = cost / item_cps
        if ratio < min_cost and cost <= cookies + cps*time_left:
            min_cost = ratio
            item_to_purchase = item
    if min_cost > cookies + cps*time_left:
        item_to_purchase = None
    return item_to_purchase


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(BuildInfo(), time, strategy)
    print strategy_name, ":\n", state
    print ""
    return state.get_total(), [(item[0], item[3]) for item in state.get_history()]


def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)


if __name__ == '__main__':
    run()
