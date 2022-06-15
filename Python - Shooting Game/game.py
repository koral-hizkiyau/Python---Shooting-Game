import math

import time
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# colors
RED = (255,0,0)
YELLOW = (251,254,51)

# background img
background = pygame.image.load('pictures/background.png')

# ball size
BALL_SIZE = 25


# life
lifeImg = pygame.image.load('pictures/life.png')
lifeX = 10
lifeY = 550
sumLife = 3

life_list = []


# function:: create life on screen
def life(x,y):
    screen.blit(lifeImg, (lifeX, lifeY))
    
    

# player
playerImg = pygame.image.load('pictures/enemy.png')
playerX = 370
playerY = 468
playerX_change = 0



# enemy
enemyX_size = 200
enemyY_size = 200
enemyImg = pygame.image.load('pictures/monster.png')
enemyImg = pygame.transform.scale(enemyImg, (enemyX_size, enemyY_size))
enemyX = 50
enemyY = 50
enemy_change = 4



# create plater on screen
def player(x, y):
    screen.blit(playerImg, (x, y))

    

# create enemy on screen
def enemy(x, y):
    screen.blit(enemyImg, (x, y))



# Ball class
class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0



# create ball on screen
def make_ball(x=400, y=50):
    ball = Ball()
    # מאיפה הכדור יתחיל להיות מוצג על המסך
    ball.x = x
    ball.y = y

    # מהירות הכדור
    ball.change_x = 2
    ball.change_y = 2
    return ball



# -----> איתחול התחלתי של הכדור הראשון במשחק
# יוצר כדור דרך הפונקציה (שמחזירה כדור)
ball = make_ball()

# מערך של כדורים
ball_list = []
ball_list.append(ball)




# bullet
bulletImg = pygame.image.load('pictures/bullet.png')
bulletX = -100
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready" #בסטטוס רדי לא רואים את הכדור על המסך, בסטטוס אש רואים

# קריאה לפונקציה בלחיצה על מקש רווח יוצא כדור
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10)) #כדי שהכדור יצא בדיוק ממרכז השחקן

    

# פונקציה שבודקת אם יש התנגשות בין שני אלמנטים במשחק
#-- בין הכדור לירייה
def isCollision(ballX, ballY, bulletX, bulletY):
    # חישוב מרחק בין 2 נקודות על פי נוסחה, בעזרת ספרייה מאט
    distance = math.sqrt(math.pow(ballX - bulletX, 2) + (math.pow(ballY - bulletY, 2)))-20
    if distance < 30:
        return True
    else:
        return False

#פונקציה שבודקת התנגשות בשלב האחרון בין המפלצת לירי
def isCollisionMonster(ballX, ballY, bulletX, bulletY, sizeMonster):
    # חישוב מרחק בין 2 נקודות על פי נוסחה, בעזרת ספרייה מאט
    distance = math.sqrt(math.pow(ballX - bulletX, 2) + (math.pow(ballY - bulletY, 2)))-20
    distance2 = math.sqrt(math.pow(ballX - (bulletX+sizeMonster), 2) + (math.pow(ballY - bulletY, 2)))-20
    if distance < 30 or distance2 < 30:
        return True
    else:
        return False

    

# פונקציה שבודקת אם יש התנגשות בין השחקן לכדורים
def isCollisionLife(ballX, ballY, playerX, playerY):
    # חישוב מרחק בין 2 נקודות על פי נוסחה, בעזרת ספרייה מאט
    distance = math.sqrt(math.pow(ballX - playerX, 2) + (math.pow(ballY - playerY, 2)))-15  
    distance2 = math.sqrt(math.pow(ballX - (playerX+30), 2) + (math.pow(ballY - playerY, 2)))-15  
    if distance < 3 or distance2 < 10:    #10
        return True
    else:
        return False
    

clock = pygame.time.Clock()

# משתני עזר
level_state = False
level = 1

#כמות החיים של המפלצת בשלב 3
level_4_score = 3

# איתחול פונט
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Sound
mixer.music.load("sound/background.wav")
mixer.music.play(-1)





