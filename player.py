import pygame

# Создаем класс, который взаимствован от класса Sprite внутри pygame
class Player(pygame.sprite.Sprite):

    # Инициализация
    def __init__(self, pos, pid):
        pygame.sprite.Sprite.__init__(self)

        # Загружаем спрайт игрока
        self.image = pygame.image.load("sprites/tank"+str(pid+1)+".png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
