from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Mouli Modak'

doc = """
Personal Questionnaire at the end of MMC experiment
"""


class Constants(BaseConstants):
    name_in_url = 'mmc_rep_questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # gender_question = models.StringField(initial="Gender")
    Gender = models.IntegerField(
        choices=[
        [1, "Female"],
        [2, "Male"],
        [3, "Prefer Not to Answer"]
        ])

    age = models.IntegerField()

    # Education_question = models.IntegerField(initial="What is highest education level?")
    Education_choices = models.IntegerField(
        choices=[
        [1, "None"],
        [2, "High School"],
        [3, "Bachelors"],
        [4, "Masters"],
        [5, "Ph.D."],
        [6, "Prefer Not to Answer"]
        ])

    Econ_courses = models.IntegerField(
        choices=[
        [1, "0"],
        [2, "1"],
        [3, "2"],
        [4, "3"],
        [5, "4+"],
        [6, "Prefer Not to Answer"]
        ])

    Stat_courses = models.IntegerField(
        choices=[
        [1, "0"],
        [2, "1"],
        [3, "2"],
        [4, "3"],
        [5, "4+"],
        [6, "Prefer Not to Answer"]
        ] )

    STEM_courses = models.IntegerField(
        choices=[
        [1, "0"],
        [2, "1"],
        [3, "2"],
        [4, "3"],
        [5, "4+"],
        [6, "Prefer Not to Answer"]
        ])

    Busi_courses = models.IntegerField(
        choices=[
        [1, "0"],
        [2, "1"],
        [3, "2"],
        [4, "3"],
        [5, "4+"],
        [6, "Prefer Not to Answer"]
        ])

    Experiments = models.IntegerField(
        choices=[
        [1, "0"],
        [2, "1"],
        [3, "2"],
        [4, "3"],
        [5, "4+"],
        [6, "Prefer Not to Answer"]
        ])

    Employment = models.IntegerField(
        choices=[
        [1, "Student (Not Employed)"],
        [2, "Manager (manager, executive, accountant, other professional)"],
        [3, "STEM (Sciences, Technology, Engineering, Math)"],
        [4, "Other (services, manufacturing, etc.)"],
        [5, "Prefer Not to Answer"]
        ])