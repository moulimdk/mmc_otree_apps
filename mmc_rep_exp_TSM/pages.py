from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


class BeginExperiment(Page):
    
    timeout_seconds = 60*Constants.time_begin
    timer_text = "Experiment will start in:"

    def vars_for_template(self):
        
        return dict(
            payoff_matrix1 = Constants.payoff_matrix1,
            payoff_matrix2 = Constants.payoff_matrix2,
            )

    def is_displayed(self):
        
        return self.round_number == 1

class ShuffleWaitPage(WaitPage):
    
    """Page where groups are formed and results are received"""
    template_name = 'mmc_rep_exp_TSM/ShuffleWaitPage.html'
    
    wait_for_all_groups = True
    after_all_players_arrive = 'shuffle'

    def vars_for_template(self):
        
        mQu = Constants.quiz_fee*self.participant.vars["myCorrectAns"]
        roundNumber = int(np.where(self.round_number <= Constants.SG_endPeriods)[0][0])+1
        #print("Player in Shuffle:", self.player, "Abandoned Status", self.player.participant.vars["abandoned"])
        if (self.round_number == 1) or ((self.round_number - 1) in Constants.SG_endPeriods):
            #print("round Number:", roundNumber)
            dict_return = dict(
                roundNumber = roundNumber,
                payoff_matrix1 = Constants.payoff_matrix1,
                payoff_matrix2 = Constants.payoff_matrix2,
                periodNumber = 1,
                disconnected = self.participant.vars["disconnected"],
                myParticipation = Constants.participation_fee,
                myQuiz = mQu,
                myTotalPayoff = Constants.participation_fee+mQu,
                )
        else:
            periodNumber = int(self.round_number)
            if roundNumber>1:
                periodNumber = int(self.round_number - Constants.SG_endPeriods[roundNumber-2])

            dict_return = dict(
                myChoiceR = self.player.in_round(self.round_number-1).myChoiceR,
                myChoiceB = self.player.in_round(self.round_number-1).myChoiceB,
                myChoiceRHistory = self.player.participant.vars["myChoiceHistoryR"],
                myChoiceBHistory = self.player.participant.vars["myChoiceHistoryB"],
                myPayoffRHistory = self.player.participant.vars["myPayoffHistoryR"],
                myPayoffBHistory = self.player.participant.vars["myPayoffHistoryB"],
                otherRChoiceHistory = self.player.participant.vars["otherChoiceHistoryR"],
                otherBChoiceHistory = self.player.participant.vars["otherChoiceHistoryB"],
                otherRPayoffHistory = self.player.participant.vars["otherPayoffHistoryR"],
                otherBPayoffHistory = self.player.participant.vars["otherPayoffHistoryB"],
                rollHistory = self.player.participant.vars["rollHistory"],
                periodNumber = periodNumber,
                periodHistory = self.player.participant.vars["periodHistory"],
                roundNumber = roundNumber,
                roundHistory = self.player.participant.vars["roundHistory"],
                payoff_matrix1 = Constants.payoff_matrix1,
                payoff_matrix2 = Constants.payoff_matrix2,
                disconnected = self.participant.vars["disconnected"],
                myParticipation = Constants.participation_fee,
                myQuiz = mQu,
                myTotalPayoff = Constants.participation_fee+mQu,
                )

        return dict_return

    def is_displayed(self):

        #Logic for disconnected person (displayed is connected and disconnected in the previous round)
        disconnected_logic = ((self.player.participant.vars["disconnected"] == 1) & (self.player.participant.vars["disconnected_period"] == self.round_number - 1)) or (self.player.participant.vars["disconnected"] == 0)
        
        return (self.round_number <= Constants.SG_endPeriods[-1]) & (self.player.participant.vars["oddGroup"] == 0) & disconnected_logic & (self.player.participant.vars["abandoned"] < 1)
    
