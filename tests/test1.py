test_serie = [
    {   'name'      : 'test1',
        'url'       : 'https://www.internike.com',
        'do'        : [],
        'check'     : lambda browser: browser.find_elements_by_css_selector('img[src$="internike.png"]')
    }
]    
