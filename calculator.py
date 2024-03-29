
from math import sin, cos, atan, sqrt, pi, radians, log

class OutOfRangeException(Exception):
    pass


def myLinspace(start, end, num):
    answer = [start]
    delta = (end - start) / num
    for _ in range(num - 1):
        answer.append(answer[-1] + delta)
    answer.append(end)
    return answer

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
        (int, int): Airtime of projectile in ticks / -1 if can't hit from (below / above)
    """
    t = 0
    t_below = 999_999_999

    if y0 <= y:
        # If cannon is lower than a target, simulating the way, up to the targets level

        while t < 100000:

            y0 += Vy
            Vy = 0.99 * Vy - 0.05

            t += 1

            if y0 > y:  # Will break when the projectile gets higher than target
                t_below = t-1
                break

            # If the projectile stopped ascending before going above target then it will never hit it, so return early
            if Vy < 0:
                return -1, -1

    while t < 100000:

        y0 += Vy
        Vy = 0.99 * Vy - 0.05

        t += 1

        # Returns only when projectile is at same level than target or lower
        if y0 <= y:
            return t_below, t
    return -1, -1

def getFirstElement(array):
    return array[0]

def getRoot(tab, sens):
    if sens == 1:
        for i in range(1, len(tab)):
            if tab[i - 1][0] < tab[i][0]:
                return tab[i - 1]
        return tab[-1]
    elif sens == -1:
        for i in reversed(range(0, len(tab) - 1)):
            if tab[i][0] > tab[i + 1][0]:
                return tab[i + 1]
        return tab[0]
    else:
        raise ValueError("sens must be 1 or -1")

def BallisticsToTarget(cannon, target, power, direction, lenght):
    """Function that calculates the elevation angle to hit the target with a cannon

    Args:
        cannon (tuple): Position of the cannon block held by the mount (x, y, z)
        target (tuple): Position of the target (x, y, z)
        power (int): Power of the cannon / Number of powder charges
        direction (str): Direction of the cannon (East, West...)
        lenght (int): Lenght of the cannon from mount to tip

    Returns:
        tuple: The yaw, pitch required and predicted airtime of the projectile (yaw, pitch, airtime, fuzeTime)
    """

    """
    R1 (int): Rotation speed of the yaw shaft
    R2 (int): Rotation speed of the pitch shaft
    """

    Dx, Dz = (cannon[0] - target[0], cannon[2] - target[2])
    distance = sqrt(Dx * Dx + Dz * Dz)
    # Horizontal distance between target and mount

    initialSpeed = power * 2

    nbOfIterations = 5  # by default

    if Dx != 0:
        yaw = atan(Dz / Dx) * 57.2957795131  # 180/pi
    else:
        yaw = 90

    if Dx >= 0:
        yaw += 180

    pitch: float
    # Let's bruteforce pitch !

    def tryAllAngles(low, high, nbOfElements):
        """Bruteforce every angle between low and high, and returns the one that corresponds the most to the timeToTarget
        
        Args:
            low (float): Lower bound of the angle
            high (float): Upper bound of the angle
            nbOfElements (int): Number of elements to bruteforce
        
        Raises:
            OutOfRangeException: If the target is unreachable with the current cannon configuration
        
        Returns:
            tuple: The pitch and the airtime of the shell
        """


        deltaTimes = []
        for triedPitch in myLinspace(low, high, nbOfElements):
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

            t_below, t_above = timeInAir(yCoordOfEndBarrel, target[1], Vy)
            if t_below < 0: continue

            # if target is above cannon it may hit on ascension
            # if target is possible to hit and it doesn't hit on ascension then "timeToTarget - t_below" will
            # be basically timeToTarget + 1 so it will always just calculate "timeToTarget - t_above"
            deltaT = min(
                abs(timeToTarget - t_below),
                abs(timeToTarget - t_above)
            )

            # We calculate the difference between the time to target and airtime of the shell
            # The way this whole thing works is by comparing those values
            # We try to find the angle that corresponds the most to the timeToTarget

            """
            TimeToTarget is the time it takes for the shell to reach the target on the horizontal plane
            timeAir is the time it takes for the shell to reach the target depending on the given angle
            We try to find the airTime that corresponds the most to TimeToTarget, by taking the difference of TimeToTarget
            by every airTime possible (Bruteforcing every angle between -30 and 60 degrees)
            """

            deltaTimes.append((deltaT, triedPitch, deltaT + timeToTarget))

        if len(deltaTimes) == 0:
            raise OutOfRangeException("The target is unreachable with your current canon configuration !")

        deltaTime1, pitch1, timeAir1 = getRoot(deltaTimes, 1)
        deltaTime2, pitch2, timeAir2 = getRoot(deltaTimes, -1)

        return (deltaTime1, pitch1, timeAir1), (deltaTime2, pitch2, timeAir2)
        # Gives the minimum value depending on deltaT, the difference between airtime and TimeToTarget

        # We do the same thing, but near pitch, to get a more precise angle

    def tryAllAnglesUnique(low, high, nbOfElements):
        """Bruteforce every angle between low and high, and returns the one that corresponds the most to the timeToTarget

        Args:
            low (float): Lower bound of the angle
            high (float): Upper bound of the angle
            nbOfElements (int): Number of elements to bruteforce
        
        Raises:
            OutOfRangeException: If the target is unreachable with the current cannon configuration
        
        Returns:
            tuple: The pitch and the airtime of the shell
        """

        deltaTimes = []
        for triedPitch in myLinspace(low, high, nbOfElements):
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

            t_below, t_above = timeInAir(yCoordOfEndBarrel, target[1], Vy)
            if t_below < 0: continue

            # if target is above cannon it may hit on ascension
            # if target is possible to hit and it doesn't hit on ascension then "timeToTarget - t_below" will
            # be basically timeToTarget + 1 so it will always just calculate "timeToTarget - t_above"
            deltaT = min(
                abs(timeToTarget - t_below),
                abs(timeToTarget - t_above)
            )
            # We calculate the difference between the time to target and airtime of the shell
            # The way this whole thing works is by comparing those values
            # We try to find the angle that corresponds the most to the timeToTarget

            """
            TimeToTarget is the time it takes for the shell to reach the target on the horizontal plane
            timeAir is the time it takes for the shell to reach the target depending on the given angle
            We try to find the airTime that corresponds the most to TimeToTarget, by taking the difference of TimeToTarget
            by every airTime possible (Bruteforcing every angle between -30 and 60 degrees)
            """

            deltaTimes.append((deltaT, triedPitch, deltaT + timeToTarget))

        if len(deltaTimes) == 0:
            raise OutOfRangeException("The target is unreachable with your current canon configuration !")

        deltaTime, pitch, timeAir = min(deltaTimes, key=getFirstElement)

        return deltaTime, pitch, timeAir
        # Gives the minimum value depending on deltaT, the difference between airtime and TimeToTarget

        # We do the same thing, but near pitch, to get a more precise angle


    (deltaTime1, pitch1, airtime1), (deltaTime2, pitch2, airtime2) = tryAllAngles(-30, 60, 91)
    
    for i in range(0, nbOfIterations):
        (deltaTime1, pitch1, airtime1) = tryAllAnglesUnique(pitch1 - 10**(-i), pitch1 + 10**(-i), 21)
        (deltaTime2, pitch2, airtime2) = tryAllAnglesUnique(pitch2 - 10**(-i), pitch2 + 10**(-i), 21)
    
    if pitch1 > 60.5:
        pitch1 = "Over 60"
    elif pitch1 < -29.5:
        pitch1 = "Under -30"
    
    if pitch2 > 60.5:
        pitch2 = "Over 60"
    elif pitch2 < -29.5:
        pitch2 = "Under -30"

    airtimeSeconds1 = airtime1 / 20
    airtimeSeconds2 = airtime2 / 20

    if direction == "north":  # Arbitrary because minecraft
        yaw = (yaw + 90) % 360
    elif direction == "west":
        yaw = (yaw + 180) % 360
    elif direction == "south":
        yaw = (yaw + 270) % 360
    elif direction != "east":
        return "Invalid direction"

    # Now, let's get the times we need to take in order to aim our cannon
    """
    yawTime = yaw * 20 / (0.75 * R1)  # in TICKS
    pitchTime = pitch * 20 / (0.75 * R2)  # in TICKS
    """
    fuzeTime1 = int(airtime1 + (deltaTime1 / 2) - 10)
    fuzeTime2 = int(airtime2 + (deltaTime2 / 2) - 10)

    precision1 = round(1 - deltaTime1 / airtime1, 2) * 100
    precision2 = round(1 - deltaTime2 / airtime2, 2) * 100

    return (
    (
        yaw,
        pitch1,
        airtime1,
        round(airtimeSeconds1, 2),
        fuzeTime1,
        precision1,
    ),
    (
        yaw,
        pitch2,
        airtime2,
        round(airtimeSeconds2, 2),
        fuzeTime2,
        precision2,
    )
        )


# CREDITS OF ORIGINAL FORMULAS : @sashafiesta#1978 on Discord