class GameDecisions(Page):

    form_model = 'player'
    form_fields = ['myChoiceR','myChoiceB']
    timer_text = "Minutes left to choose and confirm actions in this period:"

    timeout_seconds = 60*Constants.time_period

    def before_next_page(self):

        if self.timeout_happened:
            self.player.participant.vars["disconnected"] = 1
            print("I am disconnected",self.player.participant.vars["disconnected"])
            self.player.participant.vars["disconnected_period"] = self.round_number

    def vars_for_template(self):

        return dict(
                myChoiceRHistory = self.player.myChoiceHistoryR,
                myChoiceBHistory = self.player.myChoiceHistoryB,
                myPayoffRHistory = self.player.myPayoffHistoryR,
                myPayoffBHistory = self.player.myPayoffHistoryB,
                otherRChoiceHistory = self.player.otherChoiceHistoryR,
                otherBChoiceHistory = self.player.otherChoiceHistoryB,
                otherRPayoffHistory = self.player.otherPayoffHistoryR,
                otherBPayoffHistory = self.player.otherPayoffHistoryB,
                abandoned = self.player.participant.vars["abandoned"],
                abandoned_R = self.player.participant.vars["abandoned_R"],
                abandoned_B = self.player.participant.vars["abandoned_B"],
                rollHistory = self.player.rollHistory,
                periodNumber = self.player.periodNumber,
                periodHistory = self.player.periodHistory,
                roundNumber = self.player.roundNumber,
                roundHistory = self.player.roundHistory,
                payoff_matrix1 = Constants.payoff_matrix1,
                payoff_matrix2 = Constants.payoff_matrix2,
            )

    def is_displayed(self):

        return (self.round_number <= Constants.SG_endPeriods[-1]) & (self.player.participant.vars["oddGroup"] == 0) & (self.player.participant.vars["abandoned"] < 1) & (self.player.participant.vars["disconnected"] == 0)

class EndRoundWaitPage(WaitPage):

    template_name = 'mmc_rep_exp_TSM/EndRoundWaitPage.html'

    def after_all_players_arrive(self):

        self.group.end_period_outcome()

    def vars_for_template(self):

        return dict(
                myChoiceR = self.player.myChoiceR,
                myChoiceB = self.player.myChoiceB,
                myChoiceRHistory = self.player.myChoiceHistoryR,
                myChoiceBHistory = self.player.myChoiceHistoryB,
                myPayoffRHistory = self.player.myPayoffHistoryR,
                myPayoffBHistory = self.player.myPayoffHistoryB,
                otherRChoiceHistory = self.player.otherChoiceHistoryR,
                otherBChoiceHistory = self.player.otherChoiceHistoryB,
                otherRPayoffHistory = self.player.otherPayoffHistoryR,
                otherBPayoffHistory = self.player.otherPayoffHistoryB,
                rollHistory = self.player.rollHistory,
                periodNumber = self.player.periodNumber,
                periodHistory = self.player.periodHistory,
                roundNumber = self.player.roundNumber,
                roundHistory = self.player.roundHistory,
                payoff_matrix1 = Constants.payoff_matrix1,
                payoff_matrix2 = Constants.payoff_matrix2,
                )

    def is_displayed(self):

        disconnected_logic = ((self.player.participant.vars["disconnected"] == 1) & (self.player.participant.vars["disconnected_period"] == self.round_number)) or (self.player.participant.vars["disconnected"] == 0)

        return (self.round_number in Constants.SG_endPeriods) & (self.player.participant.vars["oddGroup"] == 0) & (self.player.participant.vars["abandoned"] < 1) & (disconnected_logic)

class RoundResult(Page):
    
    """docstring for RoundResult Page: Result of every supergame for connected players"""

    timeout_seconds = 15
    timer_text = "Minutes on this page:"

    def vars_for_template(self):

        # self.player.payoff = self.player.participant.vars["roundPayoff"]
        
        return dict(
                myChoiceRHistory = self.player.myChoiceHistoryR,
                myChoiceBHistory = self.player.myChoiceHistoryB,
                myPayoffRHistory = self.player.myPayoffHistoryR,
                myPayoffBHistory = self.player.myPayoffHistoryB,
                otherRChoiceHistory = self.player.otherChoiceHistoryR,
                otherBChoiceHistory = self.player.otherChoiceHistoryB,
                otherRPayoffHistory = self.player.otherPayoffHistoryR,
                otherBPayoffHistory = self.player.otherPayoffHistoryB,
                abandoned_R = self.player.participant.vars["abandoned_R"],
                abandoned_B = self.player.participant.vars["abandoned_B"],
                rollHistory = self.player.rollHistory,
                periodNumber = self.player.periodNumber,
                periodHistory = self.player.periodHistory,
                roundNumber = self.player.roundNumber,
                roundHistory = self.player.roundHistory,
                LastRound = Constants.SG_endPeriods[-1],
                payoff_matrix1 = Constants.payoff_matrix1,
                payoff_matrix2 = Constants.payoff_matrix2,
                )

    def is_displayed(self):

        return (self.round_number in Constants.SG_endPeriods) & (self.player.participant.vars["oddGroup"] == 0) & (self.player.participant.vars["abandoned"] < 1) & (self.player.participant.vars["disconnected"] == 0) 

