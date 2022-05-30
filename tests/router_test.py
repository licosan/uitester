from selenium.webdriver.support.ui import WebDriverWait

baseurl = 'https://eismea.internike.com'

def check_route_ready(browser):
    return browser.execute_script('return window.Router.route_ready;')

def wait_for_router_ready(browser):
    WebDriverWait(browser, 5).until(lambda browser: browser.execute_script('return window.Router.route_ready;'))

def launch_router(browser, role):
    def chrl(browser):
        return(browser.execute_script('route(arguments[0]);return(true);', role));
    WebDriverWait(browser, 5).until(chrl)

def check_for_class(browser, classname):
    return browser.execute_script('return(app.LoadedClasses.hasOwnProperty(arguments[0]));', classname)

def show_var(browser, varname):
    return '%s' %browser.execute_script("""return(%s);""" %varname)

def router_makelink(browser, ctrl, meth, params):
    return browser.execute_script("""return(window.Router.makelink('%s','%s',%s));""" %(ctrl, meth, params))


test_serie = [
    {   'name'      : 'defaultroute1',
        'desc'      : """Trying non-existing route to defaultRoute""",
        'url'       : baseurl + '/doesnotexist',
        'todos'     : [ {'function': launch_router, 'args': ['']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Doh, this app does not serve this URL !' in browser.find_element_by_css_selector('body').text
                                  and 'Error: No route found for this URL' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'defaultroute2',
        'desc'      : """Trying if "/" is routed to "defaultRoute.modulesChoice" """,
        'url'       : baseurl + '',
        'todos'     : [ {'function': launch_router, 'args': ['']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Choose your module' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },  
    {   'name'      : 'defaultroute3',
        'desc'      : """Trying if "/" is routed to "defaultRoute.ExpertmodulesChoice" for role expert """,
        'url'       : baseurl + '',
        'todos'     : [ {'function': launch_router, 'args': ['expert']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Choose your expert module' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'home',
        'desc'      : """Trying if "/app1" is routed app1.app1MainCtrl, method forced to "home" by config""",
        'url'       : baseurl + '/app1',
        'todos'     : [ {'function': launch_router, 'args': ['']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Called home' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'dynamicmethod1',
        'desc'      : """Trying if "/app1/helloWorld" is routed app1.app1MainCtrl, 
                         method "helloWorld" taken from URL""",
        'url'       : baseurl + '/app1/helloWorld',
        'todos'     : [ {'function': launch_router, 'args': ['']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: 'Called helloWorld' in browser.find_element_by_css_selector('body').text,
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'defaultroute4',
        'desc'      : """Trying if "/app1/badmethod" is routed to defaultRoute,
                         with "Could not find method" error""",
        'url'       : baseurl + '/app1/badmethod',
        'todos'     : [ {'function': launch_router, 'args': ['']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: ('Doh, this app does not serve this URL !' in browser.find_element_by_css_selector('body').text) 
                                  and ('Error: Could not find method' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },          
    {   'name'      : 'params1',
        'desc'      : """Trying if "/app1/user/123X" as "suckeleer" is routed to UserCtrl, method "userDetails",
                         dynamic param uid=123X, no param validation""",
        'url'       : baseurl + '/app1/user/123X',
        'todos'     : [ {'function': launch_router, 'args': ['suckeleer']},
                        {'function': wait_for_router_ready, 'args': []} 
                      ],
        'check'     : lambda browser: ('Called userDetails' in browser.find_element_by_css_selector('body').text) 
                                  and ( '"uid":"123X' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    }, 
    {   'name'      : 'params2',
        'desc'      : """Trying if "/app1/user/123X" as "dikkenek" is routed to UserCtrl, method "userDetails", 
                         dynamic param uid=123X + fixed param, no param validation""",
        'url'       : baseurl + '/app1/user/123X',
        'todos'     : [ {'function': launch_router, 'args': ['dikkenek']},
                        {'function': wait_for_router_ready, 'args': []},                          
                      ],
        'check'     : lambda browser: ('Called userDetails' in browser.find_element_by_css_selector('body').text) 
                                  and ( '"uid":"123X' in browser.find_element_by_css_selector('body').text)
                                  and ( '"extended":true' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },     
    {   'name'      : 'params3',
        'desc'      : """Trying if "/app1/user/123X" as "denbaas" fails on param validation, and therefore ends up in 
                         app1MainCtrl looking for method user, which does not exist => default page""",
        'url'       : baseurl + '/app1/user/123X',
        'todos'     : [ {'function': launch_router, 'args': ['denbaas']},
                        {'function': wait_for_router_ready, 'args': []},                          
                      ],
        'check'     : lambda browser: ('Doh, this app does not serve this URL !' in browser.find_element_by_css_selector('body').text) 
                                  and ( 'Could not find method "user" in class app1MainCtrl' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    }, 
    {   'name'      : 'index',
        'desc'      : """Trying if "/app2/" is routed to app2MainCtrl,
                         with method defaulting to index""",
        'url'       : baseurl + '/app2/',
        'todos'     : [ {'function': launch_router, 'args': ['']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: ('Called index' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'role1',
        'desc'      : """Trying if "/app2/proposals" is routed to for user not po or paco is routed to app2MainCtrl, 
                         method proposals which should not be found ! => default route""",
        'url'       : baseurl + '/app2/proposals',
        'todos'     : [ {'function': launch_router, 'args': ['']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: ('Doh, this app does not serve this URL !' in browser.find_element_by_css_selector('body').text)
                                  and ('Doh, this app does not serve this URL !' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },       
    {   'name'      : 'role2',
        'desc'      : """Trying if "/app2/proposals" is routed to app2proposalsCtrl, method list""",
        'url'       : baseurl + '/app2/proposals',
        'todos'     : [ {'function': launch_router, 'args': ['paco']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: ('Called list' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    }, 
    {   'name'      : 'split_params',
        'desc'      : """Trying if "/app2/proposal/987/reviews/456" takes separated parameters properly""",
        'url'       : baseurl + '/app2/proposal/987/reviews/456',
        'todos'     : [ {'function': launch_router, 'args': ['paco']},
                        {'function': wait_for_router_ready, 'args': []} ],
        'check'     : lambda browser: ('Called getOneReview' in browser.find_element_by_css_selector('body').text)
                                  and ( '{"pid":"987","rid":"456"}' in browser.find_element_by_css_selector('body').text),
        'debuginfo' : lambda browser: 'Content: %s\n' %browser.find_element_by_css_selector('body').text,
    },
    {   'name'      : 'dependency_helper',
        'desc'      : """Trying if "/app1/user/123X" loads dependency class "userHelper" """,
        'url'       : baseurl + '/app1/user/123X',
        'todos'     : [ {'function': launch_router, 'args': ['dikkenek']},
                        {'function': wait_for_router_ready, 'args': []},
                      ],
        'check'     : lambda browser: check_for_class(browser, 'userHelper'),
        'debuginfo' : lambda browser: show_var(browser, 'app'),
    },  
    {   'name'      : 'makelink1',
        'desc'      : """Trying if makelink('app1/app1MainCtrl','home',{}) gives "/app1"  """,
        'url'       : baseurl + '/',
        'todos'     : [ {'function': launch_router, 'args': ['toto']},
                        {'function': wait_for_router_ready, 'args': []},
                      ],
        'check'     : lambda browser: router_makelink(browser, 'app1/app1MainCtrl','home','{}') == '/app1',
        'debuginfo' : lambda browser: router_makelink(browser, 'app1/app1MainCtrl','home','{}'),
    },          
    {   'name'      : 'makelink2',
        'desc'      : """Trying if makelink('/common/User/UserCtrl','userDetails',{'uid':'789'}) gives "/app1/user/789"  """,
        'url'       : baseurl + '/',
        'todos'     : [ {'function': launch_router, 'args': ['dikkenek']},
                        {'function': wait_for_router_ready, 'args': []},
                      ],
        'check'     : lambda browser: router_makelink(browser, '/common/User/UserCtrl','userDetails',"""{'uid':'789'}""") == '/app1/user/789',
        'debuginfo' : lambda browser: 'result:'+router_makelink(browser, '/common/User/UserCtrl','userDetails',"""{'uid':'789'}"""),
    },  

]    
