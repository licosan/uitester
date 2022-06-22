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
**Prerequisites:** python3, virtualenv & Pip3 

```sh
git clone git@github.com:licosan/uitester.git
cd uitester
virtualenv -p python3 pyvenv
. ./pyvenv/bin/activate
```

