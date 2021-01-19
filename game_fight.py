import pygame
import sys
import os
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', f'{name}.png')
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_sprite(all_sprites, path, x, y, SIZE, colorkey=None):
    sprite = pygame.sprite.Sprite(all_sprites)
    sprite.image = pygame.transform.scale(load_image(path, colorkey), SIZE)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y


class Player:
    def __init__(self, name, past_time, time_impact):
        self.name = name
        self.hp = 10
        self.past_time = past_time
        self.time_impact = time_impact

    def damage(self):
        self.hp -= 1


class Fight:
    def __init__(self, screen, hero_name, bad_name):
        self.screen = screen
        self.hero = Player(hero_name, 0, 1)
        self.bad = Player(bad_name, time.time(), 2)
        self.running = True
        self.result = ''

    def load_all_sprites(self, all_sprites):
        load_sprite(all_sprites, 'fight/background', 0, 0, (660, 660))
        load_sprite(all_sprites, f'fight/{self.hero.name}', 100, 350, (200, 200))
        load_sprite(all_sprites, f'fight/{self.bad.name}', 400, 350, (200, 200), -1)
        load_sprite(all_sprites, f'fight/left_hp_{self.hero.hp}', 0, 0, (250, 40))
        load_sprite(all_sprites, f'fight/right_hp_{self.bad.hp}', 410, 0, (250, 40))
        load_sprite(all_sprites, 'fight/right_button_0', 150, 560, (60, 60), -1)

    def hero_damage(self, all_sprites):
        if time.time() - self.hero.past_time < 0.7:
            load_sprite(all_sprites, 'fight/right_button_1', 150, 560, (60, 60), -1)
            load_sprite(all_sprites, 'fight/boom', 450, 350, (100, 100))

    def bad_damdage(self, all_sprites):
        if time.time() - self.bad.past_time < 0.7:
            load_sprite(all_sprites, 'fight/boom', 170, 350, (100, 100))

    def render(self):
        all_sprites = pygame.sprite.Group()

        self.load_all_sprites(all_sprites)
        self.hero_damage(all_sprites)
        self.bad_damdage(all_sprites)

        all_sprites.draw(self.screen)

    def players_impact(self, player):
        if player == 'bad':
            if time.time() - self.bad.past_time >= self.bad.time_impact:
                self.bad.past_time = time.time()
                self.hero.damage()
                if self.hero.hp == 0:
                    self.game_end('bad')
        else:
            if time.time() - self.hero.past_time >= self.hero.time_impact:
                self.hero.past_time = time.time()
                self.bad.damage()
                if self.bad.hp == 0:
                    self.game_end('hero')

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.render()
            pygame.display.flip()

            self.players_impact('bad')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                keys_event = pygame.key.get_pressed()
                if keys_event[pygame.K_RIGHT]:
                    self.players_impact('hero')

        return self.result

    def game_end(self, result):
        self.result = result
        self.running = False
        self.screen.fill((0, 0, 0))
        self.render()
        pygame.display.flip()

        all_sprites = pygame.sprite.Group()
        if result == 'hero':
            load_sprite(all_sprites, 'fight/win', 0, 0, (660, 660), -1)
        else:
            load_sprite(all_sprites, 'fight/lost', 0, 0, (660, 660), -1)

        all_sprites.draw(self.screen)
        pygame.display.flip()
        time.sleep(3)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Textorcist')
    print(Fight(pygame.display.set_mode((660, 660)), 'hero', 'bad_1'))
