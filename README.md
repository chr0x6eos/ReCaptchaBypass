# ReCaptchaBypass
Bypassing reCAPTCHA v2 by using the audio-challenge feature

## About
ReCaptchaBypass is a simple proof-of-concept script to bypass Google reCAPTCHA v2.

### How does it work?
The ReCaptchaBypass works by automating user-input using selenium to perform following actions:

1. Click on `I'm not a robot` button
2. Choose `Get audio-challenge`
3. Grabs audio-file-link and download file
4. Uses the `Google speech recognition API` to get the audio-challenge response from the audio-file
5. Submit the challenge response and verify bypass
6. Profit

### Demo
![Demo](./demo/demo.gif)



## Legal notice
Please note that this is a simple proof-of-concept and not a full-fledged software.

**THIS TOOL IS FOR LEGAL PURPOSES ONLY!**

The author is not responsible for any misuse of this software.