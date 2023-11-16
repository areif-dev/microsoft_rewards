# All rewards cards components called 'mee-card'.
# 'mee-card'[3: 6] are tomorrow's set and should be skipped

# For the daily quizzes, the answers are a.wk_choicesInstLink
# The next question button is input[type=submit][name=submit]

# The first daily poll option is #btoption0
# Might be able to tell if the daily poll is open by checking for .bt_title.b_promtxt

# For the warpspeed quizzes, the start button is at input#rqStartQuiz[type=button].
# The options are at input.rqOption

from selenium.webdriver.common.by import By
from microsoft_rewards import DRIVER, try_await_element


def handle_daily_set():
    """
    :raises: :exc: Raise `selenium.common.exceptions.TimeoutException` if the
    daily set cards are not found within `WAIT_PERIOD`
    """

    # First make sure that the rewards cards have loaded
    try_await_element("mee-card")
    all_rewards = DRIVER.find_elements(By.CSS_SELECTOR, "mee-card")
    
    for card in all_rewards[0: 3]:
        card.click()

        try:
            try_await_element("a.wk_choicesInstLink")
            print("Found daily quiz")
            # handle_daily_quiz()
        except: 
            pass 

        try: 
            try_await_element("#btoption0")
            print("Found daily poll")
            # handle_daily_poll()
        except: 
            pass

        try: 
            try_await_element("input#rqStartQuiz[type=button]")
            print("Found warpspeed quiz")
            # handle_warpspeed_quiz()
        except:
            pass
