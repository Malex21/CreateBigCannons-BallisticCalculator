# Create Big Cannons : Ballistic Calculator
![image](https://user-images.githubusercontent.com/96785178/236646755-6cc4e52f-693f-4ab0-b87e-f2cb2ae89f06.png)

## What is this ?

This is a program intended to be used in tandem with **Create Big Cannons**, a **Minecraft** mod.

It will give you the required angles for you to hit your target with your cannon !

## Installation

This does not need any installation.
Go to the *latest release* at the right of your screen, download the .exe, put it somewhere, double-click it and an interface should pop up.

## How do I use it ?

Enter what the interface asks for and press calculate. The results will appear at the bottom, or a red message if your cannon is not powerful enough or something else occured.
It will ask for the coordinates of the target and the coordinates of the cannon mount. For both, you must input **integer** coordinates !

For the lenght of the cannon and the number of powder charges, integers are expected. 
The lenght of the cannon is the number of blocks between the cannon block held by the mount, and the tip of the cannon (block from which the projectile comes out). Both those boundary blocks are **to be included** in the lenght.

The direction expected is the direction your cannon is facing when it is not activated/mounted. Press F3 and you will find the direction.

## But how do I make my cannon aim the right way ?

In the next versions of Create Big Cannons, there *might* be an advanced mount which will allow you to input precise angles into the cannon.

However, without Computer Craft, it is hard to aim your cannon precisely.

What I do to aim my cannon manually is to press F3, and I can check the angles my character has (Horizontal and vertical angle).
The horizontal angle is relative to the south direction (0° means south) and is positive when facing west (90° means west). And 180°/-180° means north, and -90° means east.
Don't forget that the program will give you the yaw (horizontal) angle relative to the direction you gave it, and it will give you the angle between 0° and 360° clockwise. This should change in the future.
I try to aim my cannon by putting my character head next to the block held by the mount, and then I will try to get my character angles to be the same pitch than the program gives (In minecraft, looking up gives a negative pitch angle while the program considers up to be "positive") and I will aim the cannon until it's aiming where I'm looking. It's the same thing for the yaw angle.

## Where can I find those player angles ?

![angles](https://user-images.githubusercontent.com/96785178/236646396-8c34bdc7-cfea-48ee-acf8-0a54e753ecd0.png)

## Issues

If something is not working correctly, please make an issue here.

If the program says the angle is -30° (minimum angle) or 60° (maximum angle of cannons), it's probably wrong and means that the target is too elevated / too far down to be able to hit. I should soon add a clear message for that.

## Credits

**@sashafiesta#1978 (Discord) :** Original formulas and principles, you can find their very good demonstration in the Create Big Cannons discord server (as of now, pinned in #showcase).

**@Malex#6461 (Me) :** Python adaptation, this user interface, some changes and improvements on the original formulas.
