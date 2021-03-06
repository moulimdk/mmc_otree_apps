from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    # real_world_currency_per_point=1.00,
    num_demo_participants=12,
    exRate=680,
    real_world_currency_per_point=1/680,
    SG_lengths=[1,1,6,2,8,5,5,2,2,5,2,11,2,3,10,2,4,13,9,1,1,1,5,2,6,4,2,1,6,2],
    SG_totalNum=len([1,1,6,2,8,5,5,2,2,5,2,11,2,3,10,2,4,13,9,1,1,1,5,2,6,4,2,1,6,2]),
    payoff_1=[[48, 12], [50, 25]],
    payoff_2=[[30, 8], [50, 25]],
    expPoints_Red=33.75,
    expPoints_Blue=28.25,
    participation_fee=5.00,
    quiz_fee=0.25,
    avg_earn=17,
    low_earn=10,
    high_earn=25,
    minExpTime=50,
    maxExpTime=60,
    time_welcome=0.15,
    time_period=2,
    time_intro=15,
    time_next=0.15,
    time_quiz=5,
    num_ques=8,
    contProb=75,
    die_N=8,
    doc=""
)


SESSION_CONFIGS = [
    dict(
        name='mmc_rep_TSS_Lab',
        display_name="MMC Prisoner Experiment TSS Lab",
        app_sequence=['mmc_rep_intro_off_TSS', 'mmc_rep_exp_off_TSS', 'mmc_rep_questionnaire'],
        USE_POINTS=True,
        exRate=SESSION_CONFIG_DEFAULTS["exRate"],
        real_world_currency_per_point=SESSION_CONFIG_DEFAULTS["real_world_currency_per_point"],
        num_demo_participants=SESSION_CONFIG_DEFAULTS["num_demo_participants"],
        SG_lengths=SESSION_CONFIG_DEFAULTS["SG_lengths"],
        SG_totalNum=SESSION_CONFIG_DEFAULTS["SG_totalNum"],
        payoff_1=SESSION_CONFIG_DEFAULTS["payoff_1"],
        payoff_2=SESSION_CONFIG_DEFAULTS["payoff_2"],
        expPoints_Red=SESSION_CONFIG_DEFAULTS["expPoints_Red"],
        expPoints_Blue=SESSION_CONFIG_DEFAULTS["expPoints_Blue"],
        participation_fee=SESSION_CONFIG_DEFAULTS["participation_fee"],
        quiz_fee=SESSION_CONFIG_DEFAULTS["quiz_fee"],
        avg_earn=SESSION_CONFIG_DEFAULTS["avg_earn"],
        low_earn=SESSION_CONFIG_DEFAULTS["low_earn"],
        high_earn=SESSION_CONFIG_DEFAULTS["high_earn"],
        minExpTime=SESSION_CONFIG_DEFAULTS["minExpTime"],
        maxExpTime=SESSION_CONFIG_DEFAULTS["maxExpTime"],
        time_welcome=SESSION_CONFIG_DEFAULTS["time_welcome"],
        time_period=SESSION_CONFIG_DEFAULTS["time_period"],
        time_intro=SESSION_CONFIG_DEFAULTS["time_intro"],
        time_next=SESSION_CONFIG_DEFAULTS["time_next"],
        time_quiz=SESSION_CONFIG_DEFAULTS["time_quiz"],
        num_ques=SESSION_CONFIG_DEFAULTS["num_ques"],
        contProb=SESSION_CONFIG_DEFAULTS["contProb"],
        die_N=SESSION_CONFIG_DEFAULTS["die_N"],
    ),
    dict(
        name='mmc_rep_TSM_Lab',
        display_name="MMC Prisoner Experiment TSM Lab",
        app_sequence=['mmc_rep_intro_off_TSM', 'mmc_rep_exp_off_TSM', 'mmc_rep_questionnaire'],
        USE_POINTS=True,
        exRate=SESSION_CONFIG_DEFAULTS["exRate"],
        real_world_currency_per_point=SESSION_CONFIG_DEFAULTS["real_world_currency_per_point"],
        num_demo_participants=SESSION_CONFIG_DEFAULTS["num_demo_participants"],
        SG_lengths=SESSION_CONFIG_DEFAULTS["SG_lengths"],
        SG_totalNum=SESSION_CONFIG_DEFAULTS["SG_totalNum"],
        payoff_1=SESSION_CONFIG_DEFAULTS["payoff_1"],
        payoff_2=SESSION_CONFIG_DEFAULTS["payoff_2"],
        expPoints_Red=SESSION_CONFIG_DEFAULTS["expPoints_Red"],
        expPoints_Blue=SESSION_CONFIG_DEFAULTS["expPoints_Blue"],
        participation_fee=SESSION_CONFIG_DEFAULTS["participation_fee"],
        quiz_fee=SESSION_CONFIG_DEFAULTS["quiz_fee"],
        avg_earn=SESSION_CONFIG_DEFAULTS["avg_earn"],
        low_earn=SESSION_CONFIG_DEFAULTS["low_earn"],
        high_earn=SESSION_CONFIG_DEFAULTS["high_earn"],
        minExpTime=SESSION_CONFIG_DEFAULTS["minExpTime"],
        maxExpTime=SESSION_CONFIG_DEFAULTS["maxExpTime"],
        time_welcome=SESSION_CONFIG_DEFAULTS["time_welcome"],
        time_period=SESSION_CONFIG_DEFAULTS["time_period"],
        time_intro=SESSION_CONFIG_DEFAULTS["time_intro"],
        time_next=SESSION_CONFIG_DEFAULTS["time_next"],
        time_quiz=SESSION_CONFIG_DEFAULTS["time_quiz"],
        num_ques=SESSION_CONFIG_DEFAULTS["num_ques"],
        contProb=SESSION_CONFIG_DEFAULTS["contProb"],
        die_N=SESSION_CONFIG_DEFAULTS["die_N"],
    ),
    dict(
        name='mmc_rep_TAS_Lab',
        display_name="MMC Prisoner Experiment TAS Lab",
        app_sequence=['mmc_rep_intro_off_TAS', 'mmc_rep_exp_off_TAS', 'mmc_rep_questionnaire'],
        USE_POINTS=True,
        exRate=SESSION_CONFIG_DEFAULTS["exRate"],
        real_world_currency_per_point=SESSION_CONFIG_DEFAULTS["real_world_currency_per_point"],
        num_demo_participants=SESSION_CONFIG_DEFAULTS["num_demo_participants"],
        SG_lengths=SESSION_CONFIG_DEFAULTS["SG_lengths"],
        SG_totalNum=SESSION_CONFIG_DEFAULTS["SG_totalNum"],
        payoff_1=SESSION_CONFIG_DEFAULTS["payoff_1"],
        payoff_2=SESSION_CONFIG_DEFAULTS["payoff_2"],
        expPoints_Red=SESSION_CONFIG_DEFAULTS["expPoints_Red"],
        expPoints_Blue=SESSION_CONFIG_DEFAULTS["expPoints_Blue"],
        participation_fee=SESSION_CONFIG_DEFAULTS["participation_fee"],
        quiz_fee=SESSION_CONFIG_DEFAULTS["quiz_fee"],
        avg_earn=SESSION_CONFIG_DEFAULTS["avg_earn"],
        low_earn=SESSION_CONFIG_DEFAULTS["low_earn"],
        high_earn=SESSION_CONFIG_DEFAULTS["high_earn"],
        minExpTime=SESSION_CONFIG_DEFAULTS["minExpTime"],
        maxExpTime=SESSION_CONFIG_DEFAULTS["maxExpTime"],
        time_welcome=SESSION_CONFIG_DEFAULTS["time_welcome"],
        time_period=SESSION_CONFIG_DEFAULTS["time_period"],
        time_intro=SESSION_CONFIG_DEFAULTS["time_intro"],
        time_next=SESSION_CONFIG_DEFAULTS["time_next"],
        time_quiz=SESSION_CONFIG_DEFAULTS["time_quiz"],
        num_ques=SESSION_CONFIG_DEFAULTS["num_ques"],
        contProb=SESSION_CONFIG_DEFAULTS["contProb"],
        die_N=SESSION_CONFIG_DEFAULTS["die_N"],
    ),
    dict(
        name='mmc_rep_TAM_Lab',
        display_name="MMC Prisoner Experiment TAM Lab",
        app_sequence=['mmc_rep_intro_off_TAM', 'mmc_rep_exp_off_TAM', 'mmc_rep_questionnaire'],
        USE_POINTS=True,
        exRate=SESSION_CONFIG_DEFAULTS["exRate"],
        real_world_currency_per_point=SESSION_CONFIG_DEFAULTS["real_world_currency_per_point"],
        num_demo_participants=SESSION_CONFIG_DEFAULTS["num_demo_participants"],
        SG_lengths=SESSION_CONFIG_DEFAULTS["SG_lengths"],
        SG_totalNum=SESSION_CONFIG_DEFAULTS["SG_totalNum"],
        payoff_1=SESSION_CONFIG_DEFAULTS["payoff_1"],
        payoff_2=SESSION_CONFIG_DEFAULTS["payoff_2"],
        expPoints_Red=SESSION_CONFIG_DEFAULTS["expPoints_Red"],
        expPoints_Blue=SESSION_CONFIG_DEFAULTS["expPoints_Blue"],
        participation_fee=SESSION_CONFIG_DEFAULTS["participation_fee"],
        quiz_fee=SESSION_CONFIG_DEFAULTS["quiz_fee"],
        avg_earn=SESSION_CONFIG_DEFAULTS["avg_earn"],
        low_earn=SESSION_CONFIG_DEFAULTS["low_earn"],
        high_earn=SESSION_CONFIG_DEFAULTS["high_earn"],
        minExpTime=SESSION_CONFIG_DEFAULTS["minExpTime"],
        maxExpTime=SESSION_CONFIG_DEFAULTS["maxExpTime"],
        time_welcome=SESSION_CONFIG_DEFAULTS["time_welcome"],
        time_period=SESSION_CONFIG_DEFAULTS["time_period"],
        time_intro=SESSION_CONFIG_DEFAULTS["time_intro"],
        time_next=SESSION_CONFIG_DEFAULTS["time_next"],
        time_quiz=SESSION_CONFIG_DEFAULTS["time_quiz"],
        num_ques=SESSION_CONFIG_DEFAULTS["num_ques"],
        contProb=SESSION_CONFIG_DEFAULTS["contProb"],
        die_N=SESSION_CONFIG_DEFAULTS["die_N"],
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='mmc_rep_exp',
        display_name='MMC Experiment',
        participant_label_file='_rooms/econ101.txt',
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# don't share this with anybody.
SECRET_KEY = '%r0m%g126(yy&+qobgl$y@2h6%@pnzs*8%+@th-=+9k21#0jkb'

INSTALLED_APPS = ['otree']

# inactive session configs
# dict(name='trust', display_name="Trust Game", num_demo_participants=2, app_sequence=['trust', 'payment_info']),
# dict(name='prisoner', display_name="Prisoner's Dilemma", num_demo_participants=2,
#      app_sequence=['prisoner', 'payment_info']),
# dict(name='volunteer_dilemma', display_name="Volunteer's Dilemma", num_demo_participants=3,
#      app_sequence=['volunteer_dilemma', 'payment_info']),
# dict(name='cournot', display_name="Cournot Competition", num_demo_participants=2, app_sequence=[
#     'cournot', 'payment_info'
# ]),
# dict(name='dictator', display_name="Dictator Game", num_demo_participants=2,
#      app_sequence=['dictator', 'payment_info']),
# dict(name='matching_pennies', display_name="Matching Pennies", num_demo_participants=2, app_sequence=[
#     'matching_pennies',
# ]),
# dict(name='traveler_dilemma', display_name="Traveler's Dilemma", num_demo_participants=2,
#      app_sequence=['traveler_dilemma', 'payment_info']),
# dict(name='bargaining', display_name="Bargaining Game", num_demo_participants=2,
#      app_sequence=['bargaining', 'payment_info']),
# dict(name='common_value_auction', display_name="Common Value Auction", num_demo_participants=3,
#      app_sequence=['common_value_auction', 'payment_info']),
# dict(name='bertrand', display_name="Bertrand Competition", num_demo_participants=2, app_sequence=[
#     'bertrand', 'payment_info'
# ]),
# dict(name='public_goods_simple', display_name="Public Goods (simple version from tutorial)",
#      num_demo_participants=3, app_sequence=['public_goods_simple', 'payment_info']),
# dict(name='trust_simple', display_name="Trust Game (simple version from tutorial)", num_demo_participants=2,
#      app_sequence=['trust_simple']),
