from shared_model import *

author = 'Mouli Modak'


doc = """
Experiment for Treatment Symmetric Multimarket Contact
"""

class Constants(BaseConstants):
    name_in_url = 'mmc_rep_exp_TSM'
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
    thres = int(1+(dieN*contProb/100)); #Threshold number on a die

    participation_fee = settings.SESSION_CONFIGS[2].get('participation_fee') # Participation payment
    quiz_fee = settings.SESSION_CONFIGS[2].get('quiz_fee') # Quiz payment

    exRate = int(1/settings.SESSION_CONFIGS[2].get('real_world_currency_per_point')) # Exchange Rate (points to dollar)
    
    time_period = settings.SESSION_CONFIGS[2].get('time_period') # Total time alloted to a period
    time_begin = settings.SESSION_CONFIGS[2].get('time_welcome') # Time alloted in the first page
    time_next = settings.SESSION_CONFIGS[2].get('time_next') # Time to next round


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
        #Grouping by two types
        if (self.round_number == 1) or (self.round_number-1 in Constants.SG_endPeriods):
            
            temp = int(np.where(self.round_number <= Constants.SG_endPeriods)[0][0])+1
            players = self.get_players()
            nonconnected = [p for p in players if (p.participant.vars["disconnected"] == 1)] 
            connected = [p for p in players if (p.participant.vars["disconnected"] == 0)]
            for p in connected:
                p.connect(temp)

            random.shuffle(connected)
            matrix = self.pairs(connected)
            matrix.append(nonconnected)

            print("First Round of a Supergame:",matrix)

            self.set_group_matrix(matrix)
            for group in self.get_groups():
                group.init_match()

        else:
            self.group_like_round(self.round_number-1)
            groups = self.get_groups()
            for g in groups:
                if len(g.get_players()) == 2:
                    g.period_outcome()

    def end_round_outcome(self):
        groups = self.get_groups()
        rev_groups = groups[0:-1]
        for g in rev_groups:
            if len(g.get_players()) == 2:
                g.end_round_update()

    def creating_session(self):
        players = self.get_players()
        for p in players:
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
        p1, p2 = self.get_players()

        if (p1.participant.vars["disconnected"] == 0) & (p2.participant.vars["disconnected"] == 0):

            p1.roundNumber = roundPos + 1
            p1.periodNumber = p1.round_number
            if roundPos > 0:
                p1.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p1.periodHistory = p1.in_round((self.round_number - 1)).periodHistory+","+str(p1.periodNumber-1)
            p1.roundHistory = p1.in_round((self.round_number - 1)).roundHistory+","+str(p1.roundNumber)
            p1.rollHistory = p1.in_round((self.round_number - 1)).rollHistory+","+str(roll)

            p2.roundNumber = roundPos + 1
            p2.periodNumber = p2.round_number
            if roundPos > 0:
                p2.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p2.periodHistory = p2.in_round((self.round_number - 1)).periodHistory+","+str(p2.periodNumber-1)
            p2.roundHistory = p2.in_round((self.round_number - 1)).roundHistory+","+str(p2.roundNumber)
            p2.rollHistory = p2.in_round((self.round_number - 1)).rollHistory+","+str(roll)

            p1lastChoiceR = p1.in_round((self.round_number - 1)).myChoiceR
            p1lastChoiceB = p1.in_round((self.round_number - 1)).myChoiceB
            p2lastChoiceR = p2.in_round((self.round_number - 1)).myChoiceR
            p2lastChoiceB = p2.in_round((self.round_number - 1)).myChoiceB

            p1lastPayoffR = Constants.payoff_matrix1[p1lastChoiceR][p2lastChoiceR]
            p1lastPayoffB = Constants.payoff_matrix2[p1lastChoiceB][p2lastChoiceB]
            p2lastPayoffR = Constants.payoff_matrix1[p2lastChoiceR][p1lastChoiceR]
            p2lastPayoffB = Constants.payoff_matrix2[p2lastChoiceB][p1lastChoiceB]

            p1.myChoiceHistoryR = p1.in_round((self.round_number - 1)).myChoiceHistoryR+","+str(p1lastChoiceR)
            p1.myChoiceHistoryB = p1.in_round((self.round_number - 1)).myChoiceHistoryB+","+str(p1lastChoiceB)
            p1.myPayoffHistoryR = p1.in_round((self.round_number - 1)).myPayoffHistoryR+","+str(p1lastPayoffR)
            p1.myPayoffHistoryB = p1.in_round((self.round_number - 1)).myPayoffHistoryB+","+str(p1lastPayoffB)
            p1.otherChoiceHistoryR = p1.in_round((self.round_number - 1)).otherChoiceHistoryR+","+str(p2lastChoiceR)
            p1.otherChoiceHistoryB = p1.in_round((self.round_number - 1)).otherChoiceHistoryB+","+str(p2lastChoiceB)
            p1.otherPayoffHistoryR = p1.in_round((self.round_number - 1)).otherPayoffHistoryR+","+str(p2lastPayoffR)
            p1.otherPayoffHistoryB = p1.in_round((self.round_number - 1)).otherPayoffHistoryB+","+str(p2lastPayoffB)

            p2.myChoiceHistoryR = p2.in_round((self.round_number - 1)).myChoiceHistoryR+","+str(p2lastChoiceR)
            p2.myChoiceHistoryB = p2.in_round((self.round_number - 1)).myChoiceHistoryB+","+str(p2lastChoiceB)
            p2.myPayoffHistoryR = p2.in_round((self.round_number - 1)).myPayoffHistoryR+","+str(p2lastPayoffR)
            p2.myPayoffHistoryB = p2.in_round((self.round_number - 1)).myPayoffHistoryB+","+str(p2lastPayoffB)
            p2.otherChoiceHistoryR = p2.in_round((self.round_number - 1)).otherChoiceHistoryR+","+str(p1lastChoiceR)
            p2.otherChoiceHistoryB = p2.in_round((self.round_number - 1)).otherChoiceHistoryB+","+str(p1lastChoiceB)
            p2.otherPayoffHistoryR = p2.in_round((self.round_number - 1)).otherPayoffHistoryR+","+str(p1lastPayoffR)
            p2.otherPayoffHistoryB = p2.in_round((self.round_number - 1)).otherPayoffHistoryB+","+str(p1lastPayoffB)

            p1.participant.vars["myChoiceHistoryR"] = p1.myChoiceHistoryR
            p1.participant.vars["myChoiceHistoryB"] = p1.myChoiceHistoryB
            p1.participant.vars["myPayoffHistoryR"] = p1.myPayoffHistoryR
            p1.participant.vars["myPayoffHistoryB"] = p1.myPayoffHistoryB
            p1.participant.vars["otherChoiceHistoryR"] = p1.otherChoiceHistoryR
            p1.participant.vars["otherChoiceHistoryB"] = p1.otherChoiceHistoryB
            p1.participant.vars["otherPayoffHistoryR"] = p1.otherPayoffHistoryR
            p1.participant.vars["otherPayoffHistoryB"] = p1.otherPayoffHistoryB
            p1.participant.vars["rollHistory"] = p1.rollHistory
            p1.participant.vars["periodHistory"] = p1.periodHistory
            p1.participant.vars["roundHistory"] = p1.roundHistory

            p2.participant.vars["myChoiceHistoryR"] = p2.myChoiceHistoryR
            p2.participant.vars["myChoiceHistoryB"] = p2.myChoiceHistoryB
            p2.participant.vars["myPayoffHistoryR"] = p2.myPayoffHistoryR
            p2.participant.vars["myPayoffHistoryB"] = p2.myPayoffHistoryB
            p2.participant.vars["otherChoiceHistoryR"] = p2.otherChoiceHistoryR
            p2.participant.vars["otherChoiceHistoryB"] = p2.otherChoiceHistoryB
            p2.participant.vars["otherPayoffHistoryR"] = p2.otherPayoffHistoryR
            p2.participant.vars["otherPayoffHistoryB"] = p2.otherPayoffHistoryB
            p2.participant.vars["rollHistory"] = p2.rollHistory
            p2.participant.vars["periodHistory"] = p2.periodHistory
            p2.participant.vars["roundHistory"] = p2.roundHistory

            p1.participant.vars["roundPayoffHistory"][p1.roundNumber] += p1lastPayoffR+p1lastPayoffB
            p2.participant.vars["roundPayoffHistory"][p2.roundNumber] += p2lastPayoffR+p2lastPayoffB
            


        elif (p1.participant.vars["disconnected"] == 0) & (p1.participant.vars["abandoned"] == 0) & (p2.participant.vars["disconnected"] == 1):

            p1.roundNumber = roundPos + 1
            p1.periodNumber = p1.round_number
            if roundPos > 0:
                p1.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p1.periodHistory = p1.in_round((self.round_number - 1)).periodHistory+","+str(p1.periodNumber-1)
            p1.roundHistory = p1.in_round((self.round_number - 1)).roundHistory+","+str(p1.roundNumber)
            p1.rollHistory = p1.in_round((self.round_number - 1)).rollHistory+","+str(roll)

            p1lastChoiceR = p1.in_round((self.round_number - 1)).myChoiceR
            p1lastChoiceB = p1.in_round((self.round_number - 1)).myChoiceB
            p1lastPayoffR = Constants.expPoints["R"]
            p1lastPayoffB = Constants.expPoints["B"]

            p1.myChoiceHistoryR = p1.in_round((self.round_number - 1)).myChoiceHistoryR+","+str(p1lastChoiceR)
            p1.myChoiceHistoryB = p1.in_round((self.round_number - 1)).myChoiceHistoryB+","+str(p1lastChoiceB)
            p1.myPayoffHistoryR = p1.in_round((self.round_number - 1)).myPayoffHistoryR+","+str(p1lastPayoffR)
            p1.myPayoffHistoryB = p1.in_round((self.round_number - 1)).myPayoffHistoryB+","+str(p1lastPayoffB)
            p1.otherChoiceHistoryR = p1.in_round((self.round_number - 1)).otherChoiceHistoryR+","+str(2)
            p1.otherChoiceHistoryB = p1.in_round((self.round_number - 1)).otherChoiceHistoryB+","+str(2)
            p1.otherPayoffHistoryR = p1.in_round((self.round_number - 1)).otherPayoffHistoryR+","+"-"
            p1.otherPayoffHistoryB = p1.in_round((self.round_number - 1)).otherPayoffHistoryB+","+"-"

            p1.participant.vars["abandoned"] = 1
            p1.participant.vars["abandoned_period"] = p2.participant.vars["disconnected_period"]

            p1.participant.vars["myChoiceHistoryR"] = p1.myChoiceHistoryR
            p1.participant.vars["myChoiceHistoryB"] = p1.myChoiceHistoryB
            p1.participant.vars["myPayoffHistoryR"] = p1.myPayoffHistoryR
            p1.participant.vars["myPayoffHistoryB"] = p1.myPayoffHistoryB
            p1.participant.vars["otherChoiceHistoryR"] = p1.otherChoiceHistoryR
            p1.participant.vars["otherChoiceHistoryB"] = p1.otherChoiceHistoryB
            p1.participant.vars["otherPayoffHistoryR"] = p1.otherPayoffHistoryR
            p1.participant.vars["otherPayoffHistoryB"] = p1.otherPayoffHistoryB
            p1.participant.vars["rollHistory"] = p1.rollHistory
            p1.participant.vars["periodHistory"] = p1.periodHistory
            p1.participant.vars["roundHistory"] = p1.roundHistory
            
            p1.participant.vars["roundPayoffHistory"][p1.roundNumber] += p1lastPayoffR+p1lastPayoffB 

        elif (p1.participant.vars["disconnected"] == 1) & (p2.participant.vars["disconnected"] == 0) & (p2.participant.vars["abandoned"] == 0):

            p2.roundNumber = roundPos + 1
            p2.periodNumber = p2.round_number
            if roundPos > 0:
                p2.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p2.periodHistory = p2.in_round((self.round_number - 1)).periodHistory+","+str(p2.periodNumber-1)
            p2.roundHistory = p2.in_round((self.round_number - 1)).roundHistory+","+str(p2.roundNumber)
            p2.rollHistory = p2.in_round((self.round_number - 1)).rollHistory+","+str(roll)

            p2lastChoiceR = p2.in_round((self.round_number - 1)).myChoiceR
            p2lastChoiceB = p2.in_round((self.round_number - 1)).myChoiceB
            p2lastPayoffR = Constants.expPoints["R"]
            p2lastPayoffB = Constants.expPoints["B"]

            p2.myChoiceHistoryR = p2.in_round((self.round_number - 1)).myChoiceHistoryR+","+str(p2lastChoiceR)
            p2.myChoiceHistoryB = p2.in_round((self.round_number - 1)).myChoiceHistoryB+","+str(p2lastChoiceB)
            p2.myPayoffHistoryR = p2.in_round((self.round_number - 1)).myPayoffHistoryR+","+str(p2lastPayoffR)
            p2.myPayoffHistoryB = p2.in_round((self.round_number - 1)).myPayoffHistoryB+","+str(p2lastPayoffB)
            p2.otherChoiceHistoryR = p2.in_round((self.round_number - 1)).otherChoiceHistoryR+","+str(2)
            p2.otherChoiceHistoryB = p2.in_round((self.round_number - 1)).otherChoiceHistoryB+","+str(2)
            p2.otherPayoffHistoryR = p2.in_round((self.round_number - 1)).otherPayoffHistoryR+","+"-"
            p2.otherPayoffHistoryB = p2.in_round((self.round_number - 1)).otherPayoffHistoryB+","+"-"

            p2.participant.vars["abandoned"] = 1
            p2.participant.vars["abandoned_period"] = p1.participant.vars["disconnected_period"]

            p2.participant.vars["myChoiceHistoryR"] = p2.myChoiceHistoryR
            p2.participant.vars["myChoiceHistoryB"] = p2.myChoiceHistoryB
            p2.participant.vars["myPayoffHistoryR"] = p2.myPayoffHistoryR
            p2.participant.vars["myPayoffHistoryB"] = p2.myPayoffHistoryB
            p2.participant.vars["otherChoiceHistoryR"] = p2.otherChoiceHistoryR
            p2.participant.vars["otherChoiceHistoryB"] = p2.otherChoiceHistoryB
            p2.participant.vars["otherPayoffHistoryR"] = p2.otherPayoffHistoryR
            p2.participant.vars["otherPayoffHistoryB"] = p2.otherPayoffHistoryB
            p2.participant.vars["rollHistory"] = p2.rollHistory
            p2.participant.vars["periodHistory"] = p2.periodHistory
            p2.participant.vars["roundHistory"] = p2.roundHistory
            
            p2.participant.vars["roundPayoffHistory"][p2.roundNumber] += p2lastPayoffR+p2lastPayoffB


    def end_period_outcome(self):
        
        roll = self.get_group_roll(self.round_number)
        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]

        p1, p2 = self.get_players()

        if (p1.participant.vars["disconnected"] == 0) & (p2.participant.vars["disconnected"] == 0):

            p1.roundNumber = roundPos + 1
            p1.periodNumber = p1.round_number
            if roundPos > 0:
                p1.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p1.periodHistory += ","+str(p1.periodNumber)
            p1.roundHistory += ","+str(p1.roundNumber)
            p1.rollHistory += ","+str(roll)

            p2.roundNumber = roundPos + 1
            p2.periodNumber = p2.round_number
            if roundPos > 0:
                p2.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p2.periodHistory += ","+str(p2.periodNumber)
            p2.roundHistory += ","+str(p2.roundNumber)
            p2.rollHistory += ","+str(roll)

            p1lastChoiceR = p1.myChoiceR
            p1lastChoiceB = p1.myChoiceB
            p2lastChoiceR = p2.myChoiceR
            p2lastChoiceB = p2.myChoiceB

            p1lastPayoffR = Constants.payoff_matrix1[p1lastChoiceR][p2lastChoiceR]
            p1lastPayoffB = Constants.payoff_matrix2[p1lastChoiceB][p2lastChoiceB]
            p2lastPayoffR = Constants.payoff_matrix1[p2lastChoiceR][p1lastChoiceR]
            p2lastPayoffB = Constants.payoff_matrix2[p2lastChoiceB][p1lastChoiceB]

            p1.myChoiceHistoryR += ","+str(p1lastChoiceR)
            p1.myChoiceHistoryB += ","+str(p1lastChoiceB)
            p1.myPayoffHistoryR += ","+str(p1lastPayoffR)
            p1.myPayoffHistoryB += ","+str(p1lastPayoffB)
            p1.otherChoiceHistoryR += ","+str(p2lastChoiceR)
            p1.otherChoiceHistoryB += ","+str(p2lastChoiceB)
            p1.otherPayoffHistoryR += ","+str(p2lastPayoffR)
            p1.otherPayoffHistoryB += ","+str(p2lastPayoffB)

            p2.myChoiceHistoryR += ","+str(p2lastChoiceR)
            p2.myChoiceHistoryB += ","+str(p2lastChoiceB)
            p2.myPayoffHistoryR += ","+str(p2lastPayoffR)
            p2.myPayoffHistoryB += ","+str(p2lastPayoffB)
            p2.otherChoiceHistoryR += ","+str(p1lastChoiceR)
            p2.otherChoiceHistoryB += ","+str(p1lastChoiceB)
            p2.otherPayoffHistoryR += ","+str(p1lastPayoffR)
            p2.otherPayoffHistoryB += ","+str(p1lastPayoffB)

            p1.participant.vars["roundPayoffHistory"][p1.roundNumber] += p1lastPayoffR+p1lastPayoffB
            p2.participant.vars["roundPayoffHistory"][p2.roundNumber] += p2lastPayoffR+p2lastPayoffB

            p1.participant.vars["totalPayoff"] += p1.participant.vars["roundPayoffHistory"][p1.roundNumber]
            p2.participant.vars["totalPayoff"] += p2.participant.vars["roundPayoffHistory"][p2.roundNumber]

            p1.myCumulativePayoff = p1.participant.vars["totalPayoff"]
            p2.myCumulativePayoff = p2.participant.vars["totalPayoff"]
            
            print("Payoff History:",p1.participant.vars["roundPayoffHistory"])
            print("Payoff History:",p2.participant.vars["roundPayoffHistory"])

            print("Cumulative Payoff:", p1.participant.vars["totalPayoff"])
            print("Cumulative Payoff:", p2.participant.vars["totalPayoff"])

        elif (p1.participant.vars["disconnected"] == 0) & (p1.participant.vars["abandoned"] == 0) & (p2.participant.vars["disconnected"] == 1):

            p1.roundNumber = roundPos + 1
            p1.periodNumber = p1.round_number
            if roundPos > 0:
                p1.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p1.periodHistory += ","+str(p1.periodNumber)
            p1.roundHistory += ","+str(p1.roundNumber)
            p1.rollHistory += ","+str(roll)

            p1lastChoiceR = p1.myChoiceR
            p1lastChoiceB = p1.myChoiceB
            p1lastPayoffR = Constants.expPoints["R"]
            p1lastPayoffB = Constants.expPoints["B"]

            p1.myChoiceHistoryR += ","+str(p1lastChoiceR)
            p1.myChoiceHistoryB += ","+str(p1lastChoiceB)
            p1.myPayoffHistoryR += ","+str(p1lastPayoffR)
            p1.myPayoffHistoryB += ","+str(p1lastPayoffB)
            p1.otherChoiceHistoryR += ","+str(2)
            p1.otherChoiceHistoryB += ","+str(2)
            p1.otherPayoffHistoryR += ","+"-"
            p1.otherPayoffHistoryB += ","+"-"

            p1.participant.vars["roundPayoffHistory"][p1.roundNumber] += p1lastPayoffR+p1lastPayoffB

            p1.participant.vars["totalPayoff"] += p1.participant.vars["roundPayoffHistory"][p1.roundNumber]
            
            p1.myCumulativePayoff = p1.participant.vars["totalPayoff"]
            
            print("Payoff History:",p1.participant.vars["roundPayoffHistory"])
            
            print("Cumulative Payoff:", p1.participant.vars["totalPayoff"])
            
        elif (p1.participant.vars["disconnected"] == 1) & (p2.participant.vars["disconnected"] == 0) & (p2.participant.vars["abandoned"] == 0):

            p2.roundNumber = roundPos + 1
            p2.periodNumber = p2.round_number
            
            if roundPos > 0:
                p2.periodNumber = self.round_number - Constants.SG_endPeriods[roundPos-1]
        
            p2.periodHistory += ","+str(p2.periodNumber)
            p2.roundHistory += ","+str(p2.roundNumber)
            p2.rollHistory += ","+str(roll)

            p2lastChoiceR = p2.myChoiceR
            p2lastChoiceB = p2.myChoiceB
            p2lastPayoffR = Constants.expPoints["R"]
            p2lastPayoffB = Constants.expPoints["B"]

            p2.myChoiceHistoryR += ","+str(p2lastChoiceR)
            p2.myChoiceHistoryB += ","+str(p2lastChoiceB)
            p2.myPayoffHistoryR += ","+str(p2lastPayoffR)
            p2.myPayoffHistoryB += ","+str(p2lastPayoffB)
            p2.otherChoiceHistoryR += ","+str(2)
            p2.otherChoiceHistoryB += ","+str(2)
            p2.otherPayoffHistoryR += ","+"-"
            p2.otherPayoffHistoryB += ","+"-"

            p2.participant.vars["roundPayoffHistory"][p2.roundNumber] += p2lastPayoffR+p2lastPayoffB

            p2.participant.vars["totalPayoff"] += p2.participant.vars["roundPayoffHistory"][p2.roundNumber]

            p2.myCumulativePayoff = p2.participant.vars["totalPayoff"]
            
            print("Payoff History:",p2.participant.vars["roundPayoffHistory"])

            print("Cumulative Payoff:", p2.participant.vars["totalPayoff"])

        p1.participant.vars["abandoned"] = 0
        p2.participant.vars["abandoned"] = 0        


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