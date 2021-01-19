import pygame
import os
import sys


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


class PopUpWindow:
    def __init__(self, screen, text):
        self.screen = screen
        self.text = text.split('\n')
        self.running = True
        self.run()

    def render(self):
        all_sprites = pygame.sprite.Group()
        load_sprite(all_sprites, 'pop_up_window', 190, 280, (280, 100))
        all_sprites.draw(self.screen)

        f1 = pygame.font.Font(None, 20)

        if len(self.text) > 1:
            text1 = f1.render(self.text[0], True, (180, 0, 0))
            self.screen.blit(text1, (200, 315))
            text2 = f1.render(self.text[1], True, (180, 0, 0))
            self.screen.blit(text2, (200, 345))
        else:
            text1 = f1.render(self.text[0], True, (180, 0, 0))
            self.screen.blit(text1, (200, 330))

    def run(self):
        pygame.font.init()
        while self.running:
            self.render()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False
