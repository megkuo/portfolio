# Megan Kuo, mlk6une, gamebox project final submission

"""
The player is a ghost hunter, and is trying to collect as many ghosts as possible before dawn breaks. Additionally,
monsters may be implemented that will try to harm the player, and if the player's health reaches 0, then the player
receives a game over. The goal is trying to collect as many ghosts as possible.
sssssd
I discussed with my brother troubleshooting and certain components (ex. a better way to change my gamebox image sizes
and for sorting the different variables my code contains via a dictionary called settings)
He also helped my sanity in my last-minute scramble :D
"""

# --------------------------Components Included-------------------------

# Things implemented:
# - animated playable character
# - enemies (demons and zombies)
# - collectables: ghosts!
# - timer (goes from midnight to dawn, changing of background) # each game is around 1 minute
# - health bar

# Controls:
# WASD to move up, left, down, and right respectively (normal game controls)
# Space to dash


# -----------------------------Actual Code-------------------------------------

import pygame
import gamebox
import random
import time

camera = gamebox.Camera(800, 600)  # initial creation of the camera gamebox, size of display
settings = {}  # initializing the settings dictionary to be used later

# -----------------------------Functions for Creating Gameboxes---------------------

def make_player(x, y):
    """
    Makes the gamebox for the player character with the specified image/frame at the desired size. This player
    character has different frames for an animated walk.
    :param x: x-coordinate of spawn location
    :param y: y-coordinate of spawn location
    :return: player gamebox
    """
    global player_images
    global settings
    player_images = gamebox.load_sprite_sheet("player_spritesheet.png", 2, 8)  # creates the list of images for the
    # sprite sheet
    player = gamebox.from_image(x, y, player_images[int(settings["player_walk_frame"])])  # creates the gamebox
    player.size = [600/10, 800/10]  # stretch and squash to make box exact dimensions
    return player

def make_demon(x, y):
    """
    Makes the gamebox for the demon with the specified image/frame at the desired size. This is an enemy.
    :param x: x-coordinate of spawn location
    :param y: y-coordinate of spawn location
    :return: demon gamebox
    """
    demon = gamebox.from_image(x, y, "demon_sprite.png")  # uses a specific image as the sprite/gamebox
    demon.size = [600/10, 800/10]  # stretch and squash to make box exact dimensions
    return demon

def make_zombie(x, y):
    """
    Makes the gamebox for the zombie with the specified image/frame at the desired size. This is an enemy.
    :param x: x-coordinate of spawn location
    :param y: y-coordinate of spawn location
    :return: zombie gamebox
    """
    zombie = gamebox.from_image(x, y, "zombie_sprite.png")  # uses a specific image as the sprite/gamebox
    zombie.size = [600/10, 800/10]  # stretch and squash to make box exact dimensions
    return zombie

def make_ghost(x, y):
    """
    Makes the gamebox for the ghost with the specified image/frame at the desired size. This is a collectible rather
    than an enemy character.
    :param x: x-coordinate of spawn location
    :param y: y-coordinate of spawn location
    :return: ghost gamebox
    """
    global ghost_images
    global settings
    ghost_images = gamebox.load_sprite_sheet("ghost_spritesheet.png", 1, 3)  # creates list of images
    ghost = gamebox.from_image(x, y, ghost_images[int(settings["ghost_frame"])])  # start position, assigning frame
    ghost.size = [600 / 12, 800 / 12]  # stretch and squash to make box exact dimensions
    return ghost

# -----------------------------------Other Functions To Be Used-------------------------

# settings idea from my brother because I have so many variables, my pain-staking retyping and reformatting... XD
# k nvm he helped me use regex and life is easier
# I love having so many variables


