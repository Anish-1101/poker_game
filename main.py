from hand import *
from cards import *
from settings import *
import ctypes, pygame, sys
from tests.test_eval_hand import *
from tests.hand_ranking_speed import *

if sys.platform == "win32":
  ctypes.windll.user32.SetProcessDPIAware()

class Money():
   def __init__(self):
      self.player_money = 2500
      self.dealer_money = 2500
      self.pot = 0

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

class FoldButton():
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
  
class RaiseButton():
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

class RaisePercentageButton():
    def __init__(self, x, y, width, height, raise_percentage, font, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.raise_percentage = raise_percentage
        self.text = f"{raise_percentage}%"
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

    def get_raise_amount(self, current_money):
        return int(current_money * (self.raise_percentage / 100))



class Game:
  def __init__(self):

    # General setup
    pygame.init()
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE_STRING)
    self.clock = pygame.time.Clock()
    self.hand = Hand()
    self.check_counter = 0
    self.money = Money()
    self.display_winner = False
    self.raise_buttons_active = False  

    # check button
    button_font = pygame.font.Font(GAME_FONT, 30)
    # CODE CLEAN - use same button class for check, reset, fold and raise button
    self.check_button = CheckButton(250, 20, 200, 80, "Check", button_font, (0, 255, 0), (255, 255, 255))
    self.reset_button = ResetButton(500, 20, 200, 80, "New Hand", button_font, (0, 255, 0), (255, 255, 255))
    self.fold_button = FoldButton(750, 20, 200, 80, "Fold", button_font, (0, 255, 0), (255, 255, 255))
    self.raise_button = RaiseButton(1000, 20, 200, 80, "Raise", button_font, (0, 255, 0), (255, 255, 255))
    self.raise_10_button = RaisePercentageButton(850, 120, 80, 40, 10, pygame.font.SysFont(None, 30), (0, 255, 0), (255, 255, 255))
    self.raise_25_button = RaisePercentageButton(950, 120, 80, 40, 25, pygame.font.SysFont(None, 30), (0, 255, 0), (255, 255, 255))
    self.raise_50_button = RaisePercentageButton(1050, 120, 80, 40, 50, pygame.font.SysFont(None, 30), (0, 255, 0), (255, 255, 255))
    self.raise_75_button = RaisePercentageButton(1150, 120, 80, 40, 75, pygame.font.SysFont(None, 30), (0, 255, 0), (255, 255, 255))
    self.raise_100_button = RaisePercentageButton(1250, 120, 80, 40, 100, pygame.font.SysFont(None, 30), (0, 255, 0), (255, 255, 255))

    self.mouse_down = False

  def display_winner_text(self, screen):
    coordinates = (520, 100)
    text = "Player 2 Wins!"
    text_color = (135, 206, 235)  # Light blue
    self.font = pygame.font.Font(GAME_FONT, 120)
    self.win_rotation_angle = random.uniform(-10, 10)
    text_surface = self.font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = coordinates
    screen.blit(text_surface, text_rect)

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
      self.fold_button.render(self.screen)
      self.raise_button.render(self.screen)
      self.display_money(self.screen, self.money.dealer_money, pygame.font.Font(GAME_FONT, 60), 0)
      self.display_money(self.screen, self.money.player_money, pygame.font.Font(GAME_FONT, 60), 1)
      self.display_money(self.screen, self.money.pot, pygame.font.Font(GAME_FONT, 60), 2)
      self.hand.update()
      self.clock.tick(FPS)

      if self.display_winner:
         self.display_winner_text(self.screen)

      if self.raise_buttons_active:
         self.raise_10_button.render(self.screen)
         self.raise_25_button.render(self.screen)
         self.raise_50_button.render(self.screen)
         self.raise_75_button.render(self.screen)
         self.raise_100_button.render(self.screen)

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
              self.hand.dealer.player_checked = True
              print("Check button clicked!")
              self.raise_buttons_active = False
            if self.check_counter == 2:
              self.hand.dealer.can_deal_turn = True
              print("Check button clicked!")
            if self.check_counter == 3:
              self.hand.dealer.can_deal_river = True
              print("Check button clicked!")

          if self.reset_button.is_clicked(event.pos):
             self.hand = Hand()
             self.display_winner = False
             self.check_counter = 0

          if self.fold_button.is_clicked(event.pos):
             self.display_winner = True      

          if self.raise_button.is_clicked(event.pos):
             self.raise_buttons_active = True

          if self.raise_10_button.is_clicked(event.pos):
             self.money.pot += (self.money.player_money *0.1)
             self.money.player_money = (self.money.player_money * 0.9)

          if self.raise_25_button.is_clicked(event.pos):
             self.money.pot += (self.money.player_money *0.1)
             self.money.player_money = (self.money.player_money * 0.9)
            
          if self.raise_25_button.is_clicked(event.pos):
             self.money.pot += (self.money.player_money *0.25)
             self.money.player_money = (self.money.player_money * 0.75)
          
          if self.raise_50_button.is_clicked(event.pos):
             self.money.pot += (self.money.player_money *0.50)
             self.money.player_money = (self.money.player_money * 0.50)
          
          if self.raise_75_button.is_clicked(event.pos):
             self.money.pot += (self.money.player_money *0.75)
             self.money.player_money = (self.money.player_money * 0.25)
          
          if self.raise_75_button.is_clicked(event.pos):
             self.money.pot += (self.money.player_money)
             self.money.player_money = 0
          

      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:  
          if self.mouse_down:
            self.mouse_down = False

  def display_money(self, screen, money, font, is_dealer):
    if is_dealer == 0:
      money_text = font.render(f"Dealer Money: ${money}", True, (255, 255, 255))
      screen.blit(money_text, (1400, 730)) 
    elif is_dealer == 1:
       money_text = font.render(f"Your Money: ${money}", True, (255, 255, 255))
       screen.blit(money_text, (10, 730)) 
    else:
       money_text = font.render(f"The Pot: ${money}", True, (255, 255, 255))
       screen.blit(money_text, (690, 250))



if __name__ == '__main__':
      game = Game()
      game.run()