from shared_model import *

author = 'Mouli Modak'

doc = """
Experiment for Treatment Symmetric Singlemarket Contact in the Laboratory
"""

class Constants(BaseConstants):
    name_in_url = 'mmc_rep_exp_off_TSM'
    players_per_group = None

    ## Payoff Tables
    payoff_matrix1=settings.SESSION_CONFIGS[3].get('payoff_1') # Payoff matrix of setting 1
    payoff_matrix2=settings.SESSION_CONFIGS[3].get('payoff_2') # Payoff matrix of setting 2
    expPoints = {}
    expPoints["R"] = settings.SESSION_CONFIGS[3].get('expPoints_Red') # Expected Points matrix 1
    expPoints["B"] = settings.SESSION_CONFIGS[3].get('expPoints_Blue') # Expected Points matrix 2
    
    SG_lengths = settings.SESSION_CONFIGS[3].get('SG_lengths') # Number of periods in supergames
    SG_totalNum = len(SG_lengths) # Number of supergames
    SG_endPeriods = np.cumsum(SG_lengths) # End period for each supergame
    num_rounds = SG_endPeriods[-1] + 1 # Total number of rounds
    
    dieN = settings.SESSION_CONFIGS[3].get('die_N') #Number on a die
    contProb = settings.SESSION_CONFIGS[3].get('contProb') #Continuation probability in percentages
    endProb = 100 - contProb 
    thres = int(1+(dieN*contProb/100)); #Threshold number on a die

    participation_fee = settings.SESSION_CONFIGS[3].get('participation_fee') # Participation payment
    quiz_fee = settings.SESSION_CONFIGS[3].get('quiz_fee') # Quiz payment

    exRate = int(1/settings.SESSION_CONFIGS[3].get('real_world_currency_per_point')) # Exchange Rate (points to dollar)
    
    time_period = settings.SESSION_CONFIGS[3].get('time_period') # Total time alloted to a period
    time_begin = settings.SESSION_CONFIGS[3].get('time_welcome') # Time alloted in the first page
    time_next = settings.SESSION_CONFIGS[3].get('time_next') # Time to next round