class AbandonedPlayer(Page):
    
    """docstring for Abandoned Player: Notification for player whose partner left"""
    
    timeout_seconds = 60*Constants.time_next
    timer_text = "Minutes on this page:"

    def vars_for_template(self):

        self.player.abandonedPlayerPayoff()

        return dict(
            expPointsR = Constants.expPoints["R"],
            expPointsB = Constants.expPoints["B"],
            numberPeriodsLeft = self.player.numberPeriodsLeft,
            abandoned_period = self.player.participant.vars["abandoned_period"],
            myChoiceRHistory = self.player.participant.vars["myChoiceHistoryR"],
            myChoiceBHistory = self.player.participant.vars["myChoiceHistoryB"],
            myPayoffRHistory = self.player.participant.vars["myPayoffHistoryR"],
            myPayoffBHistory = self.player.participant.vars["myPayoffHistoryB"],
            otherRChoiceHistory = self.player.participant.vars["otherChoiceHistoryR"],
            otherBChoiceHistory = self.player.participant.vars["otherChoiceHistoryB"],
            otherRPayoffHistory = self.player.participant.vars["otherPayoffHistoryR"],
            otherBPayoffHistory = self.player.participant.vars["otherPayoffHistoryB"],
            rollHistory = self.player.participant.vars["rollHistory"],
            periodNumber = self.player.periodNumber,
            periodHistory = self.player.participant.vars["periodHistory"],
            roundNumber = self.player.roundNumber,
            roundHistory = self.player.participant.vars["roundHistory"],
            payoff_matrix1 = Constants.payoff_matrix1,
            payoff_matrix2 = Constants.payoff_matrix2,
            disconnected = self.participant.vars["disconnected"],
            )

    def is_displayed(self):
        
        return (self.round_number in Constants.SG_endPeriods) & (self.player.participant.vars["oddGroup"] == 0) & (self.player.participant.vars["abandoned"] == 1) & (self.player.participant.vars["disconnected"] == 0)

class OddPlayer(Page):
    
    """docstring for OddPlayer: Notification for player without Other"""

    timeout_seconds = 120*Constants.time_next
    timer_text = "Minutes on this page:"

    def vars_for_template(self):
        
        self.player.oddPlayerPayoff()

        return dict(
            expPointsR = Constants.expPoints["R"],
            expPointsB = Constants.expPoints["B"],
            totalPeriods = self.player.totalPeriod,
            roundNumber = self.player.roundNumber,
            )

    def is_displayed(self):
        
        return (self.round_number in Constants.SG_endPeriods) & (self.player.participant.vars["oddGroup"] == 1) & (self.player.participant.vars["disconnected"] == 0)

class Payment(Page):

    """docstring for Payment: Payment Page for connected players"""
    
    timeout_seconds = 60*Constants.time_begin
    timer_text = "Minutes to Questionnaire:"

    def vars_for_template(self):

        mPo = self.player.participant.vars["totalPayoff"]
        print("Cumulative Payoffs:", mPo)
        mPa = c(mPo).to_real_world_currency(self.session)
        mQu = Constants.quiz_fee*self.participant.vars["myCorrectAns"]
       
        return dict(
            conversionRate = Constants.exRate,
            myParticipation = Constants.participation_fee,
            myQuiz = mQu,
            myPoints = mPo,
            myPayoff = mPa,
            myTotalPayoff = mPa+Constants.participation_fee+mQu,
            )
    
    def is_displayed(self):

        return (self.round_number == Constants.SG_endPeriods[-1]+1) & (self.player.participant.vars["disconnected"] == 0)

class DisconnectedPayment(Page):
    
    """docstring for DisconnectedPayment: Payment Page for disconnected players"""
    
    timeout_seconds = 60*Constants.time_begin

    def vars_for_template(self):
    
        mQu = Constants.quiz_fee*self.participant.vars["myCorrectAns"]
        
        return dict(
            myParticipation = Constants.participation_fee,
            myQuiz = mQu,
            myTotalPayoff = Constants.participation_fee+mQu,
            )
    
    def is_displayed(self):
        
        return (self.round_number == Constants.SG_endPeriods[-1]+1) & (self.player.participant.vars["disconnected"]==1)


page_sequence = [BeginExperiment, 
                 ShuffleWaitPage,
                 GameDecisions,
                 EndRoundWaitPage, 
                 RoundResult,
                 AbandonedPlayer,
                 OddPlayer,
                 Payment,
                 DisconnectedPayment,
                ]