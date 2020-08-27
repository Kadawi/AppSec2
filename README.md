# Application Security Assignment 2

[![Build Status](https://travis-ci.com/Kadawi/AppSec2.svg?branch=master)](https://travis-ci.com/Kadawi/AppSec2)

My coursework for the second Application Security assignment, which introduces secure web development. 

## Goals

* Turn the spell checking system from [Assignment 1](https://www.github.com/Kadawi/AppSec/) into a Web service using Flask
* Focus on the security of the Web service
* Test the web service to ensure it is not vulnerable to common attacks
* Continue to use secure development practices established in Assignment 1

## High Level Functionality Requirements 
* A user registers to the service. This registration must persist until the application is closed, but does not need to persist after the Web service is exited.
* A user logs into the Web service.
* A user submits text to be checked by the spell checker. The binary for the spell checker is supplied on NYU Classes.
* The Web service code calls the binary spell checker program.
* The Web service code received the output of the spell checker program deals with it according to section result retrieval above.

## Assignment Requirements - Part 1
* Application to launch with the command `flask run`
* Web service must provide at least the following functionality, at the following locations:
  * User registration: /your/webroot/register
  * User login: /your/webroot/login
  * Mock Two-factor authentication: /your/webroot/login
  * Text submission: /your/webroot/spell_check
  * Result retrieval: /your/webroot/spell_check
* Registration:
  * A form for user input with username, password, and 2fa (essentially just a pin) code.
  * Implement standard rules of registration (Unique usernames, etc.)
  * When registration is complete, show a success/failure message
* Login:
  * Input for username, password, and pin
  * Return with "incorrect" for incorrect uname or pword
  * Return with success upon successful login and set up session
* Text Submission:
  * Allow logged-in user to submit text inside of a text area
  * Web service takes the text and uses the spell-checker from Assignment 1 to determine misspelled words (spell check binary is a.out)
* Result Retrieval
  * Web service must output the results to user with the supplied text in an element with id=textout and the misspelled words, separated by commas, in an element with id=misspelled.
* Use Tox for functional testing

## Part 2: Security Requirements
* Implement defenses for common web attacks:
    * Allowlisting, encoding/decoding, browser headers, etc.
* Defend against: 
  * XSS, CSRF, session hijacking, Command injection, etc.
  * SQLi not necessary due to lack of database (duh)
* Attack web service to determine existence of common vulnerabilites.
  * Patch
* Write a report of mitigations, vulnerabilities, and patches implemented/encountered. (Not included here)
