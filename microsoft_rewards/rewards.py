from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from microsoft_rewards import DRIVER, SHORT_WAIT, try_await_element
import time
import random


def handle_warpspeed_quiz(): 

    try_await_element("input#rqStartQuiz[type=button]").click()

    for _ in range(3):
        for j in range(3):
            try:
                try_await_element(f"input#rqAnswerOption{j}").click()
                time.sleep(SHORT_WAIT)
            except:
                return


def handle_daily_quiz():
    DRIVER.get("https://www.bing.com/search?q=weekly+quiz")
    time.sleep(SHORT_WAIT)
    while True:
        try:
            print("Looking for answer")
            link = try_await_element("a.wk_choicesInstLink")
            DRIVER.get(str(link.get_attribute("href")))
            time.sleep(SHORT_WAIT)
        except Exception as e:
            print("Did not find answer:", e)
            return

        try: 
            try_await_element("input[type=submit][value='Next question']").click()
        except:
            try_await_element("input[type=submit][value='Get your score']").click()
        time.sleep(SHORT_WAIT)


def handle_daily_set():
    """
    :raises: :exc: Raise `selenium.common.exceptions.TimeoutException` if the
    daily set cards are not found within `WAIT_PERIOD`
    """

    original_window = DRIVER.current_window_handle

    # First make sure that the rewards cards have loaded
    # TODO: Wrap in a try except. On exception, move to the searches
    try_await_element("mee-rewards-daily-set-item-content")
    all_daily_sets = DRIVER.find_elements(
        By.XPATH, "//mee-rewards-daily-set-item-content/div/a"
    )

    for i, card in enumerate(all_daily_sets[0:3]):
        card_text = card.find_element(By.XPATH, ".//h3").text.lower()
        print(card_text)
        card.click()

        for window_handle in DRIVER.window_handles:
            if window_handle != original_window:
                DRIVER.switch_to.window(window_handle)
                break

        if "warpspeed" in card_text:
            try:
                handle_warpspeed_quiz()
            except:
                print("Could not start warpspeed quiz")

        elif "poll" in card_text:
            try:
                try_await_element("#btoption0").click()
            except:
                print("Could not answer daily quiz")

        elif "test" in card_text or "show what you know" in card_text:
            try:
                handle_daily_quiz()
            except:
                print("Could not finish daily quiz")

        time.sleep(SHORT_WAIT)
        DRIVER.close()
        DRIVER.switch_to.window(original_window)


def handle_more_activities():
    more_activies_cards = DRIVER.find_elements(By.CSS_SELECTOR, "mee-rewards-more-activities-card-item")

    for card in more_activies_cards:
        try:
            card.find_element(By.XPATH, ".//span[contains(@class, 'mee-icon mee-icon-AddMedium')]").click()
        except:
            continue


def run_searches():
    print("Running searches")
    lorem = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
    tempor incididunt ut labore et dolore magna aliqua. Sed velit dignissim 
    sodales ut eu sem integer vitae. Elementum sagittis vitae et leo duis ut 
    diam. Bibendum est ultricies integer quis auctor elit sed vulputate. 
    Tellus cras adipiscing enim eu turpis. Turpis massa sed elementum tempus 
    egestas sed sed. Tincidunt dui ut ornare lectus sit. Etiam tempor orci eu 
    lobortis elementum nibh. Cursus euismod quis viverra nibh cras pulvinar 
    mattis nunc sed. Sodales ut etiam sit amet nisl purus in mollis. Faucibus 
    et molestie ac feugiat sed lectus vestibulum. Vulputate dignissim 
    suspendisse in est ante in nibh mauris. Erat imperdiet sed euismod nisi 
    porta lorem mollis. Integer quis auctor elit sed vulputate mi sit amet. 
    In ornare quam viverra orci sagittis eu. Eu scelerisque felis imperdiet 
    proin fermentum. Lobortis mattis aliquam faucibus purus in massa tempor nec. 
    Fusce ut placerat orci nulla pellentesque dignissim enim sit. In metus 
    vulputate eu scelerisque felis imperdiet proin. Nibh praesent tristique 
    magna sit amet purus gravida.
    """.split(" ")

    DRIVER.get("https://www.bing.com/search?q=something")

    for _ in range(30):
        try:
            DRIVER.find_element(By.CSS_SELECTOR, "input#id_a[value='Sign in']").click()
            time.sleep(2)
        except:
            pass

        word_count = random.randint(1, 10)
        words = []
        for _ in range(word_count):
            words.append(random.choice(lorem))

        try:
            search_input = try_await_element("input#sb_form_q")
        except:
            continue

        search_input.clear()
        search_input.send_keys(" ".join(words), Keys.ENTER)
        time.sleep(1)