def reset_settings():
    """
    This dictionary stores many settings as keys paired with their corresponding values. This allows for easier editing
    and usage of much of the different settings. Included are settings regarding the gameboxes, as well as game
    conditions.
    It is used in the beginning to create all of the settings for the game to run.
    :return: settings dictionary of keys and values
    """
    global settings

    # creating the gameboxes to be displayed on the start screen
    start_logo = gamebox.from_image(400, 180, "ghost_hunter_logo.png")
    start_logo.size = [int(840 / 1.5), int(395 / 1.5)]  # note: I spent a sad amount of time on this haha

    created_by = gamebox.from_image(660, 560, "created_by.png")
    created_by.size = [int(1444 / 6), int(301 / 6)]

    instructions_and_controls = gamebox.from_image(100, 470, "instructions_and_controls.png")
    instructions_and_controls.size = [int(601 / 3.5), int(737 / 3.5)]

    start_instructions = gamebox.from_image(400, 400, "start.png")
    start_instructions.size = [int(833 / 3), int(255 / 3)]

    settings = {
        # game conditions:
        "current_score": 0,  # keeps track of how many ghosts have been collected, used to display score
        "game_over": False,  # used to run specific sets of code depending on current game condition
        "game_won": False,  # same as above, changes when the timer runs out
        "game_started": False,  # same as above, runs initialization code

        # ghost settings:
        "respawn_ghost": 1,  # time limit to collect a ghost, when timer is up, it will respawn
        "ghost_frame": 0,  # same?
        "ghost_spacing": 150,  # not actually used, but would create a minimum distance between ghost spawn locations

        # player settings:
        "player_speed": 10,  # player's default speed for movement
        "player_alive": True,  # causes certain elements of code to run if True or False (ex. can lose health)
        "health": 100,  # initial health
        "move_health_bar": 0,  # used to shift the gamebox for health as it depletes, necessary because of the gamebox's
        # tendency to shrink relative to its center, rather than from one side
        "player_can_be_hurt": True,  # allows the player's health to be depleted if True
        "player_can_be_hurt_timer": 50,  # grace period after injury
        "player_walk_frame": 0,  # initializing the animation frame to be displayed for the player

        # demon settings
        "demon_1_on_screen": False,  # if False, spawns a demon on the screen and activates other necessary code
        "demon_1_wait": True,  # when it is spawned, it will have a wait time before it can dash across the screen
        "demon_1_wait_time": 30,  # period of time the demon must be on screen for before it can dash, gives player
        # time to recognize it, counted in frames
        "spawn_side": 0,  # initial value, this will be randomized to spawn the demon on either the left or right
        "spawn_position": 0,  # initial value, this will be randomized to spawn the demon within a range of y-values
        "demon_1_can_hurt": True,  # if True, then player can be hurt by the demon
        "demons_on_screen": [],  # I don't end up using this because I end up having only one demon

        # zombie settings
        "zombie_speed": 5,  # speed of the zombie # well I didn't actually use this haha, just set it to 2.5 pixel mvmt
        "zombie_on_screen": False,  # if False, runs the code to spawn a new one

        # timer-related settings
        "sky_R": 0,
        "sky_G": 20,
        "sky_B": 55,
        "sky_color": (0, 20, 55),  # essentially, I ended up using the background color of the sky to determine when the
        # game should end... rather than the other way around...
        "hour": 0,  # initializes timer, starts it at 12 am
        "time": ["12 am", "1 am", "2 am", "3 am", "4 am", "5 am", "6 am"],  # list of times to be displayed (str)
        "timer": 0,  # initializes the timer for the gameplay time

        # other settings/gameboxes:
        "start_screen": [start_logo, created_by, instructions_and_controls, start_instructions],  # uses start screen
        # gameboxes and puts them in a list to be run/displayed together
        "ground": gamebox.from_color(400, 400, (39, 39, 61), 800, 600),  # (x, y, color, width, height)
        "fences": [  # referencing pong lab code for implementation of boundaries for gameplay
            gamebox.from_color(400, 110, "grey", 780, 5),
            gamebox.from_color(400, 590, "grey", 780, 5),
            gamebox.from_color(790, 350, "grey", 5, 485),
            gamebox.from_color(10, 350, "grey", 5, 485),
        ],
    }

    return settings


def startup():
    """
    Initial startup creating of the different gameboxes. This also starts the game when activated.
    """
    global player
    global demon_1
    global ghost_1
    global zombie_1
    global settings
    player = make_player(400, 300)
    demon_1 = make_demon(-50, -50)
    zombie_1 = make_zombie(850, 650)
    ghost_1 = make_ghost(-10, -10)  # all of the gameboxes are created/spawned, and game_started is changed to True in
    # order to activate the code for gameplay
    settings["game_started"] = True


# -------------------------------------------Tick Function for The Game-------------------------------


