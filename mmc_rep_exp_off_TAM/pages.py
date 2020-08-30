from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np

class BeginExperiment(Page):
    
    def vars_for_template(self):
        
        return dict(
            payoff_matrix1 = Constants.payoff_matrix1,
            payoff_matrix2 = Constants.payoff_matrix2,
            exRate=Constants.exRate,
            contProb=Constants.contProb,
            endProb=Constants.endProb,
            )

    def is_displayed(self):
        
        return self.round_number == 1


class ShuffleWaitPage(WaitPage):
    """docstring for ShuffleWaitPage"""
    
    template_name = 'mmc_rep_exp_off_TAM/ShuffleWaitPage.html'
    
    wait_for_all_groups = True
    after_all_players_arrive = 'shuffle'

    def vars_for_template(self):
        
        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        temp = self.round_number
        
        if roundPos > 0:
            temp = int(self.round_number - Constants.SG_endPeriods[roundPos-1])

        self.player.periodNumber = temp
        self.player.roundNumber = roundPos + 1

        if self.player.periodNumber == 1:
        
            dict_return = dict(
                roundNumber = self.player.roundNumber,
                payoff_matrix1 = Constants.payoff_matrix1,
                payoff_matrix2 = Constants.payoff_matrix2,
                periodNumber = 1,
                )

        else:

            dict_return = dict(
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
                )

    
        return dict_return

    def is_displayed(self):

        return ((self.round_number == 1) or (self.round_number - 1 in Constants.SG_endPeriods[0:-1])) or ((self.round_number <= Constants.SG_endPeriods[-1]) & (self.player.participant.vars["oddGroup"] == 0))

class GameDecision(Page):

    form_model = 'player'
    form_fields = ['myChoiceR','myChoiceB']
    timer_text = "Minutes left to choose and confirm actions in this period:"

    timeout_seconds = 60*Constants.time_period

    def before_next_page(self):

        if self.timeout_happened:
            
            self.player.timeout = 1
            self.player.myChoiceR = np.random.choice([0,1],1)
            self.player.myChoiceB = np.random.choice([0,1],1)

    def vars_for_template(self):

        roundPos = np.where(self.round_number <= Constants.SG_endPeriods)[0][0]
        temp = self.round_number
        
        if roundPos > 0:
            temp = int(self.round_number - Constants.SG_endPeriods[roundPos-1])

        self.player.periodNumber = temp
        self.player.roundNumber = roundPos + 1

        return dict(
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

        return (self.round_number <= Constants.SG_endPeriods[-1]) & (self.player.participant.vars["oddGroup"] == 0)
        
class DecisionWaitPage(WaitPage):

    template_name = 'mmc_rep_exp_off_TAM/DecisionWaitPage.html'

    def after_all_players_arrive(self):

        self.group.period_update()

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

        return (self.round_number <= Constants.SG_endPeriods[-1]) & (self.player.participant.vars["oddGroup"] == 0)

class RoundResult(Page):
    
    """docstring for RoundResult Page: Result of every supergame for connected players"""

    def vars_for_template(self):

        lastRound = 0
        if self.round_number == Constants.SG_endPeriods[-1]:
            lastRound = 1
        
        return dict(
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
                lastRound = lastRound,
                )

    def is_displayed(self):

        return (self.round_number in Constants.SG_endPeriods) & (self.player.participant.vars["oddGroup"] == 0)

class OddPlayer(Page):
    
    """docstring for OddPlayer: Notification for player without Other"""

    def vars_for_template(self):
        
        lastRound = 0
        if self.round_number == Constants.SG_endPeriods[-1]:
            lastRound = 1

        self.player.oddPlayerPayoff()

        return dict(
            expPointsR = Constants.expPoints["R"],
            expPointsB = Constants.expPoints["B"],
            totalPeriods = self.player.totalPeriod,
            roundNumber = self.player.roundNumber,
            lastRound = lastRound,
            )

    def is_displayed(self):
        
        return (self.round_number in Constants.SG_endPeriods) & (self.player.participant.vars["oddGroup"] == 1)

class Payment(Page):

    """docstring for Payment: Payment Page for connected players"""
    
    def vars_for_template(self):

        mPo = self.player.participant.vars["totalPayoff"]
        mPa = mPo/Constants.exRate
        mQu = Constants.quiz_fee*self.participant.vars["myCorrectAns"]
        
        self.player.totalPayment = mPa + Constants.participation_fee + mQu
       
        return dict(
            conversionRate = Constants.exRate,
            myParticipation = Constants.participation_fee,
            myQuiz = mQu,
            myPoints = mPo,
            myPayoff = mPa,
            myTotalPayoff = mPa+Constants.participation_fee+mQu,
            )
    
    def is_displayed(self):

        return (self.round_number == Constants.SG_endPeriods[-1]+1)

page_sequence = [
                BeginExperiment,
                ShuffleWaitPage,
                GameDecision,
                DecisionWaitPage,
                RoundResult,
                OddPlayer,
                Payment
                ]