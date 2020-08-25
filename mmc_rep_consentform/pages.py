from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Consent(Page):

    form_model = 'player'
    form_fields = ['futureUse','OtherResearch','consent']

    def vars_for_template(self):
        return dict(
            participation_fee = Constants.participation_fee,
            quiz_fee=Constants.quiz_fee,
            avg_earn=Constants.avg_earn,
            low_earn=Constants.low_earn,
            high_earn=Constants.high_earn,
            )

class Results(Page):

    timeout_seconds = 20
    timer_text = 'Minutes remaining on this page'
    
    def vars_for_template(self):
        return dict(
            consent = self.player.consent,
            participation_fee = Constants.participation_fee,
            )


page_sequence = [Consent, Results]
