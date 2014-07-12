from poc_simpletest import TestSuite
from zombie import Zombie

class ZombieTest(TestSuite):

    def __init__(self):
        TestSuite.__init__(self)

    def run(self):
        self.test_zombie()
        self.test_distance_human()
        self.test_distance_zombie()
        self.test_move_human()
        self.test_move_zombie()
        self.report_results()
        
    def create_game(self):
        return Zombie(
                      grid_height = 4,
                      grid_width = 4,
                      obstacle_list = [(2,2)],
                      zombie_list = [(3,0)],
                      human_list = [(3,1)]
                      )
    
    def get_human(self, game, human_index):
        cnt = 0
        for human in game.humans():
            if (cnt == human_index):
                return human
            cnt += 1
        return None
    
    def get_zombie(self, game, zombie_index):
        cnt = 0
        for zombie in game.zombies():
            if (cnt == zombie_index):
                return zombie
            cnt += 1
        return None
        
    def test_zombie(self):
        game = self.create_game()
        game.add_human(1,1)
        self.run_test(game.num_zombies(), 1, 'One zombie')
        self.run_test(game.num_humans(), 2, 'Two humans')
        self.run_test(self.get_human(game, 0), (3, 1), 'Human #1')
        self.run_test(self.get_human(game, 1), (1, 1), 'Human #2')
            
    def test_distance_human(self):
        game = self.create_game()
        distances = game.compute_distance_field('human')
        self.run_test(distances,
                      [[4, 3, 4, 5],
                       [3, 2, 3, 4],
                       [2, 1, 16, 3],
                       [1, 0, 1, 2]],
                       'Distance to one human')
        game.add_human(1,1)
        distances = game.compute_distance_field('human')
        self.run_test(distances,
                      [[2, 1, 2, 3],
                       [1, 0, 1, 2],
                       [2, 1, 16, 3],
                       [1, 0, 1, 2]],
                       'Distance to two humans')
        
    def test_distance_zombie(self):
        game = self.create_game()
        distances = game.compute_distance_field('zombie')
        self.run_test(distances,
                      [[3, 4, 5, 6],
                       [2, 3, 4, 5],
                       [1, 2, 16, 4],
                       [0, 1, 2, 3]],
                       'Distance to one zombie')
        game.add_zombie(1, 2)
        game.add_zombie(1, 2)
        distances = game.compute_distance_field('zombie')
        self.run_test(distances,
                      [[3, 2, 1, 2],
                       [2, 1, 0, 1],
                       [1, 2, 16, 2],
                       [0, 1, 2, 3]],
                       'Distance to three zombies')

    def test_move_human(self):
        game = self.create_game()
        distances = game.compute_distance_field('zombie')
        game.move_humans(distances)
        human = self.get_human(game, 0)
        self.run_test(human in [(2,1), (3,2)], True, 'Human moved')
        
    def test_move_zombie(self):
        game = self.create_game()
        distances = game.compute_distance_field('human')
        game.move_zombies(distances)
        self.run_test(self.get_zombie(game, 0), (3,1), 'Zombie moved')


if __name__ == '__main__':
    ZombieTest().run()
