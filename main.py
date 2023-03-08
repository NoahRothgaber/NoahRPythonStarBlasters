# Noah Rothgaber
# A shootem up game utilizing turtle module for graphics
import _tkinter
import gc
import random
import turtle
from threading import Timer

turtle.colormode(255)
# Changes turtle color scheme to utilize rgb
# SPACE BAR IS SHOOT, R IS RELOAD, X ADDS LEVEL (CAREFUL WILL CRASH), ESCAPE PAUSES AND ALLOWS EXIT,
# K GOES TO END SCREEN, USES A AND D FOR MOVEMENT
# Globals
bullet_count = 0  # Represents amount of bullets in memory
bullet_list = []  # Stores bullets in one place
known_xy = []  # List of coordinates for known starting places when the game begins
level = 4  # Starting amount of enemies - 1
level_number = 0  # Displayed Level
enemy_numbers = level  # Enemy counter
enemy_list = list()  # Where enemies are stored when created
hitboxes = dict()  # A dictionary that has the location of the enemy (key) and the enemies reference in memory (value)
score = 0  # Represents Score
player_name = str()  # Placeholder for player name
speed = 1  # Speed changes rate of movement for enemies,helps keep game look consistent when more sprites are loaded
direction = [-2, 2]  # List that program chooses from to determine whether enemy goes left or right
run_amount = 0  # Determines how many times main while loop is executed, helps with garbage collector at eof
end = False  # Tells program if game is over
close_time = bool()  # Bool for quit process
level_write = turtle.Turtle()  # Level writing on top left object
level_write.hideturtle()


# CLASSES
class Polygons(turtle.Turtle):  # Creates a class with each object initiated as a turtle object
    def __init__(self, color, shape):
        super().__init__()
        self.penup()
        self.shape(shape)

        self.color(color)

    hp = 3

    # Enemy function, uses polygon object, edits some default attributes, \
    # moves object to location not already occupied  by any other enemy object,

    def enemy(self):
        self.tilt(30)
        self.shapesize(stretch_len=2, stretch_wid=2)
        while True:
            possible_locations_x = list(range(-260, 260, 50))
            possible_locations_y = list(range(0, 380, 50))
            current_xy = (random.choice(possible_locations_x), (random.choice(possible_locations_y)))
            if known_xy:
                if current_xy not in known_xy:
                    self.goto(current_xy)
                    known_xy.append(current_xy)
                    self.goto(current_xy)
                    return self
                else:
                    continue
            else:
                known_xy.append(current_xy)
                self.goto(current_xy)
                return self

    def bullets(self):  # creates bullet sprite and moves bullet object to barrel of players "gun" (the top corner)
        barrel = player_square.xcor(), player_square.ycor() + 40
        self.shapesize(stretch_len=.75, stretch_wid=.75)
        self.goto(barrel)
        self.showturtle()
        return self

########################################################################################################################
# FUNCTIONS
def window_creation():  # Creates window utilizing provided background image (created by Noah Rothgaber)
    # Window Code
    win = turtle.Screen()
    win.title("Blaster, Star Destroyers")
    win.bgpic("StarBackground.gif")
    global player_name
    win.setup(width=600, height=800)
    # Name Capture Code
    player_name = turtle.textinput("Name for High Score", "What is your name?")
    while player_name == '':  # If player clicks ok with no input
        player_name = turtle.textinput("Name for High Score", "What is your name?")
    if player_name is None:  # If player clicks cancel the game ends
        quit()
    win.tracer(0)  # Window speed
    return win


