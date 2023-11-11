from microsoft_rewards import get_microsoft_creds, get_microsoft_otp


if __name__ == "__main__":
    try:
        print(get_microsoft_creds())
    except ValueError as e:
        print("An error occurred while reading Microsoft credentials:", e)

    try: 
        print(get_microsoft_otp())

    except ValueError as e:
        print("An error occurred while reading Microsoft otp:", e)
