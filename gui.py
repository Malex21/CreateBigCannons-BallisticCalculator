from calculator import BallisticsToTarget, OutOfRangeException
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title('Create Big Cannons : Ballistic Calculator')
root.geometry("1600x768")


def represents_int(s):
    """
    Check if a string can be converted to an integer
    """
    try: 
        int(s)
    except ValueError:
        return False
    else:
        return True

def callback(P):
    """
    Callback for the entries, only allow integers
    """

    if represents_int(P) or P == "" or P == "-":
        return True
    else:
        return False

def controlButton(*args):
    """
    Control if all the entries are filled and enable the button if it's the case
    """


    if all(var.get() for var in [xCannon, yCannon, zCannon, xTarget, yTarget, zTarget, lenghtEntry, powerEntry]):
        button.configure(state="normal")
    else:
        button.configure(state="disabled")

def getAngles():
    """
    Get the angles from the entries and calculate the angles
    """


    xC = xCannon.get()
    yC = yCannon.get()
    zC = zCannon.get()

    xT = xTarget.get()
    yT = yTarget.get()
    zT = zTarget.get()

    cannonCoords = tuple(map(int, (xC, yC, zC)))
    targetCoords = tuple(map(int, (xT, yT, zT)))

    try:

        angles = BallisticsToTarget(cannonCoords, targetCoords, int(powerEntry.get()), (directionEntry.get()).lower(), int(lenghtEntry.get()))

    except OutOfRangeException as e:

        statusMessage.set(e)
        status.configure(text_color="#980404")

    else:

        varYaw.set("Yaw : " + str(angles[0]) + " degrees")
        varPitch.set("Pitch : " + str(angles[1]) + " degrees")
        varAirtime.set("Airtime in ticks : " + str(angles[2]) + " ticks")
        varAirtimeSeconds.set("Airtime in seconds : " + str(angles[3]) + " seconds")
        varFuzeTime.set("Time to put in fuze (in ticks) : " + str(angles[4]) + " ticks")

        statusMessage.set("Calculated !")
        status.configure(text_color="#50bc54")

