import pygame


class Button:
    def __init__(self, wdt, hgt, i_color, a_color):
        self.wdt = wdt
        self.hgt = hgt
        self.i_color = i_color
        self.a_color = a_color
        self.font = pygame.font.Font(None, 40)

    def draw(self, x, y, message, scr):
        text_button = self.font.render(message, True, self.i_color)
        pygame.draw.rect(scr, self.a_color, (x, y, self.wdt, self.hgt))
        scr.blit(text_button, (x + 15, y + 10))

    def mouse_click(self, x, y, message, scr):
        text_button_1 = self.font.render(message, True, self.i_color)
        text_button_2 = self.font.render(message, True, ('#003300'))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.wdt:
            if y < mouse[1] < y + self.hgt:
                scr.blit(text_button_2, (x + 15, y + 10))
                if click[0] == 1:
                    return 1
        else:
            scr.blit(text_button_1, (x + 15, y + 10))