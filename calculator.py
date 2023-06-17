from math import sin, cos, atan, sqrt, pi, radians, log

def myLinspace(start, end, num):
    answer = [start]
    delta = (end - start) / num
    for _ in range(num - 1):
        answer.append(answer[-1] + delta)
    answer.append(end)
    return answer

class OutOfRangeException(Exception):
    pass

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

    initialSpeed = power

    nbOfIterations = 5  # by default

    if Dx != 0:
        yaw = atan(Dz / Dx) * 57.2957795131  # 180/pi
    else:
        yaw = 90

    if Dx >= 0:
        yaw += 180

    pitch: float
    # Let's bruteforce pitch !

    def getRoot(tab, sens):
        if sens == 1:
            for i in range(1, len(tab)):
                if tab[i - 1][0] < tab[i][0]:
                    return tab[i - 1]
        elif sens == -1:
            for i in reversed(range(0, len(tab) - 1)):
                if tab[i][0] > tab[i + 1][0]:
                    return tab[i + 1]
        else:
            raise ValueError("sens must be 1 or -1")

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

            deltaTimes.append((deltaT, triedPitch, timeAir))

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

            deltaTimes.append((deltaT, triedPitch, timeAir))

        if len(deltaTimes) == 0:
            raise OutOfRangeException("The target is unreachable with your current canon configuration !")

        deltaTime, pitch, timeAir = min(deltaTimes, key=getFirstElement)

        return deltaTime, pitch, timeAir
        # Gives the minimum value depending on deltaT, the difference between airtime and TimeToTarget

        # We do the same thing, but near pitch, to get a more precise angle


    (deltaTime1, pitch1, airtime1), (deltaTime2, pitch2, airtime2) = tryAllAngles(-30, 60, 21)
    
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

    return (
    (
        yaw,
        pitch1,
        airtime1,
        round(airtimeSeconds1, 2),
        fuzeTime1,
    ),
    (
        yaw,
        pitch2,
        airtime2,
        round(airtimeSeconds2, 2),
        fuzeTime2,
    )
        )


# CREDITS OF ORIGINAL FORMULAS : @sashafiesta#1978 on Discord

