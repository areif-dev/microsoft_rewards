from typing import Tuple

from selenium.webdriver.common.keys import Keys
from . import DRIVER
from . import await_essential_element
import subprocess


def get_microsoft_creds() -> Tuple[str, str]:
    creds = []

    for value_to_fetch in ("username", "password"):
        fetch_command = (
            "kpcli --kdb=$HOME/Sync/secrets.kdbx --pwfile=keepass.txt --command "
            f"\"get Passwords/Gaming/Microsoft {value_to_fetch}\" | sed '/WARNING.*/d' | "
            "sed '/.*It may be opened.*/d' | sed '/Please consider.*/d' | "
            "sed '/https:\\/\\/github.com\\/sponsors\\/hightowe/d'"
        )

        completed_process = subprocess.run(
            fetch_command,
            shell=True,
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if completed_process.returncode == 0:
            creds.append(completed_process.stdout.strip()[5:])
        else:
            raise ValueError(
                f"Failed to parse {value_to_fetch}: {completed_process.stderr}"
            )

    return (creds[0], creds[1])


def get_microsoft_otp() -> str:
    fetch_command = (
        "kpcli --kdb=$HOME/Sync/secrets.kdbx --pwfile=keepass.txt --command "
        f"\"otp Passwords/Gaming/Microsoft\" | sed '/WARNING.*/d' | "
        "sed '/.*It may be opened.*/d' | sed '/Please consider.*/d' | "
        "sed '/https:\\/\\/github.com\\/sponsors\\/hightowe/d'"
    )

    completed_process = subprocess.run(
        fetch_command,
        shell=True,
        executable="/bin/bash",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed_process.returncode == 0:
        return completed_process.stdout.strip()[5:]
    else:
        raise ValueError(f"Failed to parse otp: {completed_process.stderr}")


def microsoft_login():
    DRIVER.get("https://rewards.bing.com")
    if DRIVER.title.lower().startswith("sign in to microsoft"):
        try:
            username, password = get_microsoft_creds()
        except ValueError as e:
            print("Could not log into Microsoft:", e)
            DRIVER.quit()
            return

        username_input = await_essential_element("input#i0116")
        username_input.send_keys(username, Keys.ENTER)

        await_essential_element("#displayName")
        password_input = await_essential_element("input#i0118")
        password_input.send_keys(password, Keys.ENTER)

        try:
            otp = get_microsoft_otp()
        except ValueError as e:
            print("Could not read Microsoft OTP:", e)
            DRIVER.quit()
            return

        otp_input = await_essential_element("input#idTxtBx_SAOTCC_OTC")
        otp_input.send_keys(otp, Keys.ENTER)

        stay_signed_in_btn = await_essential_element("input.win-button#idBtn_Back")
        stay_signed_in_btn.click()
