from microsoft_rewards import try_await_element, SHORT_WAIT
from microsoft_rewards.authentication import microsoft_login
from microsoft_rewards.rewards import handle_daily_set, handle_more_activities, run_searches
import time


if __name__ == "__main__":
    microsoft_login()
    time.sleep(SHORT_WAIT)
    handle_daily_set()

    try:
        try_await_element("mee-rewards-more-activities-card-item")
        handle_more_activities()
    except:
        print("Failed to handle daily activities")

    run_searches()

