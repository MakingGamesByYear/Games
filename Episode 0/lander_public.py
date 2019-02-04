#Lander 2018
#by MaGBY (Making Games By Year)
#For Episode Zero (Pilot, 1969)

#wow, this is a real game at this point!

def printFileContents(fileStr, missingFileMessage = None):

    if missingFileMessage == None:
        missingFileMessage = "\nWarning: Game is missing the file : " + fileStr
    
    try:
        with open(fileStr) as fo:
            print fo.read()
    except:
        print missingFileMessage
        pass

class LanderGame (object):

    GravitationalConstant = 1.62 # Gravitational constant on the moon, in m/s
    DeltaTimeSeconds = 10.0      # time elapsed for each "frame" of the game

    LanderEmptyMass = 6834 #kilograms mass of lander without any fuel

    #Maximum velocity for perfect, good, and imperfect landings -- in meters/second
    PerfectTouchdownVelocity = .536448
    GoodTouchdownVelocity = 4.4704
    ShipDamagedVelocity = 26.8224

    MinimumLanderFuelBurnRate = 1.50  #minimum KG/s fuel burn rate to produce acceleration
    MaximumLanderFuelBurnRate = 15  #maximum KG/s fuel burn rate

    DefaultIntroStory ="""
Lander 2018
A game by MAGBY
===================

A light blinks out and the computer goes dead.  You're going to have to land this thing manually!
  Luckily you trained for this!

Control the thrusters to slow down your descent, but watch your fuel levels!
    """

    DefaultStrandedStory = """
Wow!  That was harrowing!  But everyone is alive.

But surveying the craft, you see that there was extensive damage.  The ascent module will never take off.

You are stranded.  Unless Earth can mount a rescue mission on time, you might never make it home.

The rest of your crew gives you the honor of taking the first steps onto the surface of the moon.

As you climb out onto the surface and start to take your first steps on an alien surface, in unfamiliar gravity, the entire earth watches, transfixed to their televisions, watching the historic moment.

You search for the right words, the last you might ever transmit to your home.

"""

    DefaultOkayStory = """
Wow!  That was harrowing!  The landing was a little bumpy, but your craft is undamaged.

As you calm your nerves the rest of your crew says it should be you that does the honor of taking the first steps onto the surface of the moon.

As you climb out onto the surface and start to take your first steps on an alien surface, in unfamiliar gravity, the entire earth watches, transfixed to their televisions, watching the historic moment.

You search for the right words, the most profound thing to say to commemorate this historic occasion.

"""

    DefaultWinStory = """
Wow!  That was harrowing!  But you made a perfect landing.

As you calm your nerves the rest of your crew says it should be you that does the honor of taking the first steps onto the surface of the moon.

As you climb out onto the surface and start to take your first steps on an alien surface, in unfamiliar gravity, the entire earth watches, transfixed to their televisions, watching the historic moment.

You search for the right words, the most profound thing to say to commemorate this historic occasion.
"""

    def landerTotalMass(self):
        return LanderGame.LanderEmptyMass + self.landerFuel

    def velocityToCraterDepthMeters(self, velocity):
        return -0.03093051878 * velocity

    def onLanderTouchdown(self):

        velocityMag = abs(self.landerVelocity)

        print "\n\nYour touchdown velocity is : %d (m/s)\n\n" % (velocityMag)

        if velocityMag <= LanderGame.PerfectTouchdownVelocity:
            self.gameOutroWin()
        elif velocityMag <= LanderGame.GoodTouchdownVelocity:
            self.gameOutroWinDecent()
        elif velocityMag <= LanderGame.ShipDamagedVelocity:
            self.gameOutroStranded()
        else:
            #worst case loss scenario
            print "Your inept piloting causes the lander to crash into the lunar surface way too fast.  There were no survivors"
            print "In fact, your create a new crater {:.3f} meters deep!".format(self.velocityToCraterDepthMeters(self.landerVelocity))
            print "The population of the Earth mourns you and your crew as heroes and pioneers."


    def printInstructions(self):
        print "Instructions\n=============================\nYou quickly remember your training."
        print "\nYou will get a chance to adjust the thrust of the lander every %.2f seconds." %(LanderGame.DeltaTimeSeconds)
        print "You adjust the thrusters by selecting a fuel burn rate.  Zero is freefall, or pick a fuel burn rate from %.2f to %.2f kg/second" %(LanderGame.MinimumLanderFuelBurnRate, LanderGame.MaximumLanderFuelBurnRate)
        print "\nYour ship without fuel has a mass of %.2f kg.  You currently have %.2f kg of fuel.  For those of you astronauts that are bad at math, that's a total of %.2f kg.  Accelerating the lander will get easier as you burn more fuel" % (LanderGame.LanderEmptyMass, self.landerFuel, self.landerTotalMass())
        print "You have an ideal safe landing velocity of %.2f m/s " %(LanderGame.PerfectTouchdownVelocity)
        print "\nGood luck!"
    
    def gameIntro(self) :
        printFileContents("game_introfile.txt", LanderGame.DefaultIntroStory)
        self.printInstructions()

    def gameOutroStranded(self):
        printFileContents("game_stranded.txt", LanderGame.DefaultStrandedStory)

        message = "At long last, you speak the historic words :"

        raw_input(message)

    def gameOutroWin(self):
        printFileContents("game_win.txt", LanderGame.DefaultWinStory)

        message = "At long last, you speak the historic words :"

        raw_input(message)

    def gameOutroWinDecent(self):
        printFileContents("game_win_decent.txt", LanderGame.DefaultOkayStory)

        message = "At long last, you speak the historic words :"

        raw_input(message)
        
    def __init__(self) :
        
        self.running = True
        self.groundHeight = 0.0
        self.missionTime = 0.0

        self.landerHeight = 15000.0
        self.landerVelocity = 0.0 #-1700.0
        self.currentBurnRate = 0.0
        self.landerFuel = 8200 #kilograms, initial fuel
        
        self.gameIntro()

    def displayGameState(self) :
        print '\n{0:15}{1:15}{2:15}{3:15}{4:15}'.format("Time(s)", "Height(m)", "Velocity(m/s)", "Fuel(kg)", "Total Mass (kg)")
        print '{0:15}{1:15}{2:15}{3:15}{4:15}'.format(str(self.missionTime), str(self.landerHeight), str(self.landerVelocity), str(self.landerFuel), str(self.landerTotalMass()))
        

    def handleInput(self):

        #skip input if we're out of fuel
        if self.landerFuel == 0:
            return
        
        message = "\nEnter your fuel burn rate (or type quit)"
        
        inputStr = raw_input(message)

        while True:

            if ((inputStr.lower() == "quit") or (inputStr.lower() == "q")):
                self.running = False
                return
            
            try:
                faccel = float(inputStr)

                if faccel >= 0.0 :
                    if faccel <= LanderGame.MaximumLanderFuelBurnRate:                    
                        if faccel >= LanderGame.MinimumLanderFuelBurnRate:
                            self.currentBurnRate = faccel
                            return
                        else:
                            if faccel > 0.0: #nonzero but invalid thrust : print a message
                                print "That's below minimum thrust of %.2f -- turning thrusters off!" % (LanderGame.MinimumLanderFuelBurnRate)

                            self.currentBurnRate = 0.0
                            return
                    else:
                        self.currentBurnRate = LanderGame.MaximumLanderFuelBurnRate
                        print "No can do, but I'll assume you mean maximum burn rate of %.2f" %(self.currentBurnRate)
                        return
                else:
                    print "Please enter a *positive* number!" 
            except:
                print "Please enter a number or type quit!"

            inputStr = raw_input(message)

    def getFuelBurned(self, burnRate, time):
        return min(burnRate*time, self.landerFuel)

    def getAccelerationFromThrust(self, fuelBurned):
        specificImpulse = 3050 # meters / second

        # (fuelBurned / LanderGame.DeltaTimeSeconds) should just give us back the fuel burn rate the user input--
        # except in the case you run out of fuel mid frame.  since we assume in our physics equations that
        # we have a constant acceleration during the timestep, this basically "averages out" the burn rate over the
        # timestep
        force = (fuelBurned / LanderGame.DeltaTimeSeconds) *  specificImpulse

        #print "force is " + str(force)

        return force / self.landerTotalMass()

    def updateTimeStep(self):

        fuelBurned = self.getFuelBurned(self.currentBurnRate, LanderGame.DeltaTimeSeconds)

        self.landerFuel -= fuelBurned

        if fuelBurned != 0 and self.landerFuel == 0:
            print "Oh crap, you're out of fuel!"

        accelerationFromThrust = self.getAccelerationFromThrust(fuelBurned)

        self.missionTime += LanderGame.DeltaTimeSeconds

        acceleration = accelerationFromThrust - LanderGame.GravitationalConstant

        #1/2 * a^t^2
        accelContribution = .5 * acceleration * LanderGame.DeltaTimeSeconds * LanderGame.DeltaTimeSeconds

        self.landerHeight += self.landerVelocity * LanderGame.DeltaTimeSeconds + accelContribution
        self.landerVelocity += acceleration * LanderGame.DeltaTimeSeconds
        
        if (self.landerHeight <= self.groundHeight):
            self.landerHeight = self.groundHeight
            #print "The lander hits the ground with a loud crunch at time(s) : " + str(self.missionTime)

            self.onLanderTouchdown()
            self.running = False

    def run(self):
        while game.running == True :
            game.displayGameState()
            game.handleInput()

            if not game.running :
                continue
            
            game.updateTimeStep()

quitProgram = False

while not quitProgram:
    game = LanderGame()
    game.run()

    while True:
        playAgainMessage = "Would you like to play again?"

        playAgain = raw_input(playAgainMessage).lower()

        if playAgain == 'y' or playAgain == 'yes':
            break
        elif playAgain == 'n' or playAgain == 'no':
            quitProgram = True
            break
        else:
            print "come again?"
            continue
    
    print "Thanks for playing!"
    