# -----------------------------------> START GAME LOOP <-----------------------------
running = True
while running:

   
    #  set background color
    screen.fill((0, 0, 0))
    #  set background img
    screen.blit(background, (0, 0))
    
    # לאפס את ציר האיקס של החיים שלא יזוזו
    lifeX = 10

    
  
     # ---- screen text - level/game over/won ----
    if level != 4 and level != 5:
        level_text = over_font.render("LEVEL "+str(level), True, (255, 255, 255))
        screen.blit(level_text, (275, 250))
    if level == 4:
        level_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(level_text, (210, 250))
    if level == 5:
        level_text = over_font.render("You Won!", True, (255, 255, 255))
        screen.blit(level_text, (275, 250))
    # ---- end screen text ----
        
        
        
    # ------- keyboard loop -----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #  אם נלחץ מקש בדוק אם ימין או שמאל
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("sound/laser.wav")
                    bulletSound.play()
                    #מעדן את יציאת הירייה למיקום השחקן
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # אם לא נלחץ מקש אל תזיז את השחקן
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # ------- end keyboard loop -----------

    

    # ------ ball move logic (ball_list) ------
    for i in range(len(ball_list)):
        if len(ball_list) > 1 and i == 0 and level_state == False:
           ball_list[i].x -= ball_list[i].change_x
           ball_list[i].y += ball_list[i].change_y
        else:
           ball_list[i].x += ball_list[i].change_x
           ball_list[i].y += ball_list[i].change_y

        # במידה והכדור נתקע בצדדים
        if ball_list[i].y > 600 - BALL_SIZE -75 or ball_list[i].y < BALL_SIZE:
           ball_list[i].change_y *= -1
        if ball_list[i].x > 800 - BALL_SIZE or ball_list[i].x < BALL_SIZE:
           ball_list[i].change_x *= -1
    # -------  end ball move logic -----------




    # -------- shooting logic ---------
    #  תנאי שדואג שניתן יהיה לאורך המשחק לשלוח יותר מירייה אחת
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # אם נלחץ מקש ספייס תירה את הירייה למעלה
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    # -------- end shooting logic ---------



    # ---------- if collision --------------
    # ---------- בין הכדור לירייה--
    for i in range(len(ball_list)):
        collision = isCollision(ball_list[i].x, ball_list[i].y, bulletX, bulletY)
        if collision:
           explosionSound = mixer.Sound("sound/explosion.wav")
           explosionSound.play()
           bulletY = 480
           # כדי שהכדור החדש לא ימחק
           bulletX = -100
           bullet_state = "ready"
           if len(ball_list) > 1 or level_state == True:
              del(ball_list[i])
              level_state = True
              break
           else:
              ball_list[0] = make_ball(ball_list[0].x, ball_list[0].y)
              ball_list.append(make_ball(ball_list[0].x, ball_list[0].y))
              BALL_SIZE = 15
              break
    # ---------- end if collision --------------

    

    # ------ just for level 2--------
    if len(ball_list) < 1 and level == 1:
        level = 2
        # יוצר כדורים עבור שלב 2
        for i in range(5):
            ball_list.append(make_ball(50*(i+2),50*(i+2)))
    # ------ end just for level 2--------

    

            
    # --------------- level 3 enemy ------------------
    if len(ball_list) < 1 and level ==2 or level ==3:
        level = 3
        enemy(enemyX, enemyY)
        #תזוזת מפלצת
        enemyX += enemy_change
        if enemyX <= 0:
           enemyY += 35
           enemy_change *= -1
        elif enemyX >= 610: # לחשב מדוייק גודל מפלצת
           enemyY += 35
           enemy_change *= -1
    

        collision = isCollisionMonster(enemyX, enemyY, bulletX-20, bulletY-20, enemyX_size)
        if collision:
            level_4_score -= 1
            if level_4_score == 0:
                level = 5
            bulletY = 480
           # הכדור מאותחל ל100- כדי שהכדדורים לא יפגעו בו ויתפוצצו
            bulletX = -100
            bullet_state = "ready"
            enemyX_size -= 20
            enemyY_size -= 20
            enemyImg = pygame.transform.scale(enemyImg, (enemyX_size, enemyY_size))
        if isCollisionLife(enemyX, enemyY, playerX-130, playerY-130):
            ouchSound = mixer.Sound("sound/ouch.wav") #change sound
            ouchSound.play()
            sumLife -=1
            if sumLife == 0:
                level = 4
            else:
                enemyX = 50
                enemyY = 50
                time.sleep(2)
     # --------------- end level 3 enemy ------------------


            
  
    # ------- אם הכדור פוגע בשחקן --------------
    # תשמיע צלילים ותוריד חיים
    # במידה ויש חיים תעצור ל2 שניות ותעלה את הכדור בחזרה למעלה
    # במידה ואין חיים תעביר לשלב 4- המשחק נגמר
    for ball in ball_list:
        if isCollisionLife(ball.x, ball.y, playerX, playerY):
            ouchSound = mixer.Sound("sound/ouch.wav") #change sound
            ouchSound.play()
            sumLife -=1
            if sumLife == 0:
                level = 4
            else:
                ball.x = 400
                ball.y = 50
                time.sleep(2)
    # --------------- end אם הכדור פוגע בשחקן ------------------
 

    # ------ player move ---------
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # ------ end player move ---------



    # ----- creare player on screen ------
    player(playerX, playerY)
    
    # ----- create ball on screen by ball_list--
    if level != 4:
       for ball in ball_list:
           pygame.draw.circle(screen, YELLOW, [ball.x, ball.y], BALL_SIZE)
           
    # ------ create life on screen --------
    for i in range(sumLife):
        life(lifeX, lifeY)
        lifeX+=40

        
    clock.tick(60)
   
    pygame.display.update()
pygame.quit() 
