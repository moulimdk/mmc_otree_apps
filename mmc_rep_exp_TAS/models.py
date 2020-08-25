from shared_model import *

author = 'Mouli Modak'

doc = """
Experiment for Treatment Asymmetric Singlemarket Contact
"""

class Constants(BaseConstants):
    name_in_url = 'mmc_rep_exp_TAS'
    players_per_group = None

    ## Payoff Tables
    payoff_matrix1=settings.SESSION_CONFIGS[4].get('payoff_1') # Payoff matrix of setting 1
    payoff_matrix2=settings.SESSION_CONFIGS[4].get('payoff_2') # Payoff matrix of setting 2
    expPoints = {}
    expPoints["R"] = settings.SESSION_CONFIGS[4].get('expPoints_Red') # Expected Points matrix 1
    expPoints["B"] = settings.SESSION_CONFIGS[4].get('expPoints_Blue') # Expected Points matrix 2
    
    SG_lengths = settings.SESSION_CONFIGS[4].get('SG_lengths') # Number of periods in supergames
    SG_totalNum = len(SG_lengths) # Number of supergames
    SG_endPeriods = np.cumsum(SG_lengths) # End period for each supergame
    num_rounds = SG_endPeriods[-1] + 1 # Total number of rounds
    
    dieN = settings.SESSION_CONFIGS[4].get('die_N') #Number on a die
    contProb = settings.SESSION_CONFIGS[4].get('contProb') #Continuation probability in percentages
    endProb = 100 - contProb 
    thres = int(1+(dieN*contProb/100)); #Threshold number on a die

    participation_fee = settings.SESSION_CONFIGS[4].get('participation_fee') # Participation payment
    quiz_fee = settings.SESSION_CONFIGS[4].get('quiz_fee') # Quiz payment

    exRate = int(1/settings.SESSION_CONFIGS[4].get('real_world_currency_per_point')) # Exchange Rate (points to dollar)
    
    time_period = settings.SESSION_CONFIGS[4].get('time_period') # Total time alloted to a period
    time_begin = settings.SESSION_CONFIGS[4].get('time_welcome') # Time alloted in the first page
    time_next = settings.SESSION_CONFIGS[4].get('time_next') # Time to next round


