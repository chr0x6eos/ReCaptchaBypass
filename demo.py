#!/usr/bin/env python3
from recaptcha_bypass import ReCaptchaBypass

if __name__ == "__main__":
    # Initialize Bypass object with host defined, all other options are let default
    bypass = ReCaptchaBypass(host="https://www.google.com/recaptcha/api2/demo")
    # Run bypasser and try to solve captcha
    if not bypass.solve_captcha():
        quit() # If unsuccessful, quit program