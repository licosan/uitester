from selenium.webdriver.support.ui import WebDriverWait

baseurl = 'https://eismea.internike.com'

def check_route_ready(browser):
    return browser.execute_script('return window.Router.route_ready;')

def wait_for_router_ready(browser):
    WebDriverWait(browser, 5).until(lambda browser: browser.execute_script('return window.Router.route_ready;'))

def change_role(browser, role):
    def chrl(browser):
        return(browser.execute_script('myrole = arguments[0];return(true);', role));
    WebDriverWait(browser, 5).until(chrl)

    

test_serie = [
    {   'name'      : 'defaultroute1',
        'desc'      : """Trying non-existing route to defaultRoute""",
        'url'       : baseurl + '/doesnotexist',
        'todos'     : [ {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Doh, this app does not serve this URL !' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'defaultroute2',
        'desc'      : """Trying that "/" is routed to "defaultRoute.modulesChoice" """,
        'url'       : baseurl + '',
        'todos'     : [ {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Choose your module' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },    
    {   'name'      : 'home',
        'desc'      : """Trying that "/app1" is routed app1.app1MainCtrl, method forced to "home" by config""",
        'url'       : baseurl + '/app1',
        'todos'     : [ {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Called home' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'dynamicmethod1',
        'desc'      : """Trying that "/app1/helloWorld" is routed app1.app1MainCtrl, 
                         method "helloWorld" taken from URL""",
        'url'       : baseurl + '/app1/helloWorld',
        'todos'     : [ {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Called helloWorld' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'defaultroute3',
        'desc'      : """Trying that "/app1/badmethod" is routed to defaultRoute,
                         with "Could not find method" error""",
        'url'       : baseurl + '/app1/badmethod',
        'todos'     : [ {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: ('Doh, this app does not serve this URL !' in browser.find_element_by_css_selector('body').text) 
                                  and ('Error: Could not find method' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },          
    {   'name'      : 'params1',
        'desc'      : """Trying that "/app1/user/123X" is routed to UserCtrl, method "userDetails",
                         dynamic param uid=123, no param validation""",
        'url'       : baseurl + '/app1/user/123X',
        'todos'     : [ {'function': change_role, 'args': ['suckeleer']},
                        {'function': wait_for_router_ready, 'args': []} 
                      ],
        'check'     : lambda browser: ('Called userDetails' in browser.find_element_by_css_selector('body').text) 
                                  and ( '"uid":"123X' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    }, 
    {   'name'      : 'params2',
        'desc'      : """Trying that "/app1/user/123X" is routed to UserCtrl, method "userDetails", 
                         dynamic param uid=123 + fixed param, no param validation""",
        'url'       : baseurl + '/app1/user/123X',
        'todos'     : [ {'function': change_role, 'args': ['dikkenek']},
                        {'function': wait_for_router_ready, 'args': []},                          
                      ],
        'check'     : lambda browser: ('Called userDetails' in browser.find_element_by_css_selector('body').text) 
                                  and ( '"uid":"123' in browser.find_element_by_css_selector('body').text)
                                  and ( '"extended":true' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },     
]    
