from shared_model import *


author = 'Mouli Modak'

doc = """
Introduction and Quiz to Multimarket Contact experiment Treatment T-SSym
"""

def frame_question(contProb, num_matches, time_quiz, time_round, time_intro, expPoints_Red, payoff_matrix1, payoff_matrix2):
    questions = {}
    for i in range(8):
        questions[i+1]={}

    questions[1]['ans'] = models.IntegerField(initial=2)
    questions[1]['statement'] = models.StringField(initial="A Round is in the 4th Period. What is the probability that the Round will move to the next Period?")
    questions[1]['choices'] = models.IntegerField(
        choices=[
            [1, "100%"],
            [2, str(contProb)+"%"],
            [3, str(100-contProb)+"%"],
            [4, "0%"],
        ],
        widget=widgets.RadioSelect
    )


    questions[2]['ans'] = models.IntegerField(initial=4)
    questions[2]['statement'] = models.StringField(initial="How many Periods is a Round made up of?")
    questions[2]['choices'] = models.IntegerField(
        choices=[
            [1, str(num_matches)+" periods"],
            [2, "4 periods"],
            [3, "1 period"],
            [4, "Random Number of periods"],
        ],
        widget=widgets.RadioSelect
    )

    questions[3]['ans'] = models.IntegerField(initial=4)
    questions[3]['statement'] = models.StringField(initial="If you can not be paired in a Round, how many points will you receive in each period in Red Game? Please choose the last option.")
    questions[3]['choices'] = models.IntegerField(
        choices=[
            [1, str(48)],
            [2, str(12)],
            [3, str(expPoints_Red)],
            [4, str(expPoints_Red)],
        ],
        widget=widgets.RadioSelect
    )


    questions[4]['ans'] = models.IntegerField(initial=1)
    questions[4]['statement'] = models.StringField(initial="In a Period, if you choose Action A and Other Red chooses Action A in Red Game, then how many points will you receive in Red Game? (Refer to the Points Tables above)")
    questions[4]['choices'] = models.IntegerField(
        choices=[
            [1, str(payoff_matrix1[0][0])],
            [2, str(payoff_matrix1[0][1])],
            [3, str(payoff_matrix1[1][0])],
            [4, str(payoff_matrix1[1][1])],
        ],
        widget=widgets.RadioSelect
    )

    questions[5]['ans'] = models.IntegerField(initial=3)
    questions[5]['statement'] = models.StringField(initial="In Period 2, how many points did Other Red receive in Red Game? (Refer to the History Tables above)")
    questions[5]['choices'] = models.IntegerField(
        choices=[
            [1, str(payoff_matrix1[0][0])],
            [2, str(payoff_matrix1[0][1])],
            [3, str(payoff_matrix1[1][0])],
            [4, str(payoff_matrix1[1][1])],
        ],
        widget=widgets.RadioSelect
    )

    questions[6]['ans'] = models.IntegerField(initial=2)
    questions[6]['statement'] = models.StringField(initial="In a Period, if you choose Action W and Other Blue chooses Action Y in Blue Game, then how many points will you receive in Blue Game? (Refer to the Points Tables above)")
    questions[6]['choices'] = models.IntegerField(
        choices=[
            [1, str(payoff_matrix2[0][0])],
            [2, str(payoff_matrix2[0][1])],
            [3, str(payoff_matrix2[1][0])],
            [4, str(payoff_matrix2[1][1])],
        ],
        widget=widgets.RadioSelect
    )


    questions[7]['ans'] = models.IntegerField(initial=1)
    questions[7]['statement'] = models.StringField(initial="In Period 4, which Action was chosen by Other Blue in Blue Game? (Refer to the History Tables above)")
    questions[7]['choices'] = models.IntegerField(
        choices=[
            [1, "Y"],
            [2, "W"],
            [3, "A"],
            [4, "B"],
        ],
        widget=widgets.RadioSelect
    )

    questions[8]['ans'] = models.IntegerField(initial=4)
    questions[8]['statement'] = models.StringField(initial="In Period 3, which Action was chosen by Other Red in Red Game? (Refer to the History Tables above)")
    questions[8]['choices'] = models.IntegerField(
        choices=[
            [1, "Y"],
            [2, "W"],
            [3, "A"],
            [4, "B"],
        ],
        widget=widgets.RadioSelect
    )

    return questions

    
