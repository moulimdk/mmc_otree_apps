from shared_model import *


author = 'Mouli Modak'

doc = """
Introduction and Quiz to Multimarket Contact experiment Treatment T-SAsym (Laboratory)
"""


def frame_question(choices_prob, choices_actions, choices_periods, choices_part, choices_P1, choices_P2):
    questions = {}
    for i in range(8):
        questions[i+1] = {}

    questions[1]['ans'] = models.IntegerField(initial=2)
    questions[1]['statement'] = models.StringField(initial="A Round is in the 4th Period. What is the probability that the Round will move to the next Period?")
    questions[1]['choices'] = models.IntegerField(
        choices=choices_prob,
        widget=widgets.RadioSelect
    )

    questions[2]['ans'] = models.IntegerField(initial=4)
    questions[2]['statement'] = models.StringField(initial="How many Periods is a Round made up of?")
    questions[2]['choices'] = models.IntegerField(
        choices=choices_periods,
        widget=widgets.RadioSelect
    )

    questions[3]['ans'] = models.IntegerField(initial=1)
    questions[3]['statement'] = models.StringField(initial="How many randomly chosen participants are you paired with in a Round?")
    questions[3]['choices'] = models.IntegerField(
        choices=choices_part,
        widget=widgets.RadioSelect
    )

    questions[4]['ans'] = models.IntegerField(initial=1)
    questions[4]['statement'] = models.StringField(initial="In a Period, if you choose Action A and Other Red chooses Action A in Red Game, then how many points will you receive in Red Game? (Refer to the Points Tables above)")
    questions[4]['choices'] = models.IntegerField(
        choices=choices_P1,
        widget=widgets.RadioSelect
    )

    questions[5]['ans'] = models.IntegerField(initial=1)
    questions[5]['statement'] = models.StringField(initial="In Period 1, how many points did Other Red receive in Red Game? (Refer to the History Tables above)")
    questions[5]['choices'] = models.IntegerField(
        choices=choices_P2,
        widget=widgets.RadioSelect
    )

    questions[6]['ans'] = models.IntegerField(initial=3)
    questions[6]['statement'] = models.StringField(initial="In a Period, if you choose Action Y and Other Blue chooses Action W in Blue Game, then how many points will you receive in Blue Game? (Refer to the Points Tables above)")
    questions[6]['choices'] = models.IntegerField(
        choices=choices_P2,
        widget=widgets.RadioSelect
    )

    questions[7]['ans'] = models.IntegerField(initial=1)
    questions[7]['statement'] = models.StringField(initial="In Period 4, which Action was chosen by Other Blue in Blue Game? (Refer to the History Tables above)")
    questions[7]['choices'] = models.IntegerField(
        choices=choices_actions,
        widget=widgets.RadioSelect
    )

    questions[8]['ans'] = models.IntegerField(initial=4)
    questions[8]['statement'] = models.StringField(initial="In Period 4, which Action was chosen by Other Red in Red Game? (Refer to the History Tables above)")
    questions[8]['choices'] = models.IntegerField(
        choices=choices_actions,
        widget=widgets.RadioSelect
    )

    return questions


class Constants(BaseConstants):
    name_in_url = 'mmc_rep_intro_off_TAS'
    players_per_group = None
    num_rounds = 1

# Properties of session imported from session configurations
    num_matches = settings.SESSION_CONFIGS[2].get('SG_totalNum')  # Total Number of Supergames
    
    dieN = settings.SESSION_CONFIGS[2].get('die_N')  # Number on a die
    contProb = settings.SESSION_CONFIGS[2].get('contProb')  # Continuation probability in percentages
    endProb = 100 - contProb 
    thres = int(1+(dieN*contProb/100))  # Threshold number on a die
    
    payoff_matrix1 = settings.SESSION_CONFIGS[2].get('payoff_1')  # Payoff matrix of setting 1
    payoff_matrix2 = settings.SESSION_CONFIGS[2].get('payoff_2')  # Payoff matrix of setting 2
    
    participation_fee = settings.SESSION_CONFIGS[2].get('participation_fee')  # Participation payment
    quiz_fee = settings.SESSION_CONFIGS[2].get('quiz_fee')  # Quiz payment
    avg_earn = settings.SESSION_CONFIGS[2].get('avg_earn')  # Average Earning
    low_earn = settings.SESSION_CONFIGS[2].get('low_earn')  # Low Earning
    high_earn = settings.SESSION_CONFIGS[2].get('high_earn')  # High Earning
    expPoints_Red = settings.SESSION_CONFIGS[2].get('expPoints_Red')  # Expected Points for Red Game
    expPoints_Blue = settings.SESSION_CONFIGS[2].get('expPoints_Blue')  # Expected Points for Blue Game

    exRate = int(1/settings.SESSION_CONFIGS[2].get('real_world_currency_per_point'))  # Exchange Rate (points to dollar)
    
    minExpTime = settings.SESSION_CONFIGS[2].get('minExpTime')  # Min Expected time of the session
    maxExpTime = settings.SESSION_CONFIGS[2].get('maxExpTime')  # Max Expected time of the session
    time_welcome = settings.SESSION_CONFIGS[2].get('time_welcome')  # Time allotted to first page
    time_quiz = settings.SESSION_CONFIGS[2].get('time_quiz')  # Total time allotted to the quiz
    time_round = settings.SESSION_CONFIGS[2].get('time_round')  # Total time allotted to a round
    time_intro = settings.SESSION_CONFIGS[2].get('time_intro')  # Time allotted to instructions
    
    num_ques = settings.SESSION_CONFIGS[2].get('num_ques')  # Number of questions in the quiz
    
    choices_prob = (
            (1, "100%"),
            (2, str(contProb)+"%"),
            (3, str(100-contProb)+"%"),
            (4, "0%"),
        )

    choices_periods = (
            (1, str(num_matches)+" periods"),
            (2, "4 periods"),
            (3, "1 period"),
            (4, "Random number of periods"),
        )

    choices_part = (
            (1, str(2)),
            (2, str(1)),
            (3, "Random number of participants"),
            (4, "No one"),
        )

    choices_P1 = (
            (1, str(payoff_matrix1[0][0])),
            (2, str(payoff_matrix1[0][1])),
            (3, str(payoff_matrix1[1][0])),
            (4, str(payoff_matrix1[1][1])),
        )

    choices_P2 = (
            (1, str(payoff_matrix2[0][0])),
            (2, str(payoff_matrix2[0][1])),
            (3, str(payoff_matrix2[1][0])),
            (4, str(payoff_matrix2[1][1])),
        )

    choices_actions = (
            (1, "Y"),
            (2, "W"),
            (3, "A"),
            (4, "B"),
        )

    questions = frame_question(choices_prob, choices_actions, choices_periods, choices_part, choices_P1, choices_P2)


class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            p.participant.vars["disconnected"] = 0
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
    timedout = models.IntegerField(initial=0)

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
