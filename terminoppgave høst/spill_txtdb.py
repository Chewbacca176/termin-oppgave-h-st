import random 
import pygame as pg

pg.init()

WIDTH = 1200
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0, 255)
SPEED = 10

FPS = 30

timer = 0
score = 0

bg = pg.image.load("space3.jpeg")
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("You know when the")

heart_img = pg.image.load("heart.png")
heart_img = pg.transform.scale(heart_img, (40, 40))

start_button = pg.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
start_ny = pg.Rect(WIDTH // 2  - 125, HEIGHT // 2 + 150, 250, 100)

HighScore = []
fil = "score.txt"


def HentScore(filnavn):
    with open(filnavn, 'r') as fil:
        for linje in fil:
            for ord in linje.split():
                HighScore.append(int(ord))

def skriv_til_fil(filnavn):
    with open(filnavn, 'w') as txt_file:
        for line in HighScore:
            txt_file.write(str(line) + '\n')

class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pg.image.load("crab.png")
        self.image = pg.transform.scale(self.image, (59, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]
        self.lives = 5

    def update(self):
        key = pg.key.get_pressed()
        x = ((key[pg.K_d] - key[pg.K_a]) * SPEED)
        y = ((key[pg.K_s] - key[pg.K_w]) * SPEED)
        self.rect.move_ip(x,y)
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

class Hit_box(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pg.Surface((44,22), pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = [player.rect.x, player.rect.y]
    
    def update(self):
        hit_box.rect.topleft = (player.rect.x + 11, player.rect.y + 9)

class Astroide(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load("astroide.png")
        self.image = pg.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 8
        self.direction = pg.Vector2(player.rect.x - x, player.rect.y - y).normalize()

    def update(self):
        self.rect.move_ip(self.direction * self.speed)  

        if (self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            all_sprites.remove(self)
            if self in astroider:
                astroider.remove(self)
            global score
            score += 1

        if self.rect.colliderect(hit_box.rect):
            all_sprites.remove(self)
            if self in astroider:
                astroider.remove(self)
            player.lives -= 1

class EkstraLiv(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pg.image.load("Health-potion.png")
        self.image = pg.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
    
    def update(self):
        if self.rect.colliderect(hit_box.rect):
            all_sprites.remove(self)
            player.lives += 1
    
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

player = Player(600,400)
hit_box = Hit_box(player.rect.x, player.rect.y)
all_sprites = pg.sprite.Group()
all_sprites.add(player, hit_box)

astroider = []
clock = pg.time.Clock()
running = False
game_over = False

HentScore(fil)

while True:
    
    while running == False:
        screen.fill(BLACK)
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    running = True

        pg.draw.rect(screen, GREEN, start_button)
        draw_text("START", pg.font.Font(None, 50), BLACK, screen, WIDTH // 2, HEIGHT // 2)

        pg.display.flip()
        clock.tick(FPS)

    game_over = False 
    while game_over == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        
        h_vegg = [WIDTH, random.randint(0,HEIGHT)]
        v_vegg = [0, random.randint(0,HEIGHT)]
        tak = [random.randint(0,WIDTH), 0]
        gulv = [random.randint(0,WIDTH), HEIGHT]
        vegger = [h_vegg, v_vegg, tak, gulv]
            
        if len(astroider) < 35:
            vegg_valg = vegger[random.randint(0,3)]
            ny_astroide = Astroide(vegg_valg[0], vegg_valg[1])
            astroider.append(ny_astroide)
            all_sprites.add(ny_astroide)
        for i in range(1):
            timer +=1 
            if timer == 200:
                ekstra_liv = EkstraLiv(random.randint(0, WIDTH), random.randint(0, HEIGHT))
                all_sprites.add(ekstra_liv)
                timer = 0

            

        screen.blit(bg,(0,0))
        all_sprites.update()
        all_sprites.draw(screen)
        
        font = pg.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(score_text, (10, 10))

        for i in range(player.lives):
            screen.blit(heart_img, (WIDTH - 50 - i * 50, 10))

        if player.lives <= 0:
            draw_text("GAME OVER", pg.font.Font(None, 100), RED, screen, WIDTH // 2, HEIGHT // 2)
            draw_text(f"Final Score: {score}", pg.font.Font(None, 50), GREEN, screen, WIDTH // 2, HEIGHT // 2 + 100)
            HighScore.append(score)
            HighScore.sort()
            HighScore.reverse()
            draw_text(f"HighScore: {HighScore[0]}", pg.font.Font(None, 50), GREEN, screen, WIDTH // 2, 100)
            skriv_til_fil(fil)
            game_over = True
            while running == True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        mouse_pos = pg.mouse.get_pos()
                        if start_ny.collidepoint(mouse_pos):
                            player.lives = 5
                            score = 0
                            astroider.clear()
                            all_sprites.empty()
                            all_sprites.add(player, hit_box)
                            player.rect.topleft = [600, 400]
                            running = False
                            break
                        
                pg.draw.rect(screen, GREEN, start_ny)
                draw_text("SPILL IGJEN", pg.font.Font(None, 50), BLACK, screen, WIDTH // 2 , HEIGHT // 2 + 200)
                pg.display.flip()
                clock.tick(FPS)
                

        pg.display.flip()
        clock.tick(FPS)



 