class Constants(BaseConstants):
    name_in_url = 'mmc_rep_intro_TSS'
    players_per_group = None
    num_rounds = 1#Number of rounds for this app
    
    #Properties of session imported from session configurations
    num_matches = settings.SESSION_CONFIGS[0].get('SG_totalNum') #Total Number of Supergames
    
    dieN = settings.SESSION_CONFIGS[0].get('die_N') #Number on a die
    contProb = settings.SESSION_CONFIGS[0].get('contProb') #Continuation probability in percentages
    endProb = 100 - contProb 
    thres = int(1+(dieN*contProb/100)); #Threshold number on a die
    
    payoff_matrix1=settings.SESSION_CONFIGS[0].get('payoff_1') #Payoff matrix of setting 1
    payoff_matrix2=settings.SESSION_CONFIGS[0].get('payoff_2') #Payoff matrix of setting 2
    
    participation_fee = settings.SESSION_CONFIGS[0].get('participation_fee') #Participation payment
    quiz_fee = settings.SESSION_CONFIGS[0].get('quiz_fee') #Quiz payment
    avg_earn = settings.SESSION_CONFIGS[0].get('avg_earn') #Average Earning
    low_earn = settings.SESSION_CONFIGS[0].get('low_earn') #Low Earning
    high_earn = settings.SESSION_CONFIGS[0].get('high_earn') #High Earning
    expPoints_Red = settings.SESSION_CONFIGS[0].get('expPoints_Red') #Expected Points for Red Game
    expPoints_Blue = settings.SESSION_CONFIGS[0].get('expPoints_Blue') #Expected Points for Blue Game

    exRate = int(1/settings.SESSION_CONFIGS[0].get('real_world_currency_per_point')) #Exchange Rate (points to dollar)
    
    minExpTime = settings.SESSION_CONFIGS[0].get('minExpTime') #Min Expected time of the session
    maxExpTime = settings.SESSION_CONFIGS[0].get('maxExpTime') #Max Expected time of the session
    time_welcome = settings.SESSION_CONFIGS[0].get('time_welcome') #Time alloted to first page
    time_quiz = settings.SESSION_CONFIGS[0].get('time_quiz') #Total time alloted to the quiz
    time_round = settings.SESSION_CONFIGS[0].get('time_round') #Total time alloted to a round
    time_intro = settings.SESSION_CONFIGS[0].get('time_intro') #Time alloted to instructions
    
    num_ques = settings.SESSION_CONFIGS[0].get('num_ques') #Number of questions in the quiz
    
    questions = frame_question(contProb, num_matches, time_quiz, time_round, time_intro, expPoints_Red, payoff_matrix1, payoff_matrix2)


class Subsession(BaseSubsession):
    
    def creating_session(self):
        for p in self.get_players():
            p.participant.vars["disconnected"] = 0
            print(p.participant.vars["disconnected"])
            p.participant.vars["myCorrectAns"] = 0

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    
    ans_choice_1 = Constants.questions[1]['choices']
    ans_choice_2 = Constants.questions[2]['choices']
    ans_choice_3 = Constants.questions[3]['choices']
    ans_choice_4 = Constants.questions[4]['choices']
    ans_choice_5 = Constants.questions[5]['choices']
    ans_choice_6 = Constants.questions[6]['choices']
    ans_choice_7 = Constants.questions[7]['choices']
    ans_choice_8 = Constants.questions[8]['choices']

    correct_ans_1 = Constants.questions[1]['ans']
    correct_ans_2 = Constants.questions[2]['ans']
    correct_ans_3 = Constants.questions[3]['ans']
    correct_ans_4 = Constants.questions[4]['ans']
    correct_ans_5 = Constants.questions[5]['ans']
    correct_ans_6 = Constants.questions[6]['ans']
    correct_ans_7 = Constants.questions[7]['ans']
    correct_ans_8 = Constants.questions[8]['ans']

    ques_stat_1 = Constants.questions[1]['statement']
    ques_stat_2 = Constants.questions[2]['statement']
    ques_stat_3 = Constants.questions[3]['statement']
    ques_stat_4 = Constants.questions[4]['statement']
    ques_stat_5 = Constants.questions[5]['statement']
    ques_stat_6 = Constants.questions[6]['statement']
    ques_stat_7 = Constants.questions[7]['statement']
    ques_stat_8 = Constants.questions[8]['statement']

    myCorrectAns = models.IntegerField(initial=0)
    myQuizStatus = models.BooleanField(initial=0)
    myQuizPay = models.FloatField(initial=0)


    def answer_check(self):
        if self.ans_choice_1 == self.correct_ans_1:
            self.myCorrectAns += 1
        if self.ans_choice_2 == self.correct_ans_2:
            self.myCorrectAns += 1
        if self.ans_choice_3 == self.correct_ans_3:
            self.myCorrectAns += 1
        if self.ans_choice_4 == self.correct_ans_4:
            self.myCorrectAns += 1
        if self.ans_choice_5 == self.correct_ans_5:
            self.myCorrectAns += 1
        if self.ans_choice_6 == self.correct_ans_6:
            self.myCorrectAns += 1
        if self.ans_choice_7 == self.correct_ans_7:
            self.myCorrectAns += 1
        if self.ans_choice_8 == self.correct_ans_8:
            self.myCorrectAns += 1
        
        self.myQuizPay = Constants.quiz_fee*self.myCorrectAns
        
        self.participant.vars["myCorrectAns"] = self.myCorrectAns
