from threading import RLock

import uuid_definitions
from controller import Controller
from gui import GUI
from train import CompoundTrain, SimpleTrain, SmartTrain

'''
Correct startup sequence requires that, with the script already started, the train
hub(s) be connected first (by momentary press of the green button). Wait a few seconds
until the hub(s) connect(s). As soon as it(they) connect, press the green button on the remote
handset. As soon as it connects, the control loop starts running and the GUI pops up on screen.
Notice that the train LED will be set to its initialization color for about 2 sec, and then will
start blinking to indicate zero power. The LED in the handset will go solid white. LEDs won't 
change color (channel) by pressing the green button (the green buttons in both train and handset 
won't respond to button presses from this point on).
'''

if __name__ == '__main__':

    # global lock for threading access to BLE functionality
    lock = RLock()
    # lock = None

    # Tkinter window for displaying status information
    gui = GUI()

    # Use one of these setups to configure

    # ---------------------- Simple train setup --------------------------

    # train = SimpleTrain("Train", "1", lock=lock, report=True, record=True,
    #                           gui=gui, address=uuid_definitions.HUB_ORIG)
    # controller = Controller(train)

    # ---------------------- Smart train setup for testing ----------------------------

    # train = SmartTrain("Train 1", "1", lock=lock, report=True, record=True,
    #                         gui=gui, direction=DIRECTION_B, address=uuid_definitions.HUB_ORIG)
    # train = SmartTrain("Train 2", "2", lock=lock, report=True, record=True,
    #                         gui=gui, address=uuid_definitions.HUB_TEST)
    # controller = Controller(train)

    # ---------------------- Two-train setup (Smart self-driving) ----------------------------

    # train1 = SmartTrain("Blue", "1", lock=lock, report=True, record=True,
    #                     gui=gui, direction=DIRECTION_B, address=uuid_definitions.HUB_ORIG)
    # train2 = SmartTrain("Purple", "2", ncars=1, led_color=COLOR_PURPLE, lock=lock, report=True, record=True,
    #                         gui=gui, address=uuid_definitions.HUB_TEST)
    #
    # controller = Controller(train1, train2=train2)

    # ---------------------- Compound train setup --------------------------

    # front train hub allows control over the LED headlight.
    train_front = SimpleTrain("Front", "1", lock=lock, report=True, record=True,
                              gui=gui, address=uuid_definitions.HUB_ORIG)

    # rear train hub has a vision sensor
    train_rear = SmartTrain("Rear", "2", lock=lock, report=True, record=True,
                            gui=gui, address=uuid_definitions.HUB_TEST)

    train = CompoundTrain("Massive train", train_front, train_rear)

    controller = Controller(train)

    # --------------------------------------------------------------------------

    # connect everything and start main loop
    # controller.connect_handset()
    gui.root.after(100, gui.after_callback)
    gui.root.mainloop()
