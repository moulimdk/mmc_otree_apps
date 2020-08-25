from shared_model import *


author = 'Mouli Modak'

doc = """
Online Consent Form for MMC experiment
"""


class Constants(BaseConstants):
    name_in_url = 'mmc_rep_consentform'
    players_per_group = None
    num_rounds = 1

    participation_fee = settings.SESSION_CONFIGS[0].get('participation_fee') # Participation payment
    quiz_fee = settings.SESSION_CONFIGS[0].get('quiz_fee') #Quiz payment
    avg_earn = settings.SESSION_CONFIGS[0].get('avg_earn') #Average Earning
    low_earn = settings.SESSION_CONFIGS[0].get('low_earn') #Low Earning
    high_earn = settings.SESSION_CONFIGS[0].get('high_earn') #High Earning

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    consent = models.StringField()
    futureUse = models.IntegerField(
        choices=[
            [0, "No"],
            [1, "Yes"],
        ],
        widget = widgets.RadioSelect
        )
    OtherResearch = models.IntegerField(
        choices=[
            [0, "No"],
            [1, "Yes"],
        ],
        widget = widgets.RadioSelect
        )