def main():

    global xCannon, yCannon, zCannon, xTarget, yTarget, zTarget, lenghtEntry, powerEntry, directionEntry, button, statusMessage, status, varYaw, varPitch, varAirtime, varAirtimeSeconds, varFuzeTime

    titre = ctk.CTkLabel(master=root, text="Ballistic Calculator", font=("Roboto", 60), fg_color="#1E538D", corner_radius=20)

    frame = ctk.CTkFrame(master=root, corner_radius=20)
    titre.pack(pady=20, padx=120, fill="both", expand=True, )
    frame.pack(pady=30, padx=60, ipadx=40, fill="both", expand=True)
    frame.columnconfigure(0, weight=1)

    cannonFrame = ctk.CTkFrame(master=frame, width=200)
    targetFrame = ctk.CTkFrame(master=frame, width=200)

    cannonCoord = ctk.CTkLabel(master=cannonFrame, text="Coordinates of the cannon mount (X;Y;Z)", font=("Roboto", 16))
    targetCoord = ctk.CTkLabel(master=targetFrame, text="Coordinates of the target (X;Y;Z)      ", font=("Roboto", 16), padx=20)

    isinteger = root.register(callback)

    statusMessage = ctk.StringVar(value="Waiting calculation...")
    status = ctk.CTkLabel(master=frame, textvariable=statusMessage)

    xCannon = ctk.CTkEntry(master=cannonCoord, placeholder_text="X", validate="key", validatecommand=(isinteger, '%P'))
    yCannon = ctk.CTkEntry(master=cannonCoord, placeholder_text="Y", validate="key", validatecommand=(isinteger, '%P'))
    zCannon = ctk.CTkEntry(master=cannonCoord, placeholder_text="Z", validate="key", validatecommand=(isinteger, '%P'))

    xTarget = ctk.CTkEntry(master=targetCoord, placeholder_text="X", validate="key", validatecommand=(isinteger, '%P'))
    yTarget = ctk.CTkEntry(master=targetCoord, placeholder_text="Y", validate="key", validatecommand=(isinteger, '%P'))
    zTarget = ctk.CTkEntry(master=targetCoord, placeholder_text="Z", validate="key", validatecommand=(isinteger, '%P'))



    options = ctk.CTkFrame(master=frame, width=300)

    options.columnconfigure(0, weight=4)
    options.columnconfigure(1, weight=1)

    power = ctk.CTkLabel(master=options, text="Number of charges", font=("Roboto", 16))
    powerEntry = ctk.CTkEntry(master=options, validate="key", validatecommand=(isinteger, '%P'))

    direction = ctk.CTkLabel(master=options, text="Direction the cannon is facing when not mounted", font=("Roboto", 16))
    directionEntry = ctk.StringVar(value="North")
    directionComboBox = ctk.CTkComboBox(master=options, values=["North", "South", "West", "East"], variable=directionEntry, state="readonly")

    lenght = ctk.CTkLabel(master=options, text="""Lenght of the cannon 
    (From the block held by the mount to the tip of the cannon, both included)""", font=("Roboto", 16))
    lenghtEntry = ctk.CTkEntry(master=options, validate="key", validatecommand=(isinteger, '%P'))

    varYaw = ctk.StringVar(value = "Yaw is unknown")
    varPitch = ctk.StringVar(value = "Pitch is unknown")
    varAirtime = ctk.StringVar(value = "Airtime (ticks) is unknown")
    varAirtimeSeconds = ctk.StringVar(value = "Airtime (seconds) is unknown")
    varFuzeTime = ctk.StringVar(value = "Fuze time (ticks) is unknown")

    results = ctk.CTkFrame(master=frame)


    results.columnconfigure(0, weight=1)
    results.columnconfigure(1, weight=1)
    results.columnconfigure(2, weight=1)
    results.columnconfigure(3, weight=1)
    results.columnconfigure(4, weight=1)

    labelYaw = ctk.CTkLabel(master=results, textvariable=varYaw)
    labelPitch = ctk.CTkLabel(master=results, textvariable=varPitch)
    labelAirtime = ctk.CTkLabel(master=results, textvariable=varAirtime)
    labelAirtimeSeconds = ctk.CTkLabel(master=results, textvariable=varAirtimeSeconds)
    labelFuzeTime = ctk.CTkLabel(master=results, textvariable=varFuzeTime)

    button = ctk.CTkButton(master=frame, text="Calculate !", command=getAngles, state="disabled", width=300, height=40)

    cannonFrame.columnconfigure(0, weight=4)
    cannonFrame.columnconfigure(1, weight=1)
    cannonFrame.columnconfigure(2, weight=1)
    cannonFrame.columnconfigure(3, weight=1)

    targetFrame.columnconfigure(0, weight=4)
    targetFrame.columnconfigure(1, weight=1)
    targetFrame.columnconfigure(2, weight=1)
    targetFrame.columnconfigure(3, weight=1)

    cannonFrame.grid(column=0, row=0, pady=16, padx=20, columnspan=4, sticky="NSEW")
    targetFrame.grid(column=0, row=1, pady=16, padx=20, columnspan=4, sticky="NSEW")

    cannonCoord.grid(column=0, row=0, pady=12, padx=10)

    xCannon.grid(column=1, row=0, pady=12, padx=10)
    yCannon.grid(column=2, row=0, pady=6, padx=10)
    zCannon.grid(column=3, row=0, pady=6, padx=10)

    targetCoord.grid(column=0, row=1, pady=12, padx=10)

    xTarget.grid(column=1, row=0, pady=12, padx=10)
    yTarget.grid(column=2, row=0, pady=12, padx=10)
    zTarget.grid(column=3, row=0, pady=12, padx=10)

    options.grid(column=0, row=2, pady=12, padx=20, columnspan=4, sticky="NSEW")

    power.grid(column=0, row=0, pady=12, padx=10)
    powerEntry.grid(column=1, row=0, pady=12, padx=10)

    direction.grid(column=0, row=1, pady=12, padx=10)
    directionComboBox.grid(column=1, row=1, pady=12, padx=10)

    lenght.grid(column=0, row=2, pady=12, padx=10)
    lenghtEntry.grid(column=1, row=2, pady=12, padx=10)

    button.grid(column=0, row=5, pady=12, padx=10, columnspan=4)


    results.grid(column=0, row=7, pady=12, padx=20, columnspan=4, sticky="NSEW")

    labelYaw.grid(column=0, row=0, pady=12, padx=10)
    labelPitch.grid(column=1, row=0, pady=12, padx=10)
    labelAirtime.grid(column=2, row=0, pady=12, padx=10)
    labelAirtimeSeconds.grid(column=3, row=0, pady=12, padx=10)
    labelFuzeTime.grid(column=4, row=0, pady=12, padx=10)

    status.grid(column=0, row=8, pady=0, padx=20, columnspan=4, sticky="NSEW")

    root.bind("<Key>", controlButton)

    root.mainloop()

if __name__ == "__main__":
    main()
