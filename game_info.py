import os

import UserDataManager


def clear_file(name):
    with open(name, 'w') as input_file:
        input_file.truncate()


class GameInfo:
    def __init__(self):
        self.player_name = ''
        self.level = ''
        self.player_koor = []
        self.inventory = []

    def init_all_info(self):
        self.player_name = self.get_player_name()
        self.level = self.get_level()
        self.player_koor = self.get_player_koor()
        self.inventory = self.get_inventory()

    def get_player_name(self):
        with open('player_name.txt', 'r', encoding='utf8') as input_file:
            return input_file.read()

    def get_level(self):
        with open('level_num.txt', 'r') as input_file:
            return input_file.readline()

    def put_level(self, level):
        clear_file('level_num.txt')
        with open('level_num.txt', 'a') as output_file:
            output_file.write(level)
        self.level = self.get_level()

    def put_new_level(self):
        levels = UserDataManager.get_user_levels()

        if int(self.level.split("_")[1]) + 1 <= 2 and f'level_{int(self.level.split("_")[1]) + 1}' not in \
                levels[self.player_name]:
            levels[self.player_name].append(f"level_{int(self.level.split('_')[1]) + 1}")
            UserDataManager.put_user_levels(levels)

    def clear_files(self):
        clear_file('inventory.txt')

    def read_map(self, view):
        with open(os.path.join('data', 'levels', self.level, 'maps', f'{view}_map.txt'), 'r', encoding='utf8') as f:
            map_file = f.read().split('\n')
            for i in range(len(map_file)):
                while len(map_file[i].replace('  ', ' ')) != len(map_file[i]):
                    map_file[i] = map_file[i].replace('  ', ' ')
            return [mini_pic for mini_pic in [pic.split(' ') for pic in map_file]]

    def get_player_koor(self):
        with open(os.path.join('data', 'levels', self.level, 'player_koor.txt'), 'r', encoding='utf8') as f:
            koor_file = f.read().split(' ')
            return [int(pic) for pic in koor_file]

    def update_inventory(self, text):
        with open('inventory.txt', 'a', encoding='utf8') as output_file:
            output_file.write(text + '\n')
        self.inventory = self.get_inventory()

    def get_inventory(self):
        with open(f'inventory.txt', 'r', encoding='utf8') as input_file:
            inventory = input_file.read().split('\n')
        if inventory[-1] == '':
            inventory = inventory[:-1]
        return inventory

    def get_chest_numbers(self):
        with open(os.path.join('data', 'levels', self.level, 'chest_number.txt'), 'r', encoding='utf8') as input_file:
            all_numbers = input_file.read().split('\n')
        if all_numbers[-1] == '':
            all_numbers = all_numbers[:-1]
        return all_numbers

    def get_chest_num(self, chest_num):
        with open(os.path.join('data', 'levels', self.level, 'chest_number.txt'), 'r', encoding='utf8') as input_file:
            numbers = input_file.read().split('\n')
        return numbers[int(chest_num)]


info = GameInfo()
