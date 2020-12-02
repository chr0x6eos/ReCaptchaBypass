#!/usr/bin/env python3

import speech_recognition
from typing import Optional
from warnings import filterwarnings
from time import sleep
from os import system, remove
from pydub import AudioSegment
from selenium import webdriver
from requests import get
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException

# Ignore selenium deprecation warnings for socks-proxy options
filterwarnings("ignore", category=DeprecationWarning) 

class ReCaptchaBypass:
    """ReCaptcha v2 bypass
    
    - How it works:
    1.) Select audio-challenge option
    2.) Find and download audio-file
    3.) Use speech-recognition to detect text
    4.) Submit text
    5.) Profit
    """

    # Current IP
    ip = "127.0.0.1"
    # Browser driver
    browser = None
    # Link to audio file
    audio_link = ""
    # Challenge text
    chal_text = ""

    #### SETTINGS ####
    # Host to access
    host = "https://www.google.com/recaptcha/api2/demo"
    # Verbosity, (0:None, 1:Default, 2:Full)
    verbose = 1
    # Should tor be used?
    tor = False
    # Auto submit form afterwards
    auto_submit = True
    # Language to detect
    lang = "en-EN"
    # Browser settings profile
    profile = None

    def __init__(self, host:Optional[str] = "", verbose:Optional[int] = 1, tor:Optional[bool] = False, auto_submit:Optional[bool] = True, language:Optional[str] = "en-EN", options = "") -> None:
        """Initializes an instance of the RecaptchaBypasser class with the specified options"""
        self.set_host(host)

        # TODO: CREATE SETTERS FOR THESE VARS
        self.verbose = verbose
        self.tor = tor
        self.auto_submit = auto_submit
        self.lang = language

        # Print if verbose > 0
        if self.verbose > 0 : self.print_logo()

        if self.tor:
            self.start_tor()
        # TODO: IMPLEMENT BROWSER OPTIONS
        self.set_profile(options)
        self.start_browser()

    # Print logo
    def print_logo(self) -> str:
        print("""
     _____       _____            _       _                      ____                            
    |  __ \     / ____|          | |     | |                    |  _ \                           
    | |__) |___| |     __ _ _ __ | |_ ___| |__   __ _   ______  | |_) |_   _ _ __   __ _ ___ ___ 
    |  _  // _ \ |    / _` | '_ \| __/ __| '_ \ / _` | |______| |  _ <| | | | '_ \ / _` / __/ __|
    | | \ \  __/ |___| (_| | |_) | || (__| | | | (_| |          | |_) | |_| | |_) | (_| \__ \__ \\
    |_|  \_\___|\_____\__,_| .__/ \__\___|_| |_|\__,_|          |____/ \__, | .__/ \__,_|___/___/
                           | |                                          __/ | |                  
                           |_|                                         |___/|_|                  
     ____           _____ _           ___         __        ____                                 
    |  _ \         / ____| |         / _ \       / /       / __ \                                
    | |_) |_   _  | |    | |__  _ __| | | |_  __/ /_   ___| |  | |___                            
    |  _ <| | | | | |    | '_ \| '__| | | \ \/ / '_ \ / _ \ |  | / __|                           
    | |_) | |_| | | |____| | | | |  | |_| |>  <| (_) |  __/ |__| \__ \                           
    |____/ \__, |  \\_____|_| |_|_|   \\___//_/\_\\\___/ \___|\____/|___/                           
            __/ |                                                                                
           |___/                                                                                 

Twitter:    https://twitter.com/Chr0x6eOs
Github:     https://github.com/Chr0x6eOs 
___________________________________________________________________________________________________
        """)

    # Set host to access
    def set_host(self, host:Optional[str]) -> None:
        """Defines the web-host to bypass the captcha"""
        if host != "":
            self.host = host
        else:
            # Use captcha as demo
            self.host = "https://www.google.com/recaptcha/api2/demo"

    # Setup browser profile
    def set_profile(self, options, type:str = "firefox") -> None:
        """Setup the browser profile with the specified options"""
        if type == "firefox":
            self.profile = webdriver.FirefoxProfile()
        # Setup tor preferences
        if self.tor:
            self.profile.set_preference('network.proxy.type', 1)
            self.profile.set_preference('network.proxy.socks', "127.0.0.1")
            self.profile.set_preference('network.proxy.socks_port', 9050)

    # Get current IP address
    def update_ip(self) -> None:
        """Set the ip-variable to the currently assigned IP"""
        try:
            if self.tor:
                self.ip = get('https://api.ipify.org', proxies={'http':'socks5://127.0.0.1:9050','https':'socks5://127.0.0.1:9050'}, timeout=5).text
            else:
                self.ip = get('https://api.ipify.org', timeout=5).text
            if self.verbose > 0 : print(f"[*] Updated ip: {self.ip}")
        except:
            sleep(3)
            self.update_ip()

    # Start tor
    def start_tor(self) -> None:
        """Start the tor service and query the current ip"""
        try:
            system('service tor restart')
            sleep(1)
            self.change_ip()
        except:
            sleep(1)
            self.start_tor()

    # Change tor ip    
    def change_ip(self) -> None:
        """Reload tor service to get a new ip"""
        if self.tor:
            try:                                                   
                system('service tor reload') # Reload to get new IP
                # Query new ip
                self.update_ip()
            except:
                # Retry                                            
                sleep(1)
                self.change_ip()

    # Create browser instance
    def start_browser(self) -> None:
        """Start a browser instance"""
        # TODO: ALLOW DIFFERENT BROWSER TYPES
        # Run browers binary
        self.browser = webdriver.Firefox(executable_path="./geckodriver",firefox_profile=self.profile)
        # Access host
        self.browser.get(self.host)
    
    # Get all iframes
    def get_iframes(self, src:Optional[str]="recaptcha/api2/") -> list:
        """Gets all iframes on page and checks for google captcha frames (defined by src)"""
        # Find all iframes
        if self.verbose > 1 : print("[*] Getting all iframes...")
        iframes = self.browser.find_elements_by_tag_name("iframe")
        frames = []

        # Loop through iframes and find captcha frames
        for iframe in iframes:
            frame_src = iframe.get_attribute("src")
            if src in frame_src:
                frames.append(iframe)  
            if src != "" and self.verbose > 1:
                print(f"[+] Found iFrame with src: {frame_src}")
        return frames

    # Update iFrame
    def update_frame(self, frame_index:int = 0) -> None:
        """Changes context to iframe specified by index"""
        self.browser.switch_to.default_content()
        if frame_index == -1:
            # Switch to default context
            return
        frames = self.get_iframes()
        frame = frames[frame_index]
        # Scroll to frame
        self.browser.execute_script("arguments[0].scrollIntoView();", frame)
        sleep(1)
        # Wait for iframe to be loaded
        self.wait_for_iframes()
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame(frame)
        sleep(1)

    # Wait for iframes to be loaded
    def wait_for_iframes(self, timeout:int=30) -> None:
        """Waits until iframes are loaded on page"""
        wait = WebDriverWait(self.browser, timeout=timeout)
        wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

    # Wait for buttons to be clickable
    def wait_for_button(self, name:str, timeout:int=30) -> None:
        """Waits until button is clickable"""
        wait = WebDriverWait(self.browser, timeout=timeout)
        wait.until(expected_conditions.visibility_of_element_located((By.ID, name)))

    # Getting the link of the audio data
    def get_audio_link(self) -> None:
        """Access captcha and tries to extract audio_link"""
        if self.verbose > 0 : print("[*] Trying to get audio link...")
        # Switch to first frame
        self.update_frame(0)

        # Open captcha
        self.wait_for_button(name="recaptcha-anchor")
        self.browser.find_element_by_id("recaptcha-anchor").click()
        sleep(1)

        # Check if blocked
        if self.blocked():
            self.audio_link = ""
            return
        
        # Switch to captcha frame
        self.update_frame(1)
        # Click audio challenge button
        self.wait_for_button(name="recaptcha-audio-button")
        self.browser.find_element_by_id("recaptcha-audio-button").click()
        # Reload frame
        self.update_frame(1)

        # Check if blocked
        if self.blocked():
            self.audio_link = ""
            return
        
        err = 0
        while self.audio_link == "":
            try:
                if err > 3:
                    return
                self.audio_link = self.browser.find_element_by_tag_name("audio").get_attribute("src")
            except NoSuchElementException:
                sleep(1)
                err += 1 # Retry 3-times

    # Check if we are blocked
    def blocked(self) -> bool:
        """Check if captcha is blocking us"""
        try:
            self.browser.find_element_by_class_name("rc-doscaptcha-header")
            print("[!] We got blocked! Retrying...")
            return True
        except: # If exception occurrs, doscaptcha not found and we were not blocked
            return False

    # Download and convert audio
    def download_convert(self) -> None:
        """Downloads and converts audio.mp3 file to wav"""
        if self.verbose > 0 : print("[*] Downloading and converting audio link...")
        # Download audio
        with open("audio.mp3", "wb") as f:
            f.write(get(self.audio_link).content)
        
        # Convert audio
        AudioSegment.from_mp3("audio.mp3").export("audio.wav", format="wav")
        remove("audio.mp3") # Cleanup

    # Use speech-recognition to get text
    def get_text(self) -> None:
        """Uses speech-rocognition to get audio-challenge response from audio file"""
        # Download and convert audio
        self.download_convert()

        if self.verbose > 0 : print("[*] Trying to recognize text from audio...")
        recognizer = speech_recognition.Recognizer()
        # Get audio
        audio_file = speech_recognition.AudioFile("audio.wav")
        with audio_file as source:
            # Get audio-data
            audio = recognizer.record(source)

        # Recognize text
        try:
            self.chal_text = recognizer.recognize_google(audio, language=self.lang)
        except speech_recognition.UnknownValueError:
            self.chal_text = ""
        except Exception as ex:
            if self.verbose > 0 : print(f"[!] Error occurred on text-recognition: {ex}")

        # Cleanup audio file
        remove("audio.wav")

    # Submit found text
    def submit_text(self) -> None:
        """Submits audio-challenge response"""
        if self.verbose > 0 : print("[*] Submitting audio-challenge response...")
        # Submit input
        inputfield = self.browser.find_element_by_id("audio-response")
        inputfield.send_keys(self.chal_text.lower())
        inputfield.send_keys(Keys.ENTER)

    # Check if challenge was passed
    def challenge_passed(self) -> bool:
        """Checks if auto-challenge was passed"""
        try:
            err_msg = self.browser.find_element_by_class_name("rc-audiochallenge-error-message")
            if self.verbose > 0 : print(f"[!] Did not pass challenge!\nError-message: {err_msg.get_txt()}")
            return False
        except:
            return True

    # Check if capcha was passed
    def check_captcha(self) -> bool:
        """Checks if captcha was passed"""
        try:
            # Switch back to input view
            self.update_frame(0)

            # Check if checkmar is set
            checkmark = self.browser.find_element_by_id("recaptcha-anchor")
            if "recaptcha-checkbox-checked" in checkmark.get_attribute("class"):
                return True
        except Exception as ex:
            if self.verbose > 0 : print(f"[-] Execption: {ex}")
            return False
        return False

    # Solve the captcha
    def solve_captcha(self) -> bool:
        """Searches for ReCaptcha on web-page and tries solve it"""
        # Wait till all iframes are loaded
        self.wait_for_iframes()
        sleep(1)

        self.get_audio_link()
        while self.audio_link == "":
            # Change IP, if tor is used
            self.change_ip()
            # Restart browser
            self.browser.close()
            self.start_browser()
            # Retry
            self.get_audio_link()
        
        if self.verbose > 1 : print(f"[+] Got audio link: {self.audio_link}")
        
        # After getting link, get captcha text
        self.get_text()
        while self.chal_text == "":
            # Change IP, if tor is used
            self.change_ip()
            # Restart browser
            self.browser.close()
            self.start_browser()
            # Retry
            self.get_text()
        
        if self.verbose > 0 : print(f"[+] Got audio-challenge response: {self.chal_text}")

        # After getting captcha audio-challenge, submit the text
        self.submit_text()

        sleep(3)

        if self.check_captcha():
            print("[+] Captcha bypassed!")
            sleep(3)
            # Submit captcha
            if self.auto_submit:
                self.update_frame(-1)
                self.browser.find_element_by_id("recaptcha-demo-submit").click()
            return True
        else:
            print("[-] Could not bypass! Retry?")
            return False
