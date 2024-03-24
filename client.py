import pickle
import pygame
import sys
pygame.font.init()
from network import Network

pygame.init()
class Button:
    def __init__(self, text, position):
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.width = 150
        self.height = 50
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], self.width, self.height)
        self.color = (0, 128, 255)
        self.highlight_color = (0, 200, 255)
        self.is_hovered = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.highlight_color if self.is_hovered else self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

n=Network()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Client")
screen.fill((255,255,255))


button_1 = Button("1", (300, 200))
button_2 = Button("2",(300,200))
bts=[button_1,button_2]

playerStatus=[False,False,False,False]
print(all(playerStatus))


def redraw(screen):
    screen.fill((255,255,255))
    
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render("Prompts", 1, (0, 255,255))
    screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/18 - text.get_height()/18))


def displayWaiting():
        screen.fill((255,255,255))
        font = pygame.font.SysFont("comicsans",50)
        text=font.render("Waiting for Players",1,(255,0,0),True)
        screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/4 - text.get_height()/4))
    
def displayCurrentPrompt():
    current_prompt=n.send("current prompt")
    current_prompt=str(current_prompt)
    font = pygame.font.SysFont("comicsans", 36)
    prompt_text = font.render(current_prompt, True, (0, 0, 0))
    prompt_rect = prompt_text.get_rect(center=(screen_width // 2, 150))
    screen.blit(prompt_text, prompt_rect)

def main():
    run=True
    
    checkStat=False
    try:
        p=n.send("pos")
        print("You are player ",p)
        displayWaiting()
        pygame.display.flip()
    except:
        pass

    while run:
        while checkStat!=True:
            checkStat=n.send("Connect")
            displayWaiting()
            pygame.display.flip()

        
        redraw(screen)
        
        
        displayCurrentPrompt()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            
            elif event.type==pygame.MOUSEMOTION:
                bts[p].check_hover(pygame.mouse.get_pos())

            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if bts[p].rect.collidepoint(event.pos):
                        if p==0:
                            new_prompt=n.send('p1')
                        else:
                            new_prompt=n.send('p2')
        
                        new_prompt=str(new_prompt)
                        font = pygame.font.Font(None, 36)
                        prompt_text = font.render(new_prompt, True, (0, 0, 0))
                        prompt_rect = prompt_text.get_rect(center=(screen_width // 2, 150))
                        screen.blit(prompt_text, prompt_rect)
                        pygame.display.flip()
                redraw(screen)

            bts[p].draw(screen)
            pygame.display.flip()
        
        #checkStat=n.send("Connect")

main()
pygame.quit()
sys.exit()


    