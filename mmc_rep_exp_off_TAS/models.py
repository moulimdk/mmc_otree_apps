from shared_model import *

author = 'Mouli Modak'

doc = """
Experiment for Treatment Asymmetric Singlemarket Contact in the Laboratory
"""


class Constants(BaseConstants):
    name_in_url = 'mmc_rep_exp_off_TAS'
    players_per_group = None

    ## Payoff Tables
    payoff_matrix1=settings.SESSION_CONFIGS[2].get('payoff_1') # Payoff matrix of setting 1
    payoff_matrix2=settings.SESSION_CONFIGS[2].get('payoff_2') # Payoff matrix of setting 2
    expPoints = {}
    expPoints["R"] = settings.SESSION_CONFIGS[2].get('expPoints_Red') # Expected Points matrix 1
    expPoints["B"] = settings.SESSION_CONFIGS[2].get('expPoints_Blue') # Expected Points matrix 2
    
    SG_lengths = settings.SESSION_CONFIGS[2].get('SG_lengths') # Number of periods in supergames
    SG_totalNum = len(SG_lengths) # Number of supergames
    SG_endPeriods = np.cumsum(SG_lengths) # End period for each supergame
    num_rounds = SG_endPeriods[-1] + 1 # Total number of rounds
    
    dieN = settings.SESSION_CONFIGS[2].get('die_N') #Number on a die
    contProb = settings.SESSION_CONFIGS[2].get('contProb') #Continuation probability in percentages
    endProb = 100 - contProb 
    thres = int(1+(dieN*contProb/100)) #Threshold number on a die

    participation_fee = settings.SESSION_CONFIGS[2].get('participation_fee') # Participation payment
    quiz_fee = settings.SESSION_CONFIGS[2].get('quiz_fee') # Quiz payment

    exRate = int(1/settings.SESSION_CONFIGS[2].get('real_world_currency_per_point')) # Exchange Rate (points to dollar)
    
    time_period = settings.SESSION_CONFIGS[2].get('time_period') # Total time alloted to a period
    

class Subsession(BaseSubsession):
    
    def shuffle(self):
        
        if (self.round_number == 1) or (self.round_number-1 in Constants.SG_endPeriods):
            temp = int(np.where(self.round_number <= Constants.SG_endPeriods)[0][0])+1
            players = self.get_players()
            
            for p in players:
                p.connect(temp)

            random.shuffle(players)
            matrix = []
            if len(players)%2 == 0:
                matrix.append(players)
            else:
                matrix.append(players[0:-1])
                matrix.append([players[-1]])

            self.set_group_matrix(matrix)
            
            for group in self.get_groups():
                group.init_match()
        else:
            self.group_like_round(self.round_number-1)
            for player in self.get_players():
                player.init_period()

    def creating_session(self):
        for p in self.get_players():
            p.connect(0)


class Group(BaseGroup):
    
    ## Group methods

    # Initializing a supergame
    def init_match(self):

        for p in self.get_players():
            p.init_match()

    # Get dice roll for groups
    def get_group_roll(self,rN):

        thres = int(Constants.dieN*Constants.contProb/100)
        temp = 0
        if rN in Constants.SG_endPeriods:
            temp = np.random.choice(np.linspace(start=thres+1, stop=Constants.dieN, num=Constants.dieN-thres))
        else: 
            temp = np.random.choice(np.linspace(start=1, stop=thres, num=thres))

        return temp

    # Get period game
    def period_update(self):

        players = self.get_players() #List ordered by id_in_group
        roll = self.get_group_roll(self.round_number)
        nplayers = len(players)
        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        temp = self.round_number
        
        if roundPos > 0:
            temp = self.round_number - Constants.SG_endPeriods[roundPos-1]

        for i in range(nplayers):

            me = players[i]
            me.periodNumber = temp
            me.roundNumber = roundPos + 1

            me.rollHistory += ","+str(roll)
            me.periodHistory += ","+str(temp)
            me.roundHistory += ","+str(me.roundNumber)

            other = players[(i+1)%nplayers]

            myB = me.myChoiceB
            otherR = other.myChoiceR

            me.myPayoffB = Constants.payoff_matrix2[myB][otherR]
            other.myPayoffR = Constants.payoff_matrix1[otherR][myB]

            me.myChoiceHistoryB += ","+str(myB)
            me.myPayoffHistoryB += ","+str(me.myPayoffB)
            me.otherChoiceHistoryB += ","+str(otherR)
            me.otherPayoffHistoryB += ","+str(other.myPayoffR)

            other.myChoiceHistoryR += ","+str(otherR)
            other.myPayoffHistoryR += ","+str(other.myPayoffR)
            other.otherChoiceHistoryR += ","+str(myB)
            other.otherPayoffHistoryR += ","+str(me.myPayoffB)
                 
            me.participant.vars["myChoiceHistoryB"] = me.myChoiceHistoryB
            me.participant.vars["myPayoffHistoryB"] = me.myPayoffHistoryB
            me.participant.vars["otherChoiceHistoryB"] = me.otherChoiceHistoryB
            me.participant.vars["otherPayoffHistoryB"] = me.otherPayoffHistoryB

            other.participant.vars["myChoiceHistoryR"] = other.myChoiceHistoryR
            other.participant.vars["myPayoffHistoryR"] = other.myPayoffHistoryR
            other.participant.vars["otherChoiceHistoryR"] = other.otherChoiceHistoryR
            other.participant.vars["otherPayoffHistoryR"] = other.otherPayoffHistoryR

        for p in players:
            
            p.participant.vars["rollHistory"] = p.rollHistory
            p.participant.vars["periodHistory"] = p.periodHistory
            p.participant.vars["roundHistory"] = p.roundHistory

            p.participant.vars["roundPayoffHistory"][p.roundNumber] += p.myPayoffR+p.myPayoffB

            if self.round_number in Constants.SG_endPeriods:

                p.participant.vars["totalPayoff"] += p.participant.vars["roundPayoffHistory"][p.roundNumber]

                p.myCumulativePayoff = p.participant.vars["totalPayoff"]

