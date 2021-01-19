import pygame
import os
import time

import game_fight
import PopUpWindow
import game_info

SIZE = [660, 660]
MAP_SIZE = [11, 11]


def load_image(dir, name, colorkey=None):
    fullname = os.path.join('data', f'{dir}/{name}.png')
    if not os.path.isfile(fullname):
        name = 'empty'
        fullname = os.path.join('data', f'{dir}/{name}.png')
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_sprite(all_sprites, dir, name, x, y, SIZE, colorkey=None):
    sprite = pygame.sprite.Sprite(all_sprites)
    sprite.image = pygame.transform.scale(load_image(dir, name, colorkey), SIZE)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y


def load_sprites(group, map, koor, dir, cell_size, colorkey=None):
    for i in range(-5, 6, 1):
        for j in range(-5, 6, 1):
            sprite = pygame.sprite.Sprite(group)
            sprite.image = pygame.transform.scale(
                load_image(dir, map[koor[0] + i][koor[1] + j], colorkey), (60, 60))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = (j + 5) * cell_size
            sprite.rect.y = (i + 5) * cell_size


def is_possible_to_move(material):
    if material != 'empty' and material[:4] != 'wall':
        return True
    return False


class Board:
    def __init__(self, screen):
        self.width = MAP_SIZE[0]
        self.height = MAP_SIZE[1]
        self.cell_size = 60
        self.materials_map = game_info.info.read_map('materials')
        self.heroes_map = game_info.info.read_map('heroes')
        self.chest_map = game_info.info.read_map('chest')
        self.screen = screen

    def draw_win_window(self):
        all_sprites = pygame.sprite.Group()
        load_sprite(all_sprites, 'fight', 'win', 0, 0, (660, 660), -1)
        all_sprites.draw(self.screen)
        pygame.display.flip()
        time.sleep(3)

    def draw_map(self, all_sprites, koor):
        load_sprites(all_sprites, self.materials_map, koor, 'materials', self.cell_size)
        load_sprites(all_sprites, self.heroes_map, koor, 'heroes', self.cell_size, -1)

    def draw_hero(self, all_sprites):
        sprite = pygame.sprite.Sprite(all_sprites)
        sprite.image = pygame.transform.scale(load_image('heroes', 'hero'), (60, 60))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = 5 * self.cell_size
        sprite.rect.y = 5 * self.cell_size

    def render(self, screen, koor):
        all_sprites = pygame.sprite.Group()
        self.draw_map(all_sprites, koor)
        self.draw_hero(all_sprites)
        all_sprites.draw(screen)


class Player(Board):
    def __init__(self, screen):
        super().__init__(screen)
        self.player_koor = game_info.info.player_koor
        self.past_player_koor = game_info.info.player_koor

    def new_koor(self, command):
        if command == pygame.K_UP:
            if is_possible_to_move(self.materials_map[self.player_koor[0] - 1][self.player_koor[1]]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[0] -= 1
        elif command == pygame.K_DOWN:
            if is_possible_to_move(self.materials_map[self.player_koor[0] + 1][self.player_koor[1]]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[0] += 1
        elif command == pygame.K_LEFT:
            if is_possible_to_move(self.materials_map[self.player_koor[0]][self.player_koor[1] - 1]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[1] -= 1
        elif command == pygame.K_RIGHT:
            if is_possible_to_move(self.materials_map[self.player_koor[0]][self.player_koor[1] + 1]):
                self.past_player_koor = self.player_koor.copy()
                self.player_koor[1] += 1

    def check_fight_event(self):
        if self.heroes_map[self.player_koor[0]][self.player_koor[1]].split('_')[0] == 'bad':
            fight = game_fight.Fight(self.screen, 'hero', self.heroes_map[self.player_koor[0]][self.player_koor[1]])
            result = fight.run()
            if result == 'hero':
                self.heroes_map[self.player_koor[0]][self.player_koor[1]] = 'empty'
            else:
                self.player_koor = self.past_player_koor

    def check_chest_event(self):
        if self.heroes_map[self.player_koor[0]][self.player_koor[1]] == 'chest' and \
                self.chest_map[self.player_koor[0]][self.player_koor[1]] != 'empty':
            text = game_info.info.get_chest_num(self.chest_map[self.player_koor[0]][self.player_koor[1]])
            self.chest_map[self.player_koor[0]][self.player_koor[1]] = 'empty'
            PopUpWindow.PopUpWindow(self.screen, 'Вы нашли новую часть числа: ' + '\n' + text)
            game_info.info.update_inventory(text)

    def check_password_event(self):
        if self.heroes_map[self.player_koor[0]][self.player_koor[1]] == 'pass':
            inventory = game_info.info.inventory
            all_numbers = game_info.info.get_chest_numbers()

            if len(inventory) == len(all_numbers):
                game_info.info.put_new_level()
                self.draw_win_window()
                return 'game_end'
            else:
                PopUpWindow.PopUpWindow(self.screen, 'Вы собрали не все части моего числа!!!')
                self.player_koor = self.past_player_koor

    def heroes_processing(self):
        self.check_fight_event()
        self.check_chest_event()
        return self.check_password_event()


class Textorcist:
    def __init__(self):
        self.running = True
        pygame.init()
        pygame.display.set_caption('Textorcist')
        self.screen = pygame.display.set_mode(SIZE)
        self.run()

    def clicks_processing(self, player):
        keys_event = pygame.key.get_pressed()
        if keys_event[pygame.K_UP]:
            player.new_koor(pygame.K_UP)
        if keys_event[pygame.K_DOWN]:
            player.new_koor(pygame.K_DOWN)
        if keys_event[pygame.K_LEFT]:
            player.new_koor(pygame.K_LEFT)
        if keys_event[pygame.K_RIGHT]:
            player.new_koor(pygame.K_RIGHT)

    def run(self):
        player = Player(self.screen)
        while self.running:
            self.screen.fill((0, 0, 0))
            player.render(self.screen, player.player_koor)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.clicks_processing(player)
                result = player.heroes_processing()
                if result == 'game_end':
                    self.running = False
                    break
        pygame.quit()
