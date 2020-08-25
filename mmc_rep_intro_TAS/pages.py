from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time
from copy import deepcopy

class BeginInstructions(Page):
    """Page at the beginning of Instructions"""

    timeout_seconds = Constants.time_welcome*60
    timer_text = 'Minutes till Instructions begin:'

    def before_next_page(self):
        self.participant.vars['expiry'] = time.time()+Constants.time_intro*60

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
            participation_fee=Constants.participation_fee,
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
        print(self.player.ques_stat_1)
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
        self.player.answer_check()

class Result(Page):

    timeout_seconds = Constants.time_welcome*60
    timer_text = 'Time remaining to begin Experiment:'

    def vars_for_template(self):
        return dict(
            correct_ans = self.player.myCorrectAns,
            quiz_ques = Constants.num_ques,
            quiz_pay = self.player.myQuizPay,
            )

page_sequence = [
                BeginInstructions, 
                Welcome,
                # PayoffIntroduction, 
                # GameIntroduction, 
                # HistoryIntroduction, 
                # DecisionIntroduction,
                # Payment, 
                # Quiz, 
                # Result
                ]