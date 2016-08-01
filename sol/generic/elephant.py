# an elephant to cross the screen
# the library pygame was chosen for its support for so-called sprites.
# See: http://www.101computing.net/creating-sprites-using-pygame/

# unfortunately, the module pygame is not yet available for Python3
# if we cannot load this module, we must call the program with Python2

try:
    import pygame
except:
    import sys, os
    os.system("/usr/bin/python2 " + sys.argv[0])
    
WHITE = (255, 255, 255)
 
class Elephant(pygame.sprite.Sprite):
    #This class represents an elephant.
    # It derives from the "Sprite" class in Pygame.
    #
    # The original example in
    # http://www.101computing.net/creating-sprites-using-pygame/
    # features a car.
    
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Pass in the color of the elephant, and its x and y position,
        # width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
 
        self.image = pygame.image.load("elephant.png").convert_alpha()
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def moveRight(self, pixels):
        self.rect.x += pixels

pygame.init()
SCREENWIDTH=1200
SCREENHEIGHT=700
 
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("an elephant")

all_sprites_list = pygame.sprite.Group()

el = Elephant(WHITE, 220,200)
el.rect.x = -160
el.rect.y = 100

all_sprites_list.add(el)

carryOn = True
clock=pygame.time.Clock()
 
while carryOn:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            carryOn=False
        
    el.moveRight(1)
    if el.rect.x > SCREENWIDTH:
        carryOn=False
    
    #Game Logic
    all_sprites_list.update()

    #Drawing on Screen
    screen.fill(WHITE)
    #Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
    all_sprites_list.draw(screen)

    #Refresh Screen
    pygame.display.flip()

    #Number of frames per secong e.g. 60
    clock.tick(60)
 
pygame.quit()