class Subsession(BaseSubsession):
    
    def shuffle(self):
        
        if (self.round_number == 1) or (self.round_number-1 in Constants.SG_endPeriods):
            
            temp = int(np.where(self.round_number <= Constants.SG_endPeriods)[0][0])+1
            players = self.get_players()
            nonconnected = [p for p in players if (p.participant.vars["disconnected"] == 1)] 
            connected = [p for p in players if (p.participant.vars["disconnected"] == 0)]
            for p in connected:
                p.connect(temp)

            random.shuffle(connected)
            matrix = []
            if len(connected)%2 == 0:
                matrix.append(connected)
            else:
                matrix.append(connected[0:-1])
                matrix.append([connected[-1]])
            matrix.append(nonconnected)

            print("First Period of a supergame:",matrix)

            self.set_group_matrix(matrix)
            for group in self.get_groups():
                group.init_match()
        else:
            self.group_like_round(self.round_number-1)
            groups = self.get_groups()
            groups[0].period_outcome()

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

    # Get stage game variables
    def period_outcome(self):

        players = self.get_players() #List ordered by id_in_group
        nplayers = len(players)
        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        temp = self.round_number
        roll = self.get_group_roll(self.round_number-1)
        
        if roundPos > 0:
            temp = self.round_number - Constants.SG_endPeriods[roundPos-1]

        for i in range(int(nplayers)):

            me = players[i]
            other = players[(i+1)%nplayers]

            if (me.participant.vars["disconnected"] == 0) and (other.participant.vars["disconnected"] == 0):

                myActionB = me.in_round((self.round_number - 1)).myChoiceB
                otherRaction = other.in_round((self.round_number - 1)).myChoiceR
                me.mylastPayoffB = Constants.payoff_matrix2[myActionB][otherRaction]
                other.mylastPayoffR = Constants.payoff_matrix1[otherRaction][myActionB]

                me.myChoiceHistoryB = me.in_round((self.round_number - 1)).myChoiceHistoryB+","+str(myActionB)
                me.myPayoffHistoryB = me.in_round((self.round_number - 1)).myPayoffHistoryB+","+str(me.mylastPayoffB)
                me.otherChoiceHistoryB = me.in_round((self.round_number - 1)).otherChoiceHistoryB+","+str(otherRaction)
                me.otherPayoffHistoryB = me.in_round((self.round_number - 1)).otherPayoffHistoryB+","+str(other.mylastPayoffR)

                other.myChoiceHistoryR = other.in_round((self.round_number - 1)).myChoiceHistoryR+","+str(otherRaction)
                other.myPayoffHistoryR = other.in_round((self.round_number - 1)).myPayoffHistoryR+","+str(other.mylastPayoffR)
                other.otherChoiceHistoryR = other.in_round((self.round_number - 1)).otherChoiceHistoryR+","+str(myActionB)
                other.otherPayoffHistoryR = other.in_round((self.round_number - 1)).otherPayoffHistoryR+","+str(me.mylastPayoffB)
                
                me.participant.vars["myChoiceHistoryB"] = me.myChoiceHistoryB
                me.participant.vars["myPayoffHistoryB"] = me.myPayoffHistoryB
                me.participant.vars["otherChoiceHistoryB"] = me.otherChoiceHistoryB
                me.participant.vars["otherPayoffHistoryB"] = me.otherPayoffHistoryB

                other.participant.vars["myChoiceHistoryR"] = other.myChoiceHistoryR
                other.participant.vars["myPayoffHistoryR"] = other.myPayoffHistoryR
                other.participant.vars["otherChoiceHistoryR"] = other.otherChoiceHistoryR
                other.participant.vars["otherPayoffHistoryR"] = other.otherPayoffHistoryR

            if (me.participant.vars["disconnected"] == 0) and (other.participant.vars["disconnected"] == 1):

                if me.participant.vars["abandoned_B"] < 1:
                    me.participant.vars["abandoned"] += 0.5
                    me.participant.vars["abandoned_B"] = 1
                
                if me.participant.vars["abandoned"] == 1:
                    me.participant.vars["abandoned_period"] = self.round_number - 1

                myActionB = me.in_round((self.round_number - 1)).myChoiceB
                me.mylastPayoffB = Constants.expPoints["B"]

                me.myChoiceHistoryB = me.in_round((self.round_number - 1)).myChoiceHistoryB+","+str(myActionB)
                me.myPayoffHistoryB = me.in_round((self.round_number - 1)).myPayoffHistoryB+","+str(me.mylastPayoffB)
                me.otherChoiceHistoryB = me.in_round((self.round_number - 1)).otherChoiceHistoryB+","+str(2)
                me.otherPayoffHistoryB = me.in_round((self.round_number - 1)).otherPayoffHistoryB+","+"-"

                me.participant.vars["myChoiceHistoryB"] = me.myChoiceHistoryB
                me.participant.vars["myPayoffHistoryB"] = me.myPayoffHistoryB
                me.participant.vars["otherChoiceHistoryB"] = me.otherChoiceHistoryB
                me.participant.vars["otherPayoffHistoryB"] = me.otherPayoffHistoryB

            if (me.participant.vars["disconnected"] == 1) and (other.participant.vars["disconnected"] == 0):

                if other.participant.vars["abandoned_R"] < 1:
                    other.participant.vars["abandoned"] += 0.5
                    other.participant.vars["abandoned_R"] = 1
                
                if other.participant.vars["abandoned"] == 1:
                    other.participant.vars["abandoned_period"] = self.round_number - 1

                otherRaction = other.in_round((self.round_number - 1)).myChoiceR
                other.mylastPayoffR = Constants.expPoints["R"]

                other.myChoiceHistoryR = other.in_round((self.round_number - 1)).myChoiceHistoryR+","+str(otherRaction)
                other.myPayoffHistoryR = other.in_round((self.round_number - 1)).myPayoffHistoryR+","+str(other.mylastPayoffR)
                other.otherChoiceHistoryR = other.in_round((self.round_number - 1)).otherChoiceHistoryR+","+str(2)
                other.otherPayoffHistoryR = other.in_round((self.round_number - 1)).otherPayoffHistoryR+","+"-"
                
                other.participant.vars["myChoiceHistoryR"] = other.myChoiceHistoryR
                other.participant.vars["myPayoffHistoryR"] = other.myPayoffHistoryR
                other.participant.vars["otherChoiceHistoryR"] = other.otherChoiceHistoryR
                other.participant.vars["otherPayoffHistoryR"] = other.otherPayoffHistoryR

        for p in players:

            if p.participant.vars["disconnected"] == 0:

                p.periodNumber = temp
                p.roundNumber = roundPos + 1
                p.rollHistory = p.in_round((self.round_number - 1)).rollHistory+","+str(roll)
                p.periodHistory = p.in_round((self.round_number - 1)).periodHistory+","+str(temp-1)
                p.roundHistory = p.in_round((self.round_number - 1)).roundHistory+","+str(p.roundNumber)

                p.participant.vars["rollHistory"] = p.rollHistory
                p.participant.vars["periodHistory"] = p.periodHistory
                p.participant.vars["roundHistory"] = p.roundHistory
                
                p.participant.vars["roundPayoffHistory"][p.roundNumber] += p.mylastPayoffR+p.mylastPayoffB

    # Get end period game
    def end_period_outcome(self):

        players = self.get_players() #List ordered by id_in_group
        roll = self.get_group_roll(self.round_number)
        nplayers = len(players)
        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        temp = self.round_number
        
        if roundPos > 0:
            temp = self.round_number - Constants.SG_endPeriods[roundPos-1]

        for i in range(nplayers):

            me = players[i]
            other = players[(i+1)%nplayers]

            if (me.participant.vars["disconnected"] == 0) and (other.participant.vars["disconnected"] == 0):

                myActionB = me.myChoiceB
                otherRaction = other.myChoiceR
                me.mylastPayoffB = Constants.payoff_matrix2[myActionB][otherRaction]
                other.mylastPayoffR = Constants.payoff_matrix1[otherRaction][myActionB]

                me.myChoiceHistoryB = me.myChoiceHistoryB+","+str(myActionB)
                me.myPayoffHistoryB = me.myPayoffHistoryB+","+str(me.mylastPayoffB)
                me.otherChoiceHistoryB = me.otherChoiceHistoryB+","+str(otherRaction)
                me.otherPayoffHistoryB = me.otherPayoffHistoryB+","+str(other.mylastPayoffR)

                other.myChoiceHistoryR = other.myChoiceHistoryR+","+str(otherRaction)
                other.myPayoffHistoryR = other.myPayoffHistoryR+","+str(other.mylastPayoffR)
                other.otherChoiceHistoryR = other.otherChoiceHistoryR+","+str(myActionB)
                other.otherPayoffHistoryR = other.otherPayoffHistoryR+","+str(me.mylastPayoffB)
                
                me.participant.vars["myChoiceHistoryB"] = me.myChoiceHistoryB
                me.participant.vars["myPayoffHistoryB"] = me.myPayoffHistoryB
                me.participant.vars["otherChoiceHistoryB"] = me.otherChoiceHistoryB
                me.participant.vars["otherPayoffHistoryB"] = me.otherPayoffHistoryB

                other.participant.vars["myChoiceHistoryR"] = other.myChoiceHistoryR
                other.participant.vars["myPayoffHistoryR"] = other.myPayoffHistoryR
                other.participant.vars["otherChoiceHistoryR"] = other.otherChoiceHistoryR
                other.participant.vars["otherPayoffHistoryR"] = other.otherPayoffHistoryR

            if (me.participant.vars["disconnected"] == 0) and (other.participant.vars["disconnected"] == 1):

                if me.participant.vars["abandoned_B"] < 1:
                    me.participant.vars["abandoned"] += 0.5
                    me.participant.vars["abandoned_B"] = 1
                
                if me.participant.vars["abandoned"] == 1:
                    me.participant.vars["abandoned_period"] = self.round_number

                myActionB = me.myChoiceB
                me.mylastPayoffB = Constants.expPoints["B"]

                me.myChoiceHistoryB = me.myChoiceHistoryB+","+str(myActionB)
                me.myPayoffHistoryB = me.myPayoffHistoryB+","+str(me.mylastPayoffB)
                me.otherChoiceHistoryB = me.otherChoiceHistoryB+","+str(2)
                me.otherPayoffHistoryB = me.otherPayoffHistoryB+","+"-"

                me.participant.vars["myChoiceHistoryB"] = me.myChoiceHistoryB
                me.participant.vars["myPayoffHistoryB"] = me.myPayoffHistoryB
                me.participant.vars["otherChoiceHistoryB"] = me.otherChoiceHistoryB
                me.participant.vars["otherPayoffHistoryB"] = me.otherPayoffHistoryB

            if (me.participant.vars["disconnected"] == 1) and (other.participant.vars["disconnected"] == 0):

                if other.participant.vars["abandoned_R"] < 1:
                    other.participant.vars["abandoned"] += 0.5
                    other.participant.vars["abandoned_R"] = 1
                
                if other.participant.vars["abandoned"] == 1:
                    other.participant.vars["abandoned_period"] = self.round_number

                otherRaction = other.myChoiceR
                other.mylastPayoffR = Constants.expPoints["R"]

                other.myChoiceHistoryR = other.myChoiceHistoryR+","+str(otherRaction)
                other.myPayoffHistoryR = other.myPayoffHistoryR+","+str(other.mylastPayoffR)
                other.otherChoiceHistoryR = other.otherChoiceHistoryR+","+str(2)
                other.otherPayoffHistoryR = other.otherPayoffHistoryR+","+"-"
                
                other.participant.vars["myChoiceHistoryR"] = other.myChoiceHistoryR
                other.participant.vars["myPayoffHistoryR"] = other.myPayoffHistoryR
                other.participant.vars["otherChoiceHistoryR"] = other.otherChoiceHistoryR
                other.participant.vars["otherPayoffHistoryR"] = other.otherPayoffHistoryR

        for p in players:
            
            if p.participant.vars["disconnected"] == 0:
                p.periodNumber = temp
                p.roundNumber = roundPos + 1
                p.rollHistory = p.rollHistory+","+str(roll)
                p.periodHistory = p.periodHistory+","+str(temp)
                p.roundHistory = p.roundHistory+","+str(p.roundNumber)

                p.participant.vars["rollHistory"] = p.rollHistory
                p.participant.vars["periodHistory"] = p.periodHistory
                p.participant.vars["roundHistory"] = p.roundHistory

                p.participant.vars["roundPayoffHistory"][p.roundNumber] += p.mylastPayoffR+p.mylastPayoffB

                print("Payoff History:",p.participant.vars["roundPayoffHistory"])
                
                p.participant.vars["totalPayoff"] += p.participant.vars["roundPayoffHistory"][p.roundNumber]

                print("Cumulative Payoff:", p.participant.vars["totalPayoff"])

                p.myCumulativePayoff = p.participant.vars["totalPayoff"]

