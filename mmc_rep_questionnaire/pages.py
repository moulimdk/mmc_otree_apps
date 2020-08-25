from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Questionnaire(Page):

    form_model = 'player'
    form_fields = ['Gender','age','Education_choices','Econ_courses','Stat_courses','STEM_courses','Busi_courses','Experiments','Employment']

    def is_displayed(self):
        
        return self.participant.vars["disconnected"] == 0

class EndPage(Page):
    
    timeout_seconds = 60
 
    def is_displayed(self):
        
        return self.participant.vars["disconnected"] == 0


page_sequence = [Questionnaire, EndPage]
