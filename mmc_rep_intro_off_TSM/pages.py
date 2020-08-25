from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time
from copy import deepcopy


class BeginInstructions(Page):
    """Page at the beginning of Instructions"""

    def vars_for_template(self):
        return dict(
            time_intro=Constants.time_intro,
            minExpTime=Constants.minExpTime,
            maxExpTime=Constants.maxExpTime,
            )


class Welcome(Page):
    """First page"""

    timer_text = 'Time remaining on Instructions:'

    def get_timeout_seconds(self):

        return self.participant.vars['expiry'] - time.time()

    def vars_for_template(self):

        return dict(
            participation_fee=int(Constants.participation_fee),
            quiz_fee=Constants.quiz_fee,
            avg_earn=Constants.avg_earn,
            low_earn=Constants.low_earn,
            high_earn=Constants.high_earn,
            exRate=Constants.exRate,
            time_quiz=Constants.time_quiz,
            num_ques=Constants.num_ques,
            )

class PayoffIntroduction(Page):

    timer_text = 'Time remaining on Instructions:'

    def get_timeout_seconds(self):
      return self.participant.vars['expiry'] - time.time()

    def vars_for_template(self):
        return dict(
            Rounds=Constants.num_matches,
            dieN=Constants.dieN,
            thres=Constants.thres,
            contProb=Constants.contProb,
            endProb=Constants.endProb,
            time_period=Constants.time_round,
            exRate=Constants.exRate,
            expPoints_Red=Constants.expPoints_Red,
            expPoints_Blue=Constants.expPoints_Blue,
            )

class GameIntroduction(Page):

    timer_text = 'Time remaining on Instructions:'

    def get_timeout_seconds(self):
      return self.participant.vars['expiry'] - time.time()

    def vars_for_template(self):
        return dict(
            time_period=Constants.time_round,
            payoff_matrix1=Constants.payoff_matrix1,
            payoff_matrix2=Constants.payoff_matrix2,
            exRate=Constants.exRate,
            )

class HistoryIntroduction(Page):

    timer_text = 'Time remaining on Instructions:'

    def get_timeout_seconds(self):
      return self.participant.vars['expiry'] - time.time()

    def vars_for_template(self):
        return dict(
            dieN=Constants.dieN,
            payoff_matrix1=Constants.payoff_matrix1,
            payoff_matrix2=Constants.payoff_matrix2,
            )

class DecisionIntroduction(Page):

    timer_text = 'Time remaining on Instructions:'

    def get_timeout_seconds(self):
      return self.participant.vars['expiry'] - time.time()

class Payment(Page):

    timer_text = 'Time remaining on Instructions:'

    def get_timeout_seconds(self):
      return self.participant.vars['expiry'] - time.time()

    def vars_for_template(self):
        return dict(
            Rounds=Constants.num_matches,
            dieN=Constants.dieN,
            thres=Constants.thres,
            contProb=Constants.contProb,
            endProb=Constants.endProb,
            time_period=Constants.time_round,
            exRate=Constants.exRate,
            expPoints_Red=Constants.expPoints_Red,
            expPoints_Blue=Constants.expPoints_Blue,
            )

class Quiz(Page):

    timer_text = 'Time remaining on Quiz:'
    timeout_seconds = Constants.time_quiz*60

    form_model = 'player'
    form_fields = ['ans_choice_1','ans_choice_2','ans_choice_3','ans_choice_4','ans_choice_5','ans_choice_6','ans_choice_7','ans_choice_8']
    
    def vars_for_template(self):
        return dict(
            statement_1 = self.player.ques_stat_1,
            statement_2 = self.player.ques_stat_2,
            statement_3 = self.player.ques_stat_3,
            statement_4 = self.player.ques_stat_4,
            statement_5 = self.player.ques_stat_5,
            statement_6 = self.player.ques_stat_6,
            statement_7 = self.player.ques_stat_7,
            statement_8 = self.player.ques_stat_8,
            payoff_matrix1 = Constants.payoff_matrix1,
            payoff_matrix2 = Constants.payoff_matrix2,
            )

    def before_next_page(self):
        
        if self.timeout_happened:
            self.player.timedout = 1
        self.player.answer_check()

class Result(Page):

    def vars_for_template(self):
        return dict(
            timedout = self.player.timedout,
            correct_ans = self.player.myCorrectAns,
            quiz_ques = Constants.num_ques,
            quiz_pay = self.player.myQuizPay,
            statement_1 = self.player.ques_stat_1,
            statement_2 = self.player.ques_stat_2,
            statement_3 = self.player.ques_stat_3,
            statement_4 = self.player.ques_stat_4,
            statement_5 = self.player.ques_stat_5,
            statement_6 = self.player.ques_stat_6,
            statement_7 = self.player.ques_stat_7,
            statement_8 = self.player.ques_stat_8,
            payoff_matrix1 = Constants.payoff_matrix1,
            payoff_matrix2 = Constants.payoff_matrix2,
            Chosen_1 = Constants.choices_prob[(self.player.ans_choice_1)-1][1],
            Chosen_2 = Constants.choices_periods[(self.player.ans_choice_2)-1][1],
            Chosen_3 = Constants.choices_part[(self.player.ans_choice_3)-1][1],
            Chosen_4 = Constants.choices_P1[(self.player.ans_choice_4)-1][1],
            Chosen_5 = Constants.choices_P1[(self.player.ans_choice_5)-1][1],
            Chosen_6 = Constants.choices_P2[(self.player.ans_choice_6)-1][1],
            Chosen_7 = Constants.choices_actions[(self.player.ans_choice_7)-1][1],
            Chosen_8 = Constants.choices_actions[(self.player.ans_choice_8)-1][1],
            Correct_1 = Constants.choices_prob[(self.player.correct_ans_1)-1][1],
            Correct_2 = Constants.choices_periods[(self.player.correct_ans_2)-1][1],
            Correct_3 = Constants.choices_part[(self.player.correct_ans_3)-1][1],
            Correct_4 = Constants.choices_P1[(self.player.correct_ans_4)-1][1],
            Correct_5 = Constants.choices_P1[(self.player.correct_ans_5)-1][1],
            Correct_6 = Constants.choices_P2[(self.player.correct_ans_6)-1][1],
            Correct_7 = Constants.choices_actions[(self.player.correct_ans_7)-1][1],
            Correct_8 = Constants.choices_actions[(self.player.correct_ans_8)-1][1],
            )


page_sequence = [
                BeginInstructions, 
                Welcome,
                PayoffIntroduction, 
                GameIntroduction, 
                HistoryIntroduction, 
                DecisionIntroduction,
                Payment, 
                Quiz, 
                Result
		]
