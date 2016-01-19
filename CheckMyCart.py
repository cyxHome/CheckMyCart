import urllib
import urllib2
from BeautifulSoup import *
import getpass

# Data.
def crawl(username, password):
    while True:
        try:
            data = {
                'netid': username,
                'password': password,
                'Submit': 'Login'
            }
            hdr = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }

            # step1: get the student center home page, grab the new allocated action url.

            url = "http://css.adminapps.cornell.edu/"
            tmp = urllib.urlopen(url)
            login_page = tmp.read()

            login_url = tmp.geturl()[0:30]+'/'

            f1 = open('login_page.html', 'w')  # write to a html file for debug
            f1.write(login_page);

            soup_login = BeautifulSoup(login_page)
            form_login = soup_login.find(id="content").form
            action_url = form_login['action']

            # step2: send post request to the action url, login via the web3 server,
            #        grab the redirect link

            cookie_handler= urllib2.HTTPCookieProcessor()
            redirect_handler= urllib2.HTTPRedirectHandler()
            opener = urllib2.build_opener(redirect_handler, cookie_handler)



            login_url = login_url + action_url
            encoded_data = urllib.urlencode(data)
            # req = urllib2.Request(login_url, data=encoded_data, headers=hdr)
            # redirect_page = urllib2.urlopen(req).read()
            opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')]
            redirect_page = opener.open(login_url, data=encoded_data).read()


            f2 = open('redirect_page.html', 'w')
            f2.write(redirect_page)

            soup_redirect = BeautifulSoup(redirect_page)
            form_redirect = soup_redirect.find(id="content").form
            home_url = form_redirect['action']
            wa = form_redirect.input['value']
            wa = wa.encode('ascii','ignore')
            data_redirect = {
                'wa': wa
            }
            encoded_data = urllib.urlencode(data_redirect)

            print "The information will be ready very soon..."


            # step3: send post request in the redirect_page, finally get to the logined
            #        homepage.


            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')]
            home_page = opener.open(home_url, data=encoded_data).read()
            f3 = open('home_page.html', 'w')
            f3.write(home_page)


            target_url = "https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A"
            cart_page = opener.open(target_url).read()
            f4 = open('cart_page.html', 'w')
            f4.write(cart_page)
            break
        except:
            print "Oops!  Something wrong.  Try again..."

    cart_soup = BeautifulSoup(cart_page)
    for i in range(20):
        course_id = 'win0divP_CLASS_NAME$' + str(i)
        status_id = 'win0divDERIVED_REGFRM1_SSR_STATUS_LONG$' + str(i)
        class_info = cart_soup.findAll(id=course_id)
        status_info = cart_soup.findAll(id=status_id)
        if (len(class_info) > 0):
            print class_info[0].getText()
            print status_info[0].div.img['alt']

if __name__ == "__main__":
    print "Welcome!"
    username = raw_input('NetId: ')
    password = getpass.getpass('Password: ')
    print "Thanks, Please wait..."
    crawl(username, password)
