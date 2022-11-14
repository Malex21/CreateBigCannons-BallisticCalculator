from math import sin, cos, atan, sqrt, pi, radians, log
from numpy import linspace


def timeInAir(y0, y, Vy):
    """Find the air time of the projectile, using recursive sequence.
    It gives time in air by comparing the y-coordinate of the shell to the targets.
    The shell will hit target only when its y-coord is the same as the targets,
    so by comparing those we can find for how long the shell is airborn

    Args:
        y0 (float): y coordinate of the projectile
        y (float): y coordinate of the target
        Vy (float): vertical velocity of the projectile

    Returns:
        int: Airtime of projectile in ticks / "Error" if timeout
    """
    t = 0

    if y0 <= y:
        # If cannon is lower than a target, simulating the way, up to the targets level

        while t < 100000:

            y0 += Vy
            Vy = 0.99 * Vy - 0.05

            t += 1

            if y0 > y:  # Will break when the projectile gets higher than target
                break

    while t < 100000:

        y0 += Vy
        Vy = 0.99 * Vy - 0.05

        t += 1

        # Returns only when projectile is at same level than target or lower
        if y0 <= y:
            return t
    return "Error"


def getFirstElement(array):
    """Gives the first element of an array, only use as key for min()

    Args:
        array (list): The array from which we take the element

    Returns:
        float: The element return, it's always a float
    """
    return array[0]


def BallisticsToTarget(cannon, target, power, direction, R1, R2, lenght):
    """Function that calculates the elevation angle to hit the target with a cannon

    Args:
        cannon (tuple): Position of the cannon block held by the mount (x, y, z)
        target (tuple): Position of the target (x, y, z)
        power (int): Power of the cannon / Number of powder charges
        direction (str): Direction of the cannon (East, West...)
        R1 (int): Rotation speed of the yaw shaft
        R2 (int): Rotation speed of the pitch shaft
        lenght (int): Lenght of the cannon from mount to tip

    Returns:
        tuple: The yaw, pitch required and predicted airtime of the projectile
    """

    Dx, Dz = (cannon[0] - target[0], cannon[2] - target[2])
    distance = sqrt(Dx * Dx + Dz * Dz)
    # Horizontal distance between target and mount

    initialSpeed = power

    if Dx != 0:
        yaw = atan(Dz / Dx) * 180 / pi
    else:
        yaw = 90

    if Dx >= 0:
        yaw += 180

    pitch: float
    # Let's bruteforce pitch !

    deltaTimes = []
    for triedPitch in range(60, -30, -1):
        # Bias that the cannon is probably gonna aim up instead of down
        # No use for now, useful for a later optimisation

        triedPitchRad = radians(triedPitch)  # cuz triedPitch is in degrees

        Vw = cos(triedPitchRad) * initialSpeed
        Vy = sin(triedPitchRad) * initialSpeed

        xCoord_2d = lenght * cos(triedPitchRad)
        # This value is the horizontal distance between the mount and the tip
        # of the cannon, on the ballistic plane. By substracting this value from
        # the distance between the mount and the target, we get the horizontal distance
        # between the end of the barrel and the target which is what we want

        try:
            timeToTarget = abs(
                log(1 - (distance - xCoord_2d) / (100 * Vw)) / (-0.010050335853501)
            )
        except ValueError:
            continue
        # This is the air resistance formula, here the denominator is ln(0.99)

        yCoordOfEndBarrel = cannon[1] + sin(triedPitchRad) * lenght

        timeAir = timeInAir(yCoordOfEndBarrel, target[1], Vy)
        if type(timeAir) is str:
            continue

        deltaT = abs(timeToTarget - timeAir)
        # We calculate the difference between the time to target and airtime of the shell
        # The way this whole thing works is by comparing those values
        # We try to find the angle that corresponds the most to the timeToTarget

        """
        TimeToTarget is the time it takes for the shell to reach the target on the horizontal plane
        timeAir is the time it takes for the shell to reach the target depending on the given angle
        We try to find the airTime that corresponds the most to TimeToTarget, by taking the difference of TimeToTarget
        by every airTime possible (Bruteforcing every angle between -30 and 60 degrees)
        """

        deltaTimes.append((deltaT, triedPitch))

    if len(deltaTimes) == 0:
        return "Unreachable target"

    deltaTime, pitch = min(deltaTimes, key=getFirstElement)
    # Gives the minimum value depending on deltaT, the difference between airtime and TimeToTarget

    # We do the same thing, but near pitch, to get a more precise angle

    deltaTimes = []
    for triedPitch in linspace(pitch - 1, pitch + 1, 20):
        # Bias that the cannon is probably gonna aim up instead of down

        triedPitchRad = radians(triedPitch)

        Vw = cos(triedPitchRad) * initialSpeed
        Vy = sin(triedPitchRad) * initialSpeed

        xCoord_2d = lenght * cos(triedPitchRad)

        try:
            timeToTarget = abs(
                log(1 - (distance - xCoord_2d) / (100 * Vw)) / (-0.010050335853501)
            )
        except ValueError:
            continue

        # This is the air resistance formula, here the denominator is ln(0.99)
        # btw log() from math module is ln

        yCoordOfEndBarrel = cannon[1] + sin(triedPitchRad) * lenght

        airtime = timeInAir(yCoordOfEndBarrel, target[1], Vy)

        if type(airtime) is str:  # If timeout
            continue

        deltaT = abs(timeToTarget - airtime)

        deltaTimes.append((deltaT, triedPitch, airtime))

    if len(deltaTimes) == 0:
        return "Unreachable target"

    deltaTime, pitch, airtime = min(deltaTimes, key=getFirstElement)

    if direction == "north":  # Arbitrary because minecraft
        yaw = (yaw + 90) % 360
    elif direction == "west":
        yaw = (yaw + 180) % 360
    elif direction == "south":
        yaw = (yaw + 270) % 360
    elif direction != "east":
        return "Invalid direction"

    # Now, let's get the times we need to take in order to aim our cannon

    yawTime = yaw * 20 / (0.75 * R1)  # in TICKS
    pitchTime = pitch * 20 / (0.75 * R2)  # in TICKS
    fuzeTime = airtime + (deltaTime / 2) - 10

    return (
        yaw,
        pitch,
        airtime,
        yawTime,
        pitchTime,
        fuzeTime,
    )


