from microsoft_rewards import try_await_element, SHORT_WAIT
from microsoft_rewards.authentication import microsoft_login
from microsoft_rewards.rewards import handle_daily_set


if __name__ == "__main__":
    microsoft_login()
    time.sleep(SHORT_WAIT)
    handle_daily_set()