class Player(BasePlayer):
    
    ## Defining player variables

    myChoiceR = models.IntegerField()
    myPayoffR = models.FloatField()
    myChoiceHistoryR = models.StringField()
    myPayoffHistoryR = models.StringField()
    otherChoiceHistoryR = models.StringField()
    otherPayoffHistoryR = models.StringField()

    myChoiceB = models.IntegerField()
    myPayoffB = models.FloatField()
    myChoiceHistoryB = models.StringField()
    myPayoffHistoryB = models.StringField()
    otherChoiceHistoryB = models.StringField()
    otherPayoffHistoryB = models.StringField()   

    roll = models.IntegerField()
    rollHistory = models.StringField()
    periodNumber = models.IntegerField()
    periodHistory = models.StringField()
    roundNumber = models.IntegerField()
    roundHistory = models.StringField()
    numberRoundCurrentRound = models.IntegerField()
    myCumulativePayoff = models.FloatField()
    totalPeriod = models.IntegerField()
    timeout = models.IntegerField()
    totalPayment = models.FloatField()

    # Initialization of participant variables
    def connect(self,rN):

        if self.round_number == 1:
            self.participant.vars["roundPayoffHistory"] = {}
            self.participant.vars["roundPayoffHistory"][1] = 0
            self.participant.vars["totalPayoff"] = 0
        else:
            self.participant.vars["roundPayoffHistory"][rN] = 0
            self.participant.vars["oddGroup"] = 0

            self.participant.vars["myChoiceHistoryB"] = ""
            self.participant.vars["myChoiceHistoryR"] = ""
            self.participant.vars["myPayoffHistoryB"] = ""
            self.participant.vars["myPayoffHistoryR"] = ""
            self.participant.vars["otherChoiceHistoryB"] = ""
            self.participant.vars["otherChoiceHistoryR"] = ""
            self.participant.vars["otherPayoffHistoryB"] = ""
            self.participant.vars["otherPayoffHistoryR"] = ""

            self.participant.vars["rollHistory"] = ""
            self.participant.vars["periodHistory"] = ""
            self.participant.vars["roundHistory"] = ""

    # Initializing player variables
    def init_match(self):

        self.myChoiceHistoryR = ""
        self.myPayoffHistoryR = ""
        self.otherChoiceHistoryR = ""
        self.otherPayoffHistoryR = ""

        self.myChoiceHistoryB = ""
        self.myPayoffHistoryB = ""
        self.otherChoiceHistoryB = ""
        self.otherPayoffHistoryB = ""

        self.rollHistory = ""
        self.periodHistory = ""
        self.roundHistory = ""

        if len(self.get_others_in_group()) == 0:
            self.participant.vars["oddGroup"] = 1
        
        self.periodNumber = 1
        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        self.roundNumber = roundPos + 1

    def init_period(self):
        
        self.myChoiceHistoryR = self.in_round((self.round_number - 1)).myChoiceHistoryR 
        self.myPayoffHistoryR = self.in_round((self.round_number - 1)).myPayoffHistoryR
        self.otherChoiceHistoryR = self.in_round((self.round_number - 1)).otherChoiceHistoryR
        self.otherPayoffHistoryR = self.in_round((self.round_number - 1)).otherPayoffHistoryR

        self.myChoiceHistoryB = self.in_round((self.round_number - 1)).myChoiceHistoryB
        self.myPayoffHistoryB = self.in_round((self.round_number - 1)).myPayoffHistoryB
        self.otherChoiceHistoryB = self.in_round((self.round_number - 1)).otherChoiceHistoryB
        self.otherPayoffHistoryB = self.in_round((self.round_number - 1)).otherPayoffHistoryB

        self.rollHistory = self.in_round((self.round_number - 1)).rollHistory
        self.periodHistory = self.in_round((self.round_number - 1)).periodHistory
        self.roundHistory = self.in_round((self.round_number - 1)).roundHistory

    # Method for odd players
    def oddPlayerPayoff(self):

        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        self.roundNumber = int(roundPos) + 1
        self.totalPeriod = Constants.SG_lengths[int(roundPos)]

        self.participant.vars["roundPayoffHistory"][self.roundNumber] = self.totalPeriod*(Constants.expPoints["R"]+Constants.expPoints["B"])
        self.participant.vars["totalPayoff"] += self.participant.vars["roundPayoffHistory"][self.roundNumber]
        self.myCumulativePayoff = self.participant.vars["totalPayoff"]
        
        self.participant.vars["oddGroup"] = 0