class Subsession(BaseSubsession):

    def pairs(self,x):
        pairs_group = []

        #If group has even number of players
        if len(x)%2 == 0: 
            for i in list(range(0,int(len(x)/2))):
                pairs_group.append(x[2*i:2*(i+1)])
        #If group has odd number of players
        else: 
            for i in list(range(0,int(len(x)/2))):
                pairs_group.append(x[2*i:2*(i+1)])
            pairs_group.append([x[-1]])

        return pairs_group
    
    def shuffle(self):
        print("Otree Round Number:", self.round_number)
        if (self.round_number == 1) or (self.round_number-1 in Constants.SG_endPeriods):
            temp = int(np.where(self.round_number <= Constants.SG_endPeriods)[0][0])+1
            players = self.get_players()
            
            for p in players:
                p.connect(temp)

            random.shuffle(players)
            matrix = self.pairs(players)
            print("First Round of a Supergame:",matrix)

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

        p1,p2 = self.get_players() #List ordered by id_in_group
        roll = self.get_group_roll(self.round_number)
        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        temp = self.round_number
        
        if roundPos > 0:
            temp = self.round_number - Constants.SG_endPeriods[roundPos-1]

        p1.periodNumber = temp
        p1.roundNumber = roundPos + 1

        p1.rollHistory += ","+str(roll)
        p1.periodHistory += ","+str(temp)
        p1.roundHistory += ","+str(p1.roundNumber)

        p2.periodNumber = temp
        p2.roundNumber = roundPos + 1

        p2.rollHistory += ","+str(roll)
        p2.periodHistory += ","+str(temp)
        p2.roundHistory += ","+str(p2.roundNumber)

        p1.myPayoffR = Constants.payoff_matrix1[p1.myChoiceR][p2.myChoiceR]
        p1.myPayoffB = Constants.payoff_matrix2[p1.myChoiceB][p2.myChoiceB]
        p2.myPayoffR = Constants.payoff_matrix1[p2.myChoiceR][p1.myChoiceR]
        p2.myPayoffB = Constants.payoff_matrix2[p2.myChoiceB][p1.myChoiceB]

        p1.myChoiceHistoryR += ","+str(p1.myChoiceR)
        p1.myPayoffHistoryR += ","+str(p1.myPayoffR)
        p1.otherChoiceHistoryR += ","+str(p2.myChoiceR)
        p1.otherPayoffHistoryR += ","+str(p2.myPayoffR)

        p1.myChoiceHistoryB += ","+str(p1.myChoiceB)
        p1.myPayoffHistoryB += ","+str(p1.myPayoffB)
        p1.otherChoiceHistoryB += ","+str(p2.myChoiceB)
        p1.otherPayoffHistoryB += ","+str(p2.myPayoffB)

        p1.participant.vars["myChoiceHistoryR"] = p1.myChoiceHistoryR
        p1.participant.vars["myPayoffHistoryR"] = p1.myPayoffHistoryR
        p1.participant.vars["otherChoiceHistoryR"] = p1.otherChoiceHistoryR
        p1.participant.vars["otherPayoffHistoryR"] = p1.otherPayoffHistoryR
                 
        p1.participant.vars["myChoiceHistoryB"] = p1.myChoiceHistoryB
        p1.participant.vars["myPayoffHistoryB"] = p1.myPayoffHistoryB
        p1.participant.vars["otherChoiceHistoryB"] = p1.otherChoiceHistoryB
        p1.participant.vars["otherPayoffHistoryB"] = p1.otherPayoffHistoryB

        p2.myChoiceHistoryR += ","+str(p2.myChoiceR)
        p2.myPayoffHistoryR += ","+str(p2.myPayoffR)
        p2.otherChoiceHistoryR += ","+str(p1.myChoiceR)
        p2.otherPayoffHistoryR += ","+str(p1.myPayoffR)

        p2.myChoiceHistoryB += ","+str(p2.myChoiceB)
        p2.myPayoffHistoryB += ","+str(p2.myPayoffB)
        p2.otherChoiceHistoryB += ","+str(p1.myChoiceB)
        p2.otherPayoffHistoryB += ","+str(p1.myPayoffB)

        p2.participant.vars["myChoiceHistoryR"] = p2.myChoiceHistoryR
        p2.participant.vars["myPayoffHistoryR"] = p2.myPayoffHistoryR
        p2.participant.vars["otherChoiceHistoryR"] = p2.otherChoiceHistoryR
        p2.participant.vars["otherPayoffHistoryR"] = p2.otherPayoffHistoryR
                 
        p2.participant.vars["myChoiceHistoryB"] = p2.myChoiceHistoryB
        p2.participant.vars["myPayoffHistoryB"] = p2.myPayoffHistoryB
        p2.participant.vars["otherChoiceHistoryB"] = p2.otherChoiceHistoryB
        p2.participant.vars["otherPayoffHistoryB"] = p2.otherPayoffHistoryB

        for p in self.get_players():

            p.participant.vars["periodHistory"] = p.periodHistory
            p.participant.vars["roundHistory"] = p.roundHistory
            p.participant.vars["rollHistory"] = p.rollHistory

            p.participant.vars["roundPayoffHistory"][p.roundNumber] += p.myPayoffR+p.myPayoffB

            print("Payoff History:",p.participant.vars["roundPayoffHistory"])

            if self.round_number in Constants.SG_endPeriods:

                p.participant.vars["totalPayoff"] += p.participant.vars["roundPayoffHistory"][p.roundNumber]

                print("Cumulative Payoff:", p.participant.vars["totalPayoff"])

                p.myCumulativePayoff = p.participant.vars["totalPayoff"]

class Player(BasePlayer):
    
    ## Defining player variables

    myChoiceR = models.IntegerField()
    myPayoffR = models.CurrencyField()
    myChoiceHistoryR = models.StringField()
    myPayoffHistoryR = models.StringField()
    otherChoiceHistoryR = models.StringField()
    otherPayoffHistoryR = models.StringField()

    myChoiceB = models.IntegerField()
    myPayoffB = models.CurrencyField()
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
    myCumulativePayoff = models.CurrencyField()
    totalPeriod = models.IntegerField()
    timeout = models.IntegerField()

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
        print("Payoff History:",self.participant.vars["roundPayoffHistory"])
        self.participant.vars["totalPayoff"] += self.participant.vars["roundPayoffHistory"][self.roundNumber]
        print("Cumulative Payoff:", self.participant.vars["totalPayoff"])
        self.myCumulativePayoff = self.participant.vars["totalPayoff"]
        
        self.participant.vars["oddGroup"] = 0
