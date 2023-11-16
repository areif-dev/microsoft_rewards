from microsoft_rewards.authentication import microsoft_login
from microsoft_rewards.rewards import handle_daily_set


if __name__ == "__main__":
    microsoft_login()
    handle_daily_set()
