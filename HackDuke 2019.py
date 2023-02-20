import pygame
import random
import math

# define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT= 600
WHITE = (255,255,255)
BLACK = (0,0,0)
TRIANGLE_CENTER = (3*SCREEN_WIDTH//4, 535)
STAGNANT_SEED = random.randint(1,100000)

ASTEROID_IMAGES = {
    1: pygame.image.load("asteroid_1.png"),
    2: pygame.image.load("asteroid_2.png"),
    3: pygame.image.load("asteroid_3.png"),
}

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("timesnewroman", 30)

def message_to_screen(msg,color,x,y): # writes text on screen
    textSurf = font.render(msg, True, color)
    screen.blit(textSurf, (x,y))

def create_ship(mouse_pos):
    dx = mouse_pos[0] - TRIANGLE_CENTER[0]
    dy = mouse_pos[1] - TRIANGLE_CENTER[1]
    angle = math.degrees(math.atan2(dy, dx))
        
    mouse_dis = math.sqrt((TRIANGLE_CENTER[0]-mouse_pos[0])**2+(TRIANGLE_CENTER[1]-mouse_pos[1])**2)
    pointer_pos = (TRIANGLE_CENTER[0]-int(20*(TRIANGLE_CENTER[0]-mouse_pos[0])/mouse_dis),TRIANGLE_CENTER[1]-int(20*(TRIANGLE_CENTER[1]-mouse_pos[1])/mouse_dis))
    b_pointer_pos = (TRIANGLE_CENTER[0]+int(7*(TRIANGLE_CENTER[0]-mouse_pos[0])/mouse_dis),TRIANGLE_CENTER[1]+int(7*(TRIANGLE_CENTER[1]-mouse_pos[1])/mouse_dis))
    
    bl_pointer_pos = (int(TRIANGLE_CENTER[0]+20*math.sin(math.radians(angle-30))), int(TRIANGLE_CENTER[1]-20*math.sin(math.radians(120-angle))))
    br_pointer_pos = (int(TRIANGLE_CENTER[0]-20*math.sin(math.radians(30+angle))), int(TRIANGLE_CENTER[1]+20*math.sin(math.radians(60-angle))))
    
    pygame.draw.polygon(screen, WHITE, [pointer_pos, bl_pointer_pos, b_pointer_pos, br_pointer_pos])

def draw_bullet(bullet_pos, mouse_pos, click):
        
    if -100 < bullet_pos[0] < SCREEN_WIDTH+100 and -100 < bullet_pos[1] < SCREEN_HEIGHT+100:
        # draws bullet when rendered
        pygame.draw.circle(screen, WHITE, bullet_pos, 3)
        
        center_dis = math.sqrt((TRIANGLE_CENTER[0]-bullet_pos[0])**2+(TRIANGLE_CENTER[1]-bullet_pos[1])**2)
        bullet_pos = (TRIANGLE_CENTER[0]-int((center_dis+4)*(TRIANGLE_CENTER[0]-bullet_pos[0])/max(center_dis,0.1)),
                      TRIANGLE_CENTER[1]-int((center_dis+4)*(TRIANGLE_CENTER[1]-bullet_pos[1])/max(center_dis,0.1)))

    if click[0]:
        bullet_pos = TRIANGLE_CENTER
        center_dis = math.sqrt((TRIANGLE_CENTER[0]-mouse_pos[0])**2+(TRIANGLE_CENTER[1]-mouse_pos[1])**2)
        bullet_pos = (TRIANGLE_CENTER[0]-int(10*(TRIANGLE_CENTER[0]-mouse_pos[0])/max(center_dis,0.1)),
                      TRIANGLE_CENTER[1]-int(10*(TRIANGLE_CENTER[1]-mouse_pos[1])/max(center_dis,0.1)))
    
    return bullet_pos

def asteroid_hit(bullet_pos, asteroids, score, answer, victory, n):
    if SCREEN_WIDTH//2 < bullet_pos[0] < SCREEN_WIDTH and  bullet_pos[1] < asteroids[0][1]+10:
        closest = 700
        nearest_ast = 0
        for ast in range(len(asteroids)):
            if min(closest,math.sqrt((bullet_pos[0]-asteroids[ast][0])**2+(bullet_pos[1]-asteroids[ast][1])**2)) != closest:
                closest = min(closest,math.sqrt((bullet_pos[0]-asteroids[ast][0])**2+(bullet_pos[1]-asteroids[ast][1])**2))
                nearest_ast = ast
        bullet_pos = (-100, -100)
        if n%10 < 9:
            asteroids = [(TRIANGLE_CENTER[0]-112, -100),(TRIANGLE_CENTER[0]-22, -100),(TRIANGLE_CENTER[0]+68, -100)]
        else:
            asteroids = [(TRIANGLE_CENTER[0]-112, -700),(TRIANGLE_CENTER[0]-22, -700),(TRIANGLE_CENTER[0]+68, -700)]
            
        if chr(nearest_ast+ord("A")) == answer:
            victory = f"HIT! Answer was {answer}"
            score += 10
        else:
            victory = f"Miss... Answer was {answer}"
            score -= 10
        n += 1

    if asteroids[0][1] > TRIANGLE_CENTER[1]:
        bullet_pos = (-100, -100)
        if n%10 < 9:
            asteroids = [(TRIANGLE_CENTER[0]-112, -100),(TRIANGLE_CENTER[0]-22, -100),(TRIANGLE_CENTER[0]+68, -100)]
        else:
            asteroids = [(TRIANGLE_CENTER[0]-112, -700),(TRIANGLE_CENTER[0]-22, -700),(TRIANGLE_CENTER[0]+68, -700)]
            
        victory = f"Miss... Answer was {answer}"
        score -= 10
    
    return bullet_pos, asteroids, score, answer, victory, n

def code_challenge(n):
    random.seed(STAGNANT_SEED+n//10)
    message_to_screen(f"value = 0",WHITE,0,1*45)

    i = random.randint(1,5)
    itr = random.randint(1,5)
    message_to_screen(f"for(int i = {i}; i < {i+10}; i+={itr}) {{",WHITE,10,2*45)

    modX, modY = random.sample([3,4,5,6], 2)
    message_to_screen(f"    if (i%{modX} == 0) {{",WHITE,10,3*45)
    message_to_screen(f"        print('A')",WHITE,10,4*45)
    message_to_screen(f"    else if (i%{modY} == 0) {{",WHITE,10,5*45)
    message_to_screen(f"        print('B')",WHITE,10,6*45)
    message_to_screen(f"    else {{",WHITE,10,7*45)
    message_to_screen(f"        print('C')",WHITE,10,8*45)

    return 'A' if (i+itr*(n%10))%modX == 0 else 'B' if (i+itr*(n%10))%modY == 0 else 'C'
        
def game():
    # game variables
    bullet_pos = (-100,-100)
    asteroids = [(3*SCREEN_WIDTH//4-112, -700), (3*SCREEN_WIDTH//4-22, -700), (3*SCREEN_WIDTH//4+68, -700)]

    score = 0
    n = 0
    victory = ""
    answer = 0
    
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit
                gameExit = True

        # update screen
        screen.fill(BLACK)
        
        mouse_pos = pygame.mouse.get_pos() # mouse position
        click = pygame.mouse.get_pressed() # gets if mouse clicked

        create_ship(mouse_pos)
        bullet_pos = draw_bullet(bullet_pos, mouse_pos, click)

        for astPos in range(len(asteroids)):
            random.seed(astPos+score+n)
            screen.blit(ASTEROID_IMAGES[1], (asteroids[astPos][0]+random.randint(-5,5),asteroids[astPos][1]+random.randint(-5,5)))
            screen.blit(ASTEROID_IMAGES[2], (asteroids[astPos][0]+random.randint(-5,5),asteroids[astPos][1]+random.randint(-5,5)))
            screen.blit(ASTEROID_IMAGES[3], (asteroids[astPos][0]+random.randint(-5,5),asteroids[astPos][1]+random.randint(-5,5)))
            message_to_screen(chr(astPos+ord("A")), BLACK, asteroids[astPos][0]+10, asteroids[astPos][1]+10)

        for ast in range(len(asteroids)):
            asteroids[ast] = (asteroids[ast][0],asteroids[ast][1]+1)

        answer = code_challenge(n)

        bullet_pos, asteroids, score, answer, victory, n = asteroid_hit(bullet_pos, asteroids, score, answer, victory, n)

        message_to_screen(f"SCORE: {score}",WHITE,SCREEN_WIDTH//4,0)
        message_to_screen(victory,WHITE,SCREEN_WIDTH//4,9*45)
        
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
game()
