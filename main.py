import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bet Against Yourself")

BACKGROUND_COLOR = (40, 44, 52) 
TEXT_COLOR = (248, 248, 242)  
KEYWORD_COLOR = (98, 174, 239) 
STRING_COLOR = (152, 195, 121)  
COMMENT_COLOR = (105, 112, 126)  
BUTTON_HOVER_COLOR = (68, 71, 90)  
BUTTON_COLOR = (50, 54, 61) 
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
YELLOW_COLOR = (255, 255, 0)


main_font = pygame.font.Font(pygame.font.match_font("courier", bold=True), 36)
sub_font = pygame.font.Font(pygame.font.match_font("courier", bold=True), 24)
button_font = pygame.font.Font(pygame.font.match_font("courier", bold=True), 18)

player_resources = {"wealth": 100, "health": 100, "integrity": 100}
ai_behavior = {"risk_tolerance": 0.5, "mode": "neutral"}
game_running = True
message = "Place your bets!"
particles = []
bonus_active = False
bonus_message = ""
visual_state = {"slots": ["-", "-", "-"], "roulette": "-", "coin": "-"}

# Function to draw text with a specific color
def draw_text(text, x, y, font, color=TEXT_COLOR):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Particle Effect
def create_particles(x, y, color):
    for _ in range(20):
        particles.append({
            "pos": [x, y],
            "vel": [random.uniform(-2, 2), random.uniform(-2, 2)],
            "radius": random.randint(3, 6),
            "color": color,
            "lifetime": 50
        })

def update_particles():
    for particle in particles[:]:
        particle["pos"][0] += particle["vel"][0]
        particle["pos"][1] += particle["vel"][1]
        particle["lifetime"] -= 1
        particle["radius"] = max(0, particle["radius"] - 0.1)
        pygame.draw.circle(screen, particle["color"], (int(particle["pos"][0]), int(particle["pos"][1])), int(particle["radius"]))
        if particle["lifetime"] <= 0:
            particles.remove(particle)

# Draw Button and Detect Clicks
def draw_button(x, y, width, height, text, text_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Change button color on hover
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))

    # Draw button text
    draw_text(text, x + 10, y + 10, button_font, text_color)

# AI Behavior Adjustment
def adjust_ai_behavior():
    global ai_behavior
    if player_resources["wealth"] > 150:
        ai_behavior["mode"] = "greedy"
        ai_behavior["risk_tolerance"] = 0.8
    elif player_resources["wealth"] < 50:
        ai_behavior["mode"] = "cautious"
        ai_behavior["risk_tolerance"] = 0.2
    else:
        ai_behavior["mode"] = "neutral"
        ai_behavior["risk_tolerance"] = 0.5

# Mini-Games
def roulette(bet):
    global message
    adjust_ai_behavior()
    result = random.choice(["Red", "Black", "Green"])
    visual_state["roulette"] = result
    player_guess = random.choice(["Red", "Black", "Green"])
    ai_bet = int(bet * ai_behavior["risk_tolerance"] * random.uniform(1, 2))
    if player_guess == result:
        player_resources["wealth"] += ai_bet
        message = f"Roulette: Guessed {player_guess}, spun {result}. Won {ai_bet}!"
        create_particles(WIDTH // 2, HEIGHT // 2, STRING_COLOR)
    else:
        player_resources["wealth"] -= bet
        player_resources["health"] -= 1
        player_resources["integrity"]-=1
        message = f"Roulette: Guessed {player_guess}, spun {result}. Lost {bet}!"

def slot_machine(bet):
    global message
    adjust_ai_behavior()
    slots = [random.choice(["Cherry", "Bell", "7"]) for _ in range(3)]
    visual_state["slots"] = slots
    ai_bet = int(bet * ai_behavior["risk_tolerance"] * random.uniform(1, 2))
    if len(set(slots)) == 1:
        winnings = bet * 5
        player_resources["wealth"] += winnings
        message = f"Slot Machine: {slots}. WIN!"
        create_particles(WIDTH // 2, HEIGHT // 2, KEYWORD_COLOR)
    else:
        player_resources["wealth"] -= bet
        player_resources["health"] -= 1
        player_resources["integrity"] -=1
        message = f"Slot Machine: {slots}. Lost {bet}!"

def coin_flip(bet):
    global message
    adjust_ai_behavior()
    result = random.choice(["Heads", "Tails"])
    visual_state["coin"] = result
    player_guess = random.choice(["Heads", "Tails"])
    ai_bet = int(bet * ai_behavior["risk_tolerance"] * random.uniform(1, 2))
    if player_guess == result:
        player_resources["wealth"] += ai_bet
        message = f"Coin Flip: Guessed {player_guess}, flipped {result}. Won!"
        create_particles(WIDTH // 2, HEIGHT // 2, COMMENT_COLOR)
    else:
        player_resources["wealth"] -= bet
        player_resources["integrity"] -= 1
        player_resources["health"] -= 1
        message = f"Coin Flip: Guessed {player_guess}, flipped {result}. Lost {bet}!"

# Draw Visual Components
def draw_visuals():
    # Slot Machine Visuals
    slot_x = 100
    slot_y = 400
    slot_width = 80
    slot_height = 60
    for i, symbol in enumerate(visual_state["slots"]):
        pygame.draw.rect(screen, YELLOW_COLOR, (slot_x - 10 + i * (slot_width + 10), slot_y, slot_width, slot_height))
        draw_text(symbol, slot_x + i * (slot_width + 10) - 10, slot_y + 10, button_font, BLACK_COLOR)

    # Roulette Visual
    draw_text(f"Roulette: {visual_state['roulette']}", 450, 400, sub_font, RED_COLOR if visual_state["roulette"] == "Red" else GREEN_COLOR if visual_state["roulette"] == "Green" else BLACK_COLOR)

    # Coin Flip Visual
    draw_text(f"Coin Flip: {visual_state['coin']}", 450, 450, sub_font, COMMENT_COLOR)

# Main Game Loop
clock = pygame.time.Clock()
while game_running:
    screen.fill(BACKGROUND_COLOR)
    update_particles()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Draw Buttons
    draw_button(50, 300, 200, 50, "Roulette(Bet 10)", KEYWORD_COLOR, lambda: roulette(10))
    draw_button(300, 300, 200, 50, "Slots(Bet 20)", STRING_COLOR, lambda: slot_machine(20))
    draw_button(550, 300, 200, 50, "Coin Flip(Bet 50)", COMMENT_COLOR, lambda: coin_flip(50))

    # Draw Game Interface
    draw_text("BET AGAINST YOURSELF", 20, 20, main_font, KEYWORD_COLOR)
    draw_text(f"Wealth: {player_resources['wealth']}", 20, 100, sub_font, STRING_COLOR)
    draw_text(f"Health: {player_resources['health']}", 20, 150, sub_font, COMMENT_COLOR)
    draw_text(f"Integrity: {player_resources['integrity']}", 20, 200, sub_font, KEYWORD_COLOR)
    draw_text(f"AI Behavior: {ai_behavior['mode']}", 20, 250, sub_font, TEXT_COLOR)

    # Draw Visual Components
    draw_visuals()

    draw_text(message, 20, 550, button_font, TEXT_COLOR)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