def tick(keys):
    """
    This is the function for the game to run. It takes in key inputs and translates them into action within the game.
    :param keys: keyboard/mouse input
    """

    global settings  # imports the dictionary containing all of the various settings

    if settings["game_started"]:  # checks to see if game has been started

        # Code for Demon ------------------------------------------------------------------
        # demon spawning
        if not settings["demon_1_on_screen"]:  # triggers spawning of demon
            settings["demon_1_wait_time"] = 20  # it will wait a few seconds before it dashes
            settings["demon_1_wait"] = True  # tells it to wait and prevents movement
            settings["demon_1_on_screen"] = True  # activates code that relies on it being on screen
            settings["spawn_side"] = random.randint(0, 1)  # randomly spawns on left or right side of screen
            if settings["spawn_side"] == 0 or settings["spawn_side"] == 1:
                settings["spawn_position"] = random.randint(200, 500)  # determines its y-coordinate of its spawn loc.
                demon_1.y = settings["spawn_position"]
                if settings["spawn_side"] == 0:  # left side spawn
                    demon_1.x = 50
                elif settings["spawn_side"] == 1:  # right side spawn
                    demon_1.x = 750

        if settings["demon_1_on_screen"]:  # this all happens only if demon is on screen

            # demon movement: -------------------
            settings["demon_1_wait_time"] -= 1  # decreases wait time of demon
            if settings["demon_1_wait_time"] == 0:  # once wait time runs out
                settings["demon_1_wait"] = False  # it exits waiting state

            if not settings["demon_1_wait"]:  # if not in waiting state anymore
                settings["demon_1_can_hurt"] = True  # prevent hurting player if spawns on them? not really haha

                # acceleration/direction
                if settings["spawn_side"] == 0:  # left side
                    demon_1.xspeed += 2  # moves faster to the right
                elif settings["spawn_side"] == 1:  # right side
                    demon_1.xspeed -= 2  # moves fast to the left

                # demon and player interact
                if player.touches(demon_1, -20, -20) and settings["demon_1_can_hurt"] \
                        and settings["player_can_be_hurt"]:  # trying to be gracious with hitbox area/player health
                    settings["health"] -= 20  # player health is decreased by 20
                    settings["demon_1_can_hurt"] = False  # to prevent getting docked multiple times for "one demon"
                    settings["player_can_be_hurt"] = False  # immunity period of time for the player

            # if demon goes off-screen:
            if demon_1.x < -100 or demon_1.x > 900:  # if it exits the camera's display/the screen
                settings["demon_1_on_screen"] = False  # this will allow the demon to be respawned
                demon_1.xspeed = 0  # prevents continual zooming into the void

        # demon movement
        demon_1.x += demon_1.xspeed  # actually moves the demon's x-coordinate if it has speed/acceleration

        # Player Character -----------------------------------------------------------

        # player movement
        if settings["player_speed"] > 10:  # cap for player speed/tends towards speed of 10
            settings["player_speed"] -= 1

        if pygame.K_SPACE in keys and settings["player_speed"] == 10:  # tried to make it so it would only be able to
            # periodically dash
            settings["player_speed"] = 20  # random dash feature haha

        if pygame.K_w in keys:
            player.move(0, -settings["player_speed"])  # to move the gamebox up, need to have negative y velocity
            settings["player_walk_frame"] += .5  # works to shift walking frame slowly

        if pygame.K_s in keys:
            player.move(0, settings["player_speed"])  # need positive y velocity to move down
            settings["player_walk_frame"] += .5  # works to shift walking frame slowly

        if pygame.K_a in keys:  # moving to left
            player.move(-settings["player_speed"], 0)
            if settings["player_walk_frame"] >= 7:  # keeps it so only frames w/ player facing left will show
                settings["player_walk_frame"] = 0  # resets it
            settings["player_walk_frame"] += .5  # works to shift walking frame slowly

        if pygame.K_d in keys:  # moving to the right
            player.move(settings["player_speed"], 0)
            if settings["player_walk_frame"] < 8:  # keeps it so only frames w/ player facing right will show
                settings["player_walk_frame"] = 8  # starts it at the first right-facing frame
            settings["player_walk_frame"] += .5  # works to shift walking frame slowly

        if not keys:  # if the player is standing, it defaults to the correct standing frame
            if settings["player_walk_frame"] <= 7:  # if the player is facing left, it will use the standing frame that
                # faces the left
                settings["player_walk_frame"] = 0
            elif settings["player_walk_frame"] <= 15:  # if the player is facing right, it will use the standing frame
                # that faces the right
                settings["player_walk_frame"] = 8

        if settings["player_walk_frame"] >= 7 and pygame.K_a in keys:  # if they need to shift to facing left
            settings["player_walk_frame"] = 0

        if settings["player_walk_frame"] >= 15:  # if it's still facing right, it'll restart the cycle of frames
            settings["player_walk_frame"] = 8

        # Zombie Code ----------------------------------------------
        if not settings["zombie_on_screen"]:  # to spawn zombie
            settings["zombie_on_screen"] = True

        # zombies will chase the player at a slower pace, 2.5 vs. 10+
        if settings["zombie_on_screen"]:
            if player.y < zombie_1.y:
                zombie_1.y -= 2.5
            if player.y > zombie_1.y:
                zombie_1.y += 2.5

            if player.x < zombie_1.x:
                zombie_1.x -= 2.5
            if player.x > zombie_1.x:
                zombie_1.x += 2.5

            if zombie_1.touches(player,  -20, -20):
                if settings["player_can_be_hurt"]:
                    settings["health"] -= 20
                    settings["player_can_be_hurt"] = False

                # zombie respawns when touches player
                settings["spawn_position"] = random.randint(200, 500)
                zombie_1.y = settings["spawn_position"]  # how much up or down/vertical position
                if settings["spawn_side"] == 0:  # left side  # this is actually borrowed from the demon's spawn_side
                    zombie_1.x = -50
                elif settings["spawn_side"] == 1:  # right side
                    zombie_1.x = 850

        # Ghost Code ------------------------------------------------------

        # tells it to respawn the ghost every 100 frames/3.3 seconds or so
        settings["respawn_ghost"] += 1
        if settings["respawn_ghost"] >= 100:  # after 100 frames, it will respawn
            settings["respawn_ghost"] = 0  # timer is reset, indicates that it should be respawned
            settings["ghost_frame"] += 1  # if it respawns, then the ghost's image will change

            if settings["ghost_frame"] == 3:  # resets it back to 0 if it would otherwise exceed the index range
                # could also use modulo but ehh
                settings["ghost_frame"] = 0

        if player.touches(ghost_1):  # get point if touch ghost, then it respawns randomly
            x = random.randrange(20, 780)
            y = random.randrange(140, 580)
            ghost_1.x = x
            ghost_1.y = y
            settings["current_score"] += 1
            settings["respawn_ghost"] = 1  # so that it won't respawn again right after (when = to 0, that indicates
            # time ran out and it needs to be respawned), aka its timer is restarted

            settings["ghost_frame"] += 1  # cycles to next image for respawn
            if settings["ghost_frame"] == 3:  # restarts cycle if it reaches the last frame
                settings["ghost_frame"] = 0

        if settings["respawn_ghost"] == 0:  # if time runs out, ghost respawns
            x = random.randrange(20, 780)
            y = random.randrange(140, 580)
            ghost_1.x = x
            ghost_1.y = y
            settings["respawn_ghost"] = 1  # sets timer to 1 so that it won't reactivate respawning
            settings["ghost_frame"] += 1
            if settings["ghost_frame"] == 3:  # resets it back to 0 if it would otherwise exceed the index range
            # could also use modulo but ehh
                settings["ghost_frame"] = 0

        # using fences as boundaries for player, also referenced pong lab for this mechanic
        for fence in settings["fences"]:  # applies code to each fence/gamebox in settings["fences"]
            if player.touches(fence):
                player.move_to_stop_overlapping(fence)

        # health-----------------
        if settings["health"] == 0:  # if player is dead
            settings["player_alive"] = False
            settings["game_over"] = True

        # immunity timer, gives about 1 second of immunity after being hit
        if not settings["player_can_be_hurt"]:
            settings["player_can_be_hurt_timer"] -= 1
            if settings["player_can_be_hurt_timer"] == 0:
                settings["player_can_be_hurt_timer"] = 30  # restarts timer for next time player is hit
                settings["player_can_be_hurt"] = True  # player can lose health again

        # drawing gameboxes :D
        settings["sky_color"] = (settings["sky_R"], settings["sky_G"], settings["sky_B"])  # tuple for RGB color of sky
        camera.clear(settings["sky_color"])  # important to have this first so that all the old gameboxes will be
        # properly cleared, and that it will be behind all of the other gameboxes

        # timer
        # RGB = timer
        if settings["hour"] >= 0:  # color of sky starts changing after 1 am
            if settings["sky_R"] < 255 and settings["hour"] < 4:
                settings["sky_R"] += .0625
            if settings["sky_R"] < 255 and settings["hour"] >= 4:  # sky becomes more red faster
                settings["sky_R"] += .125
            if settings["sky_G"] < 54:
                settings["sky_G"] += .02
            if settings["sky_B"] < 109:  # max desired B value
                settings["sky_B"] += .03

            settings["timer"] += 1  # timer increases as game progresses
            if settings["timer"] % 300 == 0:
                settings["hour"] += 1  # every 10 seconds or so, the hour will change (ex. 12 am to 1 am), hour gives
                # the index value for the time list

            current_time = settings["time"][settings["hour"]]  # in dict, key = list and pulls the index wanted
            camera.draw(
                gamebox.from_text(100, 50, current_time, 70, "white"))  # note: use different fonts in final version
            if not settings["game_won"] and current_time == "6 am":  # ends the game
                settings["game_won"] = True

        # DRAWING

        camera.draw(settings["ground"])

        for fence in settings["fences"]:
            camera.draw(fence)

        ghostx = ghost_1.x
        ghosty = ghost_1.y
        camera.draw(make_ghost(ghostx, ghosty))  # draws the ghost at its current coordinates (since it doesn't have a
        # function like the others... surely an oversight haha)
        camera.draw(gamebox.from_text(620, 50, "Score:", 50, "white"))
        camera.draw(gamebox.from_text(700, 50, str(settings["current_score"]), 50, "white"))

        if settings["demon_1_on_screen"]:
            camera.draw(demon_1)

        if settings["zombie_on_screen"]:
            camera.draw(zombie_1)

        x = player.x
        y = player.y
        camera.draw(make_player(x, y))  # drawing based on coordinates and fetched image

        # score needs to be constantly updated

        if settings["game_over"]:  # or settings["sky_R"] == 255:
            # aka game is over when player's health is depleted or "timer" is up
            settings["game_over"] = True  # hmm this is kind of redundant haha

        if settings["health"] > 0:  # if the player still has health
            camera.draw(gamebox.from_color(650, 80, "black", 100, 20))  # background of the health bar, allows user to
            # see how much has been depleted
            if settings["health"] == 100:
                camera.draw(gamebox.from_color(650, 80, "green", settings["health"], 20))
            else:
                settings["move_health_bar"] = (100 - settings["health"]) / 2  # amt to move the midpt appropriately
                camera.draw(gamebox.from_color(650 - settings["move_health_bar"], 80, "green", settings["health"], 20))
                # the gamebox would shrink by 10 pixels on each side for a total of 20, so it should be shifted to the
                # left by 10 pixels to make it seem the health bar shrunk by 20 pixels from the right side

    else:  # when the game is not started, it will display start screen
        camera.clear("black")

        for item in settings["start_screen"]:  # draws all of the start screen gameboxes
            camera.draw(item)

        if pygame.K_RETURN in keys:  # OH HO HO :D (to start the game)
            startup()  # initializes the gameboxes
            settings = reset_settings()
            settings["game_started"] = True
            # if want restart, will need to refill settings["health"] bar/game over conditions

    camera.display()  # tells it to show image generated

    if settings["game_over"]:  # down here so that "Game Over" will also display, if game is over after gameplay
        camera.clear("black")
        camera.draw(gamebox.from_text(400, 220, "You lost :(", 70, "white"))
        camera.draw(gamebox.from_text(350, 300, "Score:", 50, "white"))
        camera.draw(gamebox.from_text(430, 300, str(settings["current_score"]), 50, "white"))
        camera.display()  # camera.display() is nested in here specifically because I use time.sleep(), and it otherwise
        # fails to draw the gameboxes before it is paused
        time.sleep(3)  # displays the game over screen for 3 seconds
        settings["game_started"] = False  # starts start screen
        settings["game_over"] = False  # removes game over screen

    if settings["game_won"] and not settings["game_over"]:  # makes sure that player survived until timer ended
        camera.clear("black")
        camera.draw(gamebox.from_text(400, 220, "You won!", 70, "white"))
        camera.draw(gamebox.from_text(350, 300, "Score:", 50, "white"))
        camera.draw(gamebox.from_text(430, 300, str(settings["current_score"]), 50, "white"))
        camera.display()
        time.sleep(3)  # displays the game won screen for 3 seconds
        settings["game_started"] = False  # will show start screen
        settings["game_over"] = False
        settings["game_won"] = False  # removes game won screen


settings = reset_settings()  # initializes settings to default values and creates the settings dict to be used in tick()
gamebox.timer_loop(30, tick)  # acts as a framerate

# I apologize for not using more functions...
# thanks for reading!