print("For the cannon coordinates, please input the coordinates of the cannon mount.")
cannonCoord = (
    float(input("x coord of cannon : ")),
    float(input("y coord of cannon : ")) + 2,
    float(input("z coord of cannon : ")),
)
targetCoord = (
    float(input("x coord of target : ")),
    float(input("y coord of target : ")),
    float(input("z coord of target : ")),
)

powderCharges = int(input("Number of powder charges (int) : "))

directionOfCannon = input(
    "What is the standart direction of the cannon ? (north, south, east, west) "
)

yawRPM = float(input("What is the RPM of the yaw axis ? "))
pitchRPM = float(input("What is the RPM of the pitch axis ? "))

cannonLenght = int(
    input(
        "What is the lenght of the cannon ? (From the block held by the mount to the tip of the cannon, the held block excluded) "
    )
)

ballistic = BallisticsToTarget(
    cannonCoord,
    targetCoord,
    powderCharges,
    directionOfCannon,
    yawRPM,
    pitchRPM,
    cannonLenght,
)

if type(ballistic) is tuple:
    print(f"Yaw is {round(ballistic[0], 1)}")
    print(f"Pitch is {round(ballistic[1], 1)}")
    print(f"Airtime is {round(ballistic[2], 0)} ticks")
    print(
        f"With the yaw axis set at {yawRPM} rpm, the cannon must take {round(ballistic[3], 0)} ticks of turning the yaw axis."
    )
    print(
        f"With the pitch axis set at {pitchRPM} rpm, the cannon must take {round(ballistic[4], 0)} ticks of turning the pitch axis."
    )
    print(
        f"You must set the fuze time to {round(ballistic[5], 0)} ticks,\
        which is {round(ballistic[5], 0) // 20} seconds and {round(ballistic[5], 0) % 20} ticks."
    )
else:
    print(ballistic)

# CREDITS OF ORIGINAL FORMULAS : @sashafiesta#1978 on Discord