def end_game():  # This follows through the steps of hiding any objects, and displays top 10 high scores
    global end
    new_highscore()
    end = True
    y_cord = 200
    if enemy_list:
        for item in enemy_list:
            item.hideturtle()
        enemy_list.clear()
    player_square.hideturtle()
    player_square.clear()
    if bullet_list:
        for item in bullet_list:
            item.hideturtle()
        bullet_list.clear()
    list_em = top_ten_highscores()
    template_write = turtle.Turtle()
    template_write.speed(0)
    template_write.color(245, 167, 66)
    template_write.hideturtle()
    template_write.penup()
    template_write.goto(0, 300)
    template_write.write(f'GREAT JOB', font=("Comic Sans MS", 30, "normal"), align="center")
    template_write.color(40, 40, 40)
    template_write.goto(0, y_cord)
    template_write.write(f'Name  |   High Score', font=("Comic Sans MS", 30, "normal"), align="center")
    for i in list_em:
        y_cord = y_cord - 40
        final_write = turtle.Turtle()
        final_write.speed(0)
        final_write.color(0, 220, 100)
        final_write.hideturtle()
        final_write.penup()
        final_write.goto(0, y_cord)
        final_write.write(f'{i[1]}  |   {i[0]}', font=("Comic Sans MS", 30, "normal"), align="center")


def close_game():  # Brings up turtle input screen to verify if user wants to quit, gives option to save
    global close_time
    close = turtle.textinput('Quit?', 'Do you want to quit? (y) or (n)')
    while True:
        if close is None:
            return
        elif close.isalpha():
            if close.lower() == 'y':
                score_save = turtle.textinput('Save?', 'Do you want to save your score? (y) or (n)')
                print(score_save)
                while True:
                    if score_save is None:
                        return
                    elif score_save.isalpha():
                        if score_save.lower() == 'y':
                            new_highscore()
                            close_time = True
                        elif score_save.lower() == 'n':
                            close_time = True
                        else:
                            close = turtle.textinput('Please type y or n',
                                                     'Do you want to save your score? (y) or (n)')
                            continue
                        return
                    else:
                        score_save = turtle.textinput('Please Type y or n',
                                                      'Do you want to save your score? (y) or (n)')
                        continue
            elif close.lower() == 'n':
                return
        else:
            close = turtle.textinput('Please type y or n', 'Do you want to quit? (y) or (n)')
            continue


def high_score_file():  # Makes highscore file if one doesnt exist
    try:
        file_handle = open("high_score.txt", 'r')
        file_handle.close()
    except FileNotFoundError:
        file_handle = open("high_score.txt", 'w')
        file_handle.write('Player Name : High Score : Highest Level \n')
        file_handle.close()


high_score_file()


def top_ten_highscores():  # Utilizes find to organize high score list into the top 10 high scores and associated name
    file_handle = open("high_score.txt", "r")
    file_handle.seek(0)
    lines = file_handle.readlines()
    high_score_dict = dict()
    high_score_list = list()
    top_ten = list()
    # Uses text manipulation whilst reading from file to read values as numbers
    for line in lines:
        colon = line.find(':')
        name = line[:colon].strip()
        line = line[colon + 1:]
        colon = line.find(':')
        score_amount = line[:colon].strip()
        high_score_dict[score_amount] = name
    high_score_list.sort(reverse=True)
    high_score_list = high_score_list[:10]
    for item in high_score_dict:
        if item.isdigit():
            high_score_list.append(item)

    for item in high_score_list:
        top_ten.append((int(item), high_score_dict[item]))
    top_ten.sort(reverse=True)
    return top_ten[:10]


def new_highscore():  # High score write, PASS if health of player = 0 or max level reached, write highscore
    file_handle = open("high_score.txt", 'a+')
    file_handle.write(f'{player_name.upper()} : {score} : {level_number} \n')
    file_handle.close()


def player():  # Creates player sprite, moves it to the starting position
    player_sprite = Polygons((50, 255, 50), 'square')
    player_sprite.tilt(45)
    player_sprite.goto(0, -200)
    player_sprite.shapesize(stretch_len=2, stretch_wid=2)
    return player_sprite


def player_left():  # Moves player left by 10 points
    x = player_square.xcor()
    x -= 10
    player_square.setx(x)


