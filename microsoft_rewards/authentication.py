from typing import Tuple

from selenium.webdriver.common.keys import Keys
from . import DRIVER, SHORT_WAIT
from . import await_essential_element, try_await_element
import subprocess

import time


def get_microsoft_creds() -> Tuple[str, str]:
    """
    Retrieve the Microsoft username and password from a keepass file using kpcli

    :returns: A tuple containing the username and password for Microsoft
    :raises: `ValueError` if either `username` or `password` fail to fetch
    """

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
            creds.append(completed_process.stdout.strip())
        else:
            raise ValueError(
                f"Failed to parse {value_to_fetch}: {completed_process.stderr}"
            )

    return (creds[0], creds[1])


def get_microsoft_otp() -> str:
    """
    Retrieve the Time based One Time Passcode from the keepass database using
    kpcli

    :returns: The OTP code
    :raises: `ValueError` if OTP cannot be found
    """

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
        return completed_process.stdout.strip()
    else:
        raise ValueError(f"Failed to parse otp: {completed_process.stderr}")


def microsoft_login():
    """Login to a Microsoft rewards account using Selenium"""

    DRIVER.get("https://rewards.bing.com")
    if DRIVER.title.lower().startswith("sign in to microsoft"):
        try:
            print("Getting username and password")
            username, password = get_microsoft_creds()
        except ValueError as e:
            print("Could not log into Microsoft:", e)
            DRIVER.quit()
            return

        username_input = await_essential_element("input#i0116")
        username_input.send_keys(username, Keys.ENTER)
        time.sleep(SHORT_WAIT)

        await_essential_element("#displayName")
        password_input = await_essential_element("input#i0118")
        password_input.send_keys(password, Keys.ENTER)
        time.sleep(SHORT_WAIT)

        try:
            print("Getting OTP")
            otp = get_microsoft_otp()
        except ValueError as e:
            print("Could not read Microsoft OTP:", e)
            DRIVER.quit()
            return

        otp_input = await_essential_element("input#idTxtBx_SAOTCC_OTC")
        otp_input.send_keys(otp, Keys.ENTER)
        time.sleep(SHORT_WAIT)

        for i in range(5):
            try:
                print("Refuse saving login info")
                try_await_element("input.win-button#idBtn_Back").click()
                return
            except:
                print("Could not find button to refuse saving login. Retrying")
                continue
