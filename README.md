## UITESTER
uitester is a small wrapping script around Selenium to ease the writing & execution of end-to-end testing.
It is meant to be launched from a console.

**usage:** uitester [-h] [--chrome] [--firefox] [--single SINGLE] testfile

positional arguments:  
testfile         Test serie (python file in folder ./tests)  
   
optional arguments:  
-h, --help       show the help message and exit  
--chrome         test in Chrome  
--firefox        test in Firefox  
--single         Name of the single test to make (if not present, performs all tests)  
  
  
  
Your testing scenario is written in a Python testfile as a dict.
Each test entry has :
- **name** : A (short) name of the test, usefull when you want to lauch a single test instead of the whole scenario.

- **desc** : A long description of the test, what it is supposed to do and to assert.

- **url**  : The URL to give the browser for this test.

- **todos** : A list of dicts like {'function': fn, 'args': arguments to pass to that function}.
          This is a list of pseudo-user actions / things to wit for to do once the page is loaded.
          They are executed in sequence, and in a synchronous (blocking) way.
          You can of course use lambda, of more complex (Python) functions defined in your test file.
          In your actions, use Selenium "WebDriverWait" to wait for some condition on the page to be true (like presence of a DOM element).
          Use Selenium "execute_script" to interact with the javascipt of the page (like inject some data).
          Using both together, you can wait for some javascript condition to be true (like some post-process js callback)
- **check** : The function (typically a lambda) that should return True or False for the test to succeed or fail.
          Here too, use Selenium functions to test for content/ DOM nodes etc, or use "execute_script" to test some javascript things.
- **debuginfo** : A function that will be called when the test fails, to get a text displayed as debugging information.
              He you typically want to show if a DOM element was found or not, show fragments of html, or some javascript values.

## INSTALL
**Prerequisites (Linux):** python3, virtualenv, pip3, /usr/bin/env

Clone the rep, and make your virtualenv
```sh
git clone git@github.com:licosan/uitester.git
cd uitester
virtualenv -p python3 pyvenv
. ./pyvenv/bin/activate
```

Now check you are in python3 (min 3.6)
```sh
python -V
```
Now install uitester required libs:
```sh
pip install -r requirements.txt
```
To be able to test with Firefox, you need to install geckodriver (see: https://github.com/mozilla/geckodriver)
```sh
sudo apt-get install firefox-geckodriver
```
 
To be able to test with Chrome, you need to install chromedriver (see: https://chromedriver.chromium.org/downloads)
```sh 
 sudo apt-get install chromium-chromedriver
```

You should now be ready to go...
First check the script is launching properly (won't yet use a browser web driver)
```sh
./uitester --help
```

Now launch the test your created (the python definition script you saved in the tests folder) with one or both browsers:
```sh
./uitester --help./uitester --firefox --chrome my_test
```

## TEST FILES
A test file is a python script that mainly defines a list called **test_serie**
Elements of that list are dictionaries of the form:
```python
    {   'name'      : 'test1',
        'desc'      : """The first test ever.""",
        'url'       :'https://mydomain/app1/user/123X',
        'todos'     : [ {'function': launch_js_action, 'args': ['toto']},                        
                      ],
        'check'     : lambda browser: ('helloworld' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },   
```
**name** is the shortname of this particular test. 
It is used when you call uitester with "--single" to launch only that test instead of the whole serie.

**desc** is the long description of this test. Displayed when the test fails. (Therefore, be cool with others or your future-self:
Explain precisely in what was tested & how)

**url** the url that will be fetched. As this is a UI tester, only GET is foreseen for now.

**todos** a list of actions that will be performed before the check is made. 
this is the place you trigger wait for things to happen on the page, you make fake user actions (like click somewhere), 
you launch javascript code, or wait for javascript results.
Each action is of the form: {'function': myfunc, 'args': [arg2, arg3]}
The first argument of the function is always the selenium browser instance (on which you call selenium methods), then eventual other parguments passed in args. You'll find some cool functions in the boilerplate example below ...

**check** a function (often a lambda) receiving the selenium browser instance, that shall return True if the test succeeds

**debuginfo** a function (often a lambda) receiving the selenium browser instance, that shall return a string containing some debug info, displayed when the test fails, to help understand why. Showing the source of the page is a basic typical example, but you could also dump some javascript variables for example.

## TEST FILE Example / Boilerplate
```python
from selenium.webdriver.support.ui import WebDriverWait

baseurl = 'https://www.mydomain.com'

def check_js_variable_true(browser):
    return browser.execute_script('return myvariable;')

def wait_js_variable_true(browser):
    WebDriverWait(browser, 10).until(lambda browser: browser.execute_script('return myvariable;'))

def launch_js_function(browser, myarg):
    def chrl(browser):
        return(browser.execute_script('myfunc(arguments[0]);return(true);', myarg));
    WebDriverWait(browser, 10).until(chrl)

def show_var(browser, varname):
    return '%s' %browser.execute_script("""return(%s);""" %varname)


def wait_for_correct_current_url(browser, target_url):
    WebDriverWait(browser, 10).until(
        lambda driver: browser.current_url == target_url)

test_serie = [
    {   'name'      : 'test1',
        'desc'      : """The first test, well described ;-) """,
        'url'       : baseurl + '/helloworld',
        'todos'     : [  {'function': wait_for_correct_current_url, 'args': ['https://www.mydomain.com/login']}, ]
        'check'     : lambda browser: 'Please login' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
]    

```