def player_right():  # Moves player right by 10 points
    x = player_square.xcor()
    x += 10
    player_square.setx(x)


# Player shoot, checks to see if the player has any bullets left, if they do, the function adds 1 to the count of /
# the bullets, and then creates a "bullet" object by appending it to the main bullet list. If they don't /
# The function does nothing and will require the player to reload

def player_shoot():  # Creates instance of bullet in memory (by storing in list), keeps track of bullet totals
    global bullet_count
    if bullet_count > 8:
        return
    bullet_count = bullet_count + 1
    bullet_list.append(Polygons((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                "circle").bullets())
    return bullet_list


def reload():  # The reload function when activated (r key) "empties" your bullets, uses threading module /
    # to add a 1 second delay for setting your bullet count back to 0, and also changes your color to show reload timing
    global bullet_count
    if bullet_count == 0:
        return
    bullet_count = 9
    player_square.color(245, 75, 210)

    def cooldown():
        global bullet_count
        bullet_count = 0

    r = Timer(1, cooldown)
    r.start()
    return


def level_load():  # This is in charge of instantiating the enemies and updates the level counter above
    # This was prior to me being comfortable using classes, I generally would not advise using globals
    global level
    global level_number
    level = level + 1
    level_write.speed(0)
    level_write.color(255, 255, 255)
    level_write.hideturtle()
    level_write.penup()
    level_write.goto(-200, 375)
    level_write.clear()
    level_number = level_number + 1
    level_write.write(f'LEVEL {level_number}', font=("Comic Sans MS", 12, "normal"), align="center")
    for _ in range(level):
        enemy_list.append(Polygons((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                   'triangle').enemy())
    return enemy_list


# Screen 1 is the main game screen


# MAIN GAME LOGIC STARTS HERE
window1 = window_creation()

# Rendering Player
player_square = player()

# Listening for user input
window1.onkeyrelease(player_shoot, "space")
window1.onkeypress(player_left, "a")
window1.onkeypress(player_right, "d")
window1.onkeyrelease(reload, "r")
window1.onkeyrelease(level_load, "x")
window1.onkeyrelease(new_highscore, "h")
window1.onkeyrelease(end_game, "k")
window1.onkeyrelease(close_game, 'Escape')

# SCORE WRITE
score_write = turtle.Turtle()
score_write.speed(0)
score_write.color(255, 255, 255)
score_write.hideturtle()
score_write.penup()
score_write.goto(200, 375)
score_write.pendown()
score_write.write(f'SCORE {score}', font=("Comic Sans MS", 12, "normal"), align="center")

# ENEMY CREATION
level_load()
# MAIN GAME LOOP
while True:
    # The error check is required if something fails with the tkinter library
    window1.update()
    try:
        window1.listen()
    except _tkinter.TclError:
        quit()
    if close_time is True:
        quit()
    if not enemy_list:  # If enemies are defeated create 5 additional enemies, update screen with information
        hitboxes.clear()
        gc.collect()
        if end is False:
            level_load()
        else:
            score_write.clear()
            level_write.clear()
    if bullet_count == 0:  # "Ends" the reload animation by swapping color back to green after successful reload
        player_square.color((50, 255, 50))
    # RANDOM ENEMY MOVEMENT AND HIT BOX CREATION
    # YOU HAVE A CUSHION OF 5 COORDINATES TO "HIT" THE ENEMY -2 -1 0 +1 +2
    run_amount = run_amount + 1
    for ship in enemy_list:
        # Captures window or cushion for hitbox, makes list of them
        current_cord = (int(ship.xcor()), int(ship.ycor()))
        current_cord_minus_two = (int(ship.xcor() - 2), int(ship.ycor()))
        current_cord_minus_one = (int(ship.xcor() - 1), int(ship.ycor()))
        current_cord_plus_one = (int(ship.xcor() + 1), int(ship.ycor()))
        current_cord_plus_two = (int(ship.xcor() + 2), int(ship.ycor()))
        ship_xcords = [(current_cord[0] - 1), current_cord[0], current_cord[0] + 1]
        random_direction = random.choice(direction)
        if run_amount % 5 == 0:  # Slows down enemies rate of movement
            run_amount = 0
            if -260 < ship.xcor() < 260:  # As long as ship is in between the start and end points move rand direction
                ship.setx(ship.xcor() + random_direction)
            elif ship.xcor() >= 260:  # If ship at end or past end move to start
                ship.setx(-259)
            else:  # If ship at start or past start move ship to end
                ship.setx(259)
            # Setup Hitbox dictionary, identifies which ship to remove if bullet hits any of the ships hitboxes
            hitboxes[current_cord] = ship
            hitboxes[current_cord_minus_two] = ship
            hitboxes[current_cord_minus_one] = ship
            hitboxes[current_cord_plus_one] = ship
            hitboxes[current_cord_plus_two] = ship
            # Removes any hitboxes no longer relevant to ship (as it is moving)
            # This is formatted this way since you can not pop a dictionary while iterating through it
            for hitbox in hitboxes:
                if hitboxes.get(hitbox) == ship and hitbox[0] not in ship_xcords:
                    hitboxes[hitbox] = None
                    temp_box = hitbox
                    break
                else:
                    temp_box = False
                    continue
            if temp_box:
                hitboxes.pop(temp_box)
    if len(bullet_list) > 0:  # Starts the loop for hit detection if there has been a bullet fired
        for bullet in bullet_list:
            dex = bullet_list.index(bullet)  # Finds the index of the current bullet being viewed in the loop
            bullet_location = (int(bullet.xcor()), int(bullet.ycor()))  # Stores the bullet's coordinate to tuple
            bullet.sety(bullet.ycor() + speed)  # Moves the bullet up by 10 coordinates
            if bullet.ycor() > 415:  # Removes the bullet if it misses, speeds up runtime by removing bullet from mem
                bullet.hideturtle()
                bullet_list.pop(dex)
                continue
            # Finds which ship the current bullet hit (if it did hit anything)
            # Subtracts 1 health from the ships health attribute if it was hit
            # Removes bullet from the bullet list
            if bullet_location in hitboxes:
                which_enemy = hitboxes.get(bullet_location)
                if which_enemy in enemy_list:
                    this_enemy = enemy_list.index(which_enemy)
                else:
                    continue
                enemy_list[this_enemy].hp = enemy_list[this_enemy].hp - 1
                enemy_list[this_enemy].color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                # Adds to score, prints score at top of right of screen
                score = score + 10
                score_write.clear()
                score_write.write(f'SCORE {score}', font=("Comic Sans MS", 12, "normal"), align="center")
                bullet_list.pop(dex)
                bullet.reset()
                bullet.hideturtle()
            # Killed enemy code, if hp less than or equal to 0, delete enemy
            # Removes all traces of enemy from  possible hitboxes
            for enemy in enemy_list:
                delete_me = []
                if enemy.hp <= 0:
                    score = score + 30
                    score_write.clear()
                    score_write.write(f'SCORE {score}', font=("Comic Sans MS", 12, "normal"), align="center")
                    for hitbox in hitboxes:
                        if hitboxes.get(hitbox) == enemy:
                            delete_me.append(hitbox)
                    if delete_me:
                        for delete in delete_me:
                            hitboxes.pop(delete)
                    enemy.reset()
                    enemy.hideturtle()
                    enemy_numbers = enemy_numbers - 1
                    enemy_list.pop(enemy_list.index(enemy))
    if len(enemy_list) > 80:  # Last level is level 75? Before crash at 80 enemies
        end_game()
    # Borders will stop player from going off screen on either side
    # Left Border Player
    if player_square.xcor() < -260:
        player_square.setx(-260)
    # Right Border Player
    if player_square.xcor() > 260:
        player_square.setx(260)
# END
