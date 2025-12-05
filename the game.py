import pygame
import random
import sys

money = 100
fuel = 10
ore = 0
day = 1
max_cargo = 10
hp = 100
max_hp = 100
price = 0
fuel_price = 5
state = "main"
message = ""
message_timer = 0

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Trader")
clock = pygame.time.Clock()

try:
    bg = pygame.image.load("5446991.jpg").convert()
    bg = pygame.transform.scale(bg, (1280, 720))
except:
    bg = None

font = pygame.font.Font(None, 32)
bigfont = pygame.font.Font(None, 64)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def draw_text(text, x, y, color=WHITE, fnt=font):
    img = fnt.render(text, True, color)
    screen.blit(img, (x, y))

def draw_hp_bar(x, y, width, height, hp, max_hp):
    ratio = hp / max_hp
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * ratio, height))

def generate_price():
    return random.randint(5, 20)

def random_event():
    global money, fuel, ore, hp
    events = ["scrap","scrap","meteor","meteor","ore1","ore1","ore2","nothing","nothing","nothing"]
    result = random.choice(events)
    if result == "scrap":
        money += 10
        return "Found scrap metal! +10 credits."
    elif result == "meteor":
        fuel -= 1
        hp -= 10
        if fuel < 0: fuel = 0
        if hp < 0: hp = 0
        return "Meteor strike! -1 fuel, -10 HP."
    elif result == "ore1":
        if ore < max_cargo:
            ore += 1
            return "Found small ore container! +1 ore."
        else:
            return "Cargo full."
    elif result == "ore2":
        space = max_cargo - ore
        if space >= 2:
            ore += 2
            return "Found large ore container! +2 ore."
        elif space == 1:
            ore += 1
            return "Cargo almost full — +1 ore."
        else:
            return "Cargo full."
    return "Nothing happened."

def show_message(text, duration=120):
    global message, message_timer, state
    message = text
    message_timer = duration
    state = "message"

price = generate_price()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state == "main":
                if event.key == pygame.K_1:
                    if fuel <= 0:
                        show_message("No fuel! You are stranded.")
                    else:
                        fuel -= 1
                        result = random_event()
                        day += 1
                        show_message("You travelled. " + result)
                elif event.key == pygame.K_2:
                    state = "trade"
                elif event.key == pygame.K_3:
                    if money >= 5:
                        money -= 5
                        hp += 20
                        if hp > max_hp: hp = max_hp
                        show_message("Ship repaired.")
                    else:
                        show_message("Not enough credits.")
                elif event.key == pygame.K_4:
                    day += 1
                    show_message("You rested.")
                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif state == "trade":
                if event.key == pygame.K_b:
                    if money >= price and ore < max_cargo:
                        money -= price
                        ore += 1
                        show_message("Bought 1 ore.")
                    else:
                        show_message("Cannot buy.")
                elif event.key == pygame.K_s:
                    if ore > 0:
                        ore -= 1
                        money += price
                        show_message("Sold 1 ore.")
                    else:
                        show_message("No ore to sell.")
                elif event.key == pygame.K_f:
                    if money >= fuel_price:
                        money -= fuel_price
                        fuel += 1
                        show_message("Bought 1 fuel.")
                    else:
                        show_message("Not enough credits for fuel.")
                elif event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    day += 1
                    show_message("You left trading.")

            elif state == "message":
                if event.key == pygame.K_SPACE:
                    message_timer = 0

            elif state == "gameover":
                if event.key == pygame.K_r:
                    money = 100
                    fuel = 10
                    ore = 0
                    hp = max_hp
                    day = 1
                    price = generate_price()
                    state = "main"
                elif event.key == pygame.K_ESCAPE:
                    running = False

    if state == "message":
        if message_timer > 0:
            message_timer -= 1
        else:
            price = generate_price()
            state = "main"

    if hp <= 0 and state != "gameover":
        state = "gameover"
        message = "Your ship was destroyed!"
    if fuel <= 0 and state != "gameover":
        state = "gameover"
        message = "You are stranded!"

    if bg:
        screen.blit(bg, (0, 0))
    else:
        screen.fill((0, 0, 30))

    draw_hp_bar(20, 70, 200, 20, hp, max_hp)

    draw_text(f"Day: {day}", 20, 20, YELLOW, bigfont)
    draw_text(f"Money: {money}", 20, 120)
    draw_text(f"Fuel:  {fuel}", 20, 160)
    draw_text(f"Ore:   {ore}/{max_cargo}", 20, 200)
    draw_text(f"Ore Price: {price}", 20, 240)
    draw_text(f"Fuel Price: {fuel_price}", 20, 280)

    if state == "main":
        draw_text("1 - Travel", 450, 150)
        draw_text("2 - Trade", 450, 190)
        draw_text("3 - Repair (5 credits)", 450, 230)
        draw_text("4 - Rest", 450, 270)
        draw_text("ESC - Quit", 450, 310)

    elif state == "trade":
        draw_text("TRADE MODE", 450, 100, YELLOW, bigfont)
        draw_text(f"Ore Price: {price}", 450, 160)
        draw_text(f"b - Buy 1 ore", 450, 220)
        draw_text(f"s - Sell 1 ore", 450, 260)
        draw_text(f"f - Buy 1 fuel ({fuel_price} credits)", 450, 300)
        draw_text("c - Exit trading", 450, 340)

    elif state == "message":
        draw_text("EVENT:", 450, 100, YELLOW, bigfont)
        draw_text(message, 450, 160)
        draw_text("SPACE to continue", 450, 240, GRAY)

    elif state == "gameover":
        final_score = money + (ore * price)
        draw_text("GAME OVER", 450, 100, YELLOW, bigfont)
        draw_text(message, 450, 160)
        draw_text(f"Days Survived: {day}", 450, 200)
        draw_text(f"Final Money: {money}", 450, 240)
        draw_text(f"Final Ore: {ore}", 450, 280)
        draw_text(f"Final Price: {price}", 450, 320)
        draw_text(f"Total Score: {final_score}", 450, 360, YELLOW)
        draw_text("R - Restart | ESC - Quit", 450, 400, GRAY)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
