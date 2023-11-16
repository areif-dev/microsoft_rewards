# All rewards cards components called 'mee-card'.
# 'mee-card'[3: 6] are tomorrow's set and should be skipped

# For the daily quizzes, the answers are a.wk_choicesInstLink
# The next question button is input[type=submit][name=submit]

# The first daily poll option is #btoption0
# Might be able to tell if the daily poll is open by checking for .bt_title.b_promtxt

# For the warpspeed quizzes, the start button is at input#rqStartQuiz[type=button].
# The options are at input.rqOption

from selenium.webdriver.common.by import By
from microsoft_rewards import DRIVER, WAIT_PERIOD, try_await_element
import time


def handle_daily_set():
    """
    :raises: :exc: Raise `selenium.common.exceptions.TimeoutException` if the
    daily set cards are not found within `WAIT_PERIOD`
    """

    # First make sure that the rewards cards have loaded
    try_await_element("mee-rewards-daily-set-item-content")
    time.sleep(WAIT_PERIOD)
    all_daily_sets = DRIVER.find_elements(
        By.XPATH, "//mee-rewards-daily-set-item-content/div/a"
    )

    for i, card in enumerate(all_daily_sets[0:3]):
        print(i)
        card.click()

        try:
            try_await_element("a.wk_choicesInstLink")
            print("Found daily quiz")
            continue
            # handle_daily_quiz()
        except:
            pass

        try:
            try_await_element("#btoption0")
            print("Found daily poll")
            continue
            # handle_daily_poll()
        except:
            pass

        try:
            try_await_element("input#rqStartQuiz[type=button]")
            print("Found warpspeed quiz")
            continue
            # handle_warpspeed_quiz()
        except:
            pass

        print("Found freebee")
