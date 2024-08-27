from hand import *
from cards import *
from settings import *
import ctypes, pygame, sys
from tests.test_eval_hand import *
from tests.hand_ranking_speed import *

if sys.platform == "win32":
  ctypes.windll.user32.SetProcessDPIAware()

class CheckButton():
  def __init__(self, x, y, width, height, text, font, color, text_color):
      self.rect = pygame.Rect(x, y, width, height)
      self.text = text
      self.font = font
      self.color = color
      self.text_color = text_color

  def render(self, surface):
      pygame.draw.rect(surface, self.color, self.rect)
      text_surface = self.font.render(self.text, True, self.text_color)
      text_rect = text_surface.get_rect(center=self.rect.center)
      surface.blit(text_surface, text_rect)

  def is_clicked(self, pos):
      return self.rect.collidepoint(pos)
  
class ResetButton():
  def __init__(self, x, y, width, height, text, font, color, text_color):
      self.rect = pygame.Rect(x, y, width, height)
      self.text = text
      self.font = font
      self.color = color
      self.text_color = text_color

  def render(self, surface):
      pygame.draw.rect(surface, self.color, self.rect)
      text_surface = self.font.render(self.text, True, self.text_color)
      text_rect = text_surface.get_rect(center=self.rect.center)
      surface.blit(text_surface, text_rect)

  def is_clicked(self, pos):
      return self.rect.collidepoint(pos)

class Game:
  def __init__(self):

    # General setup
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE_STRING)
    self.clock = pygame.time.Clock()
    self.hand = Hand()
    self.check_counter = 0

    # check button
    button_font = pygame.font.Font(GAME_FONT, 60)
    self.check_button = CheckButton(100, 200, 200, 80, "Check", button_font, (0, 255, 0), (255, 255, 255))
    self.reset_button = ResetButton(100, 100, 200, 80, "Reset", button_font, (0, 255, 0), (255, 255, 255))
    self.mouse_down = False

  def run(self):
    self.start_time = pygame.time.get_ticks()

    while True:
      self.handle_events()
      # Time variables
      self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
      self.start_time = pygame.time.get_ticks()
      pygame.display.update()
      self.screen.fill(BG_COLOR)
      self.check_button.render(self.screen)
      self.reset_button.render(self.screen)
      self.display_money(self.screen, self.hand.dealer.money, pygame.font.Font(GAME_FONT, 60), True)
      self.display_money(self.screen, self.hand.money, pygame.font.Font(GAME_FONT, 60), False)
      self.hand.update()
      self.clock.tick(FPS)

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  
          self.mouse_down = True
          if self.check_button.is_clicked(event.pos):
            self.check_counter += 1

            if self.check_counter == 1:
              self.hand.dealer.checked = True
              print("Check button clicked!")
            if self.check_counter == 2:
              self.hand.dealer.can_deal_turn = True
              print("Check button clicked!")
            if self.check_counter == 3:
              self.hand.dealer.can_deal_river = True
              print("Check button clicked!")

          if self.reset_button.is_clicked(event.pos):
             self.hand = Hand()
             self.check_counter = 0

      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  
          if self.mouse_down:
            self.mouse_down = False

  def display_money(self, screen, money, font, is_dealer):
    if is_dealer:
      money_text = font.render(f"Dealer Money: ${money}", True, (255, 255, 255))
      screen.blit(money_text, (1400, 730)) 
    else:
       money_text = font.render(f"Your Money: ${money}", True, (255, 255, 255))
       screen.blit(money_text, (10, 730)) 



if __name__ == '__main__':
      game = Game()
      game.run()