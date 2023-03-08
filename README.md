SPLOOSH< WAZZAH KABANG

You are a pilot of a beautiful ship The Tetragono and have been sent by your squadron to defend a sector inside of
GALAXY ESPERADE111X88. Your ship is equipped with your favorite weapon, a star blaster cannon developed by your people.
Your squadron has trusted you to solely defend the sector as you are the ace pilot of your planet. Enemies are abound
and are many in number. Fight until your last breath as your planet needs you for future battles!

Game requires python 3 and additonal modules referenced below to run.
Please extract folder prior to running in order for game to launch properly
Requires:
        tkinter,
        turtle,
        random,
        threading,
        and gc modules

Space Bar is shoot, R is reload, X adds level (careful will crash at too many levels),
Escape pauses and allows exit, K goes to end screen, uses A and D for movement

This game was my first real shot at a python project. It uses turtle for the graphics needed to display the Player,
Enemies, Bullets, and any Text displayed on screen.

The backend uses object oriented concepts such as classes to represent distinct enemies and bullets. The enemy and
bullet information are stored in dictionaries, representing their location in memory, as well as, their coordinate location.
The game uses a hitbox system representing coordinates on the xy grid to allow for a "cushion" of sorts when firing at
a given enemy.

Players may save their current score to a high score file and there is a high score screen built by processing text
stored in the file.

