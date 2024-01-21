# Create Big Cannons : Ballistic Calculator
![image](https://github.com/Malex21/CreateBigCannons-BallisticCalculator/assets/96785178/7e2e47f8-c82b-4931-9e47-6c770f65fa4a)


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

Relative precision is a quick way to determine whether a shot is precise or not. The higher it is, the more likely the shot is gonna hit.
More precisely, a high relative precision means that the shell should land *relatively* close to the target.
For example, firing on a close target will land the shot closer than on a far target, and yet relative precision remains unchanged between those 2 targets ;
that is because the area of what we consider "close" gets bigger on longer distances.

The current formula for calculating this value (relative precision) remains experimental !

As of v1.1.0, there are now two trajectories calculated (steep and shallow).

## But how do I make my cannon aim the right way ?

An "advanced cannon mount" is currently planned to release in Create Big Cannons 0.6.0 which is not yet out.
This mount allows you to aim the cannon through a GUI where you should be able to input the angles.

There are also create contraptions which allow you to aim your cannon through Computer Craft.
You can find examples of such contraptions in the #showcase channel in the [Create Big Cannons discord server](https://discord.gg/vgfMMUUgvT).

However, without Computer Craft, it is hard to aim your cannon precisely.

### Manual aiming

What I do to aim my cannon manually is to press F3, and I can check the angles my character has (Horizontal and vertical angle).
The horizontal angle is relative to the south direction (0° means south) and is positive when facing west (90° means west). And 180°/-180° means north, and -90° means east.

Don't forget that the program will give you the yaw (horizontal) angle relative to the direction you gave it, and it will give you the angle between 0° and 360° clockwise. This should change in the future.

I try to aim my cannon by putting my character head next to the block held by the mount, and then I will try to get my character angles to be the same pitch than the program gives (In minecraft, looking up gives a negative pitch angle while the program considers up to be "positive") and I will aim the cannon until it's aiming where I'm looking. It's the same thing for the yaw angle.

## Where can I find those player angles ?

![angles](https://user-images.githubusercontent.com/96785178/236646396-8c34bdc7-cfea-48ee-acf8-0a54e753ecd0.png)

## How does it work ?

This program calculates the angles through bruteforcing. There is currently no known public direct formula that provides the angles, or at least none that I know of.
Although this program bruteforces the angles, it is still very fast.

I might post more details here, but sashafiesta's demonstration in the [Create Big Cannons discord server](https://discord.gg/vgfMMUUgvT) covers pretty much everything (pinned in #showcase as of now). In case of doubt on how it functions I invite you to read the comments in the code (in calculator.py, the other .py is just graphics stuff).

I and many others have tried to find a direct formula but as far as I know no one succeeded in doing so. I have my doubts that such formula actually exists.

## Build instructions

Python version used is 3.9.13 64-bit.

Copy the repo in some folder. You need to have customtkinter installed (do so through pip)
In order to build, use Pyinstaller in a venv (to get the size down since you then have less libraries installed).

Example command : 
pyinstaller --noconfirm --onefile --windowed --name "CBC BC v1.2.0" --add-data "path to calculator.py" --add-data "C:/Users/<user>/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0/LocalCache/local-packages/Python39/site-packages/customtkinter;customtkinter/"  "path to gui.py"

Note that your target file should be gui, as it is the one importing calculator.py. Also, you absolutely have to --add-data your customtkinter **folder** , else it won't work.
You might have to install customtkinter on the venv too.

The exe should appear in a "dist" folder located in the directory where your cmd is.

## Issues

If something is not working correctly, please make an issue here.

If the cannon is a tad bit not powerful enough, the program might give very imprecise results. I am aware of this issue and working on it. (Might be fixed through SuperSpaceEye's pull request, to test)

## Credits (on Discord)

**@sashafiesta :** Original formulas and principles, you can find their very good demonstration in the Create Big Cannons discord server (as of now, pinned in #showcase).

**@malexy (Me) :** Python adaptation, this user interface, some changes and improvements on the original formulas.