class Player(BasePlayer):
    
    ## Defining player variables

    myChoiceR = models.IntegerField()
    mylastPayoffR = models.FloatField()
    otherlastPayoffR = models.CurrencyField()
    myChoiceHistoryR = models.StringField()
    myPayoffHistoryR = models.StringField()
    otherChoiceHistoryR = models.StringField()
    otherPayoffHistoryR = models.StringField()

    myChoiceB = models.IntegerField()
    mylastPayoffB = models.FloatField()
    otherlastPayoffB = models.CurrencyField()
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
    numberPeriodsLeft = models.IntegerField()

    ## Player methods

    # Initialization of participant variables
    def connect(self,rN):

        if self.round_number == 1:
            self.participant.vars["roundPayoffHistory"] = {}
            self.participant.vars["roundPayoffHistory"][1] = 0
            self.participant.vars["totalPayoff"] = 0
            self.participant.vars["disconnected"] = 0
        else:
            self.participant.vars["roundPayoffHistory"][rN] = 0
            self.participant.vars["abandoned"] = 0
            self.participant.vars["abandoned_R"] = 0
            self.participant.vars["abandoned_B"] = 0
            self.participant.vars["oddGroup"] = 0
            self.participant.vars["disconnected_period"] = 0
            self.participant.vars["abandoned_period"] = 0

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

    # Method for abandoned players
    def abandonedPlayerPayoff(self):

        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        self.roundNumber = int(roundPos) + 1
        self.numberPeriodsLeft = int(Constants.SG_endPeriods[roundPos] - self.participant.vars["abandoned_period"])

        self.participant.vars["roundPayoffHistory"][self.roundNumber] = self.numberPeriodsLeft*(Constants.expPoints["R"]+Constants.expPoints["B"])
        print("Payoff History:",self.participant.vars["roundPayoffHistory"])
        self.participant.vars["totalPayoff"] += self.participant.vars["roundPayoffHistory"][self.roundNumber]
        print("Cumulative Payoff:", self.participant.vars["totalPayoff"])
        self.myCumulativePayoff = self.participant.vars["totalPayoff"]
        
        self.participant.vars["abandoned"] = 0
        self.participant.vars["abandoned_R"] = 0
        self.participant.vars["abandoned_B"] = 0