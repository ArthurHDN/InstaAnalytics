#!/usr/bin/python
'''
Insta Analytics
by Arthur Nunes
@arthurhdn_
'''
import instaloader
import webbrowser
import requests
import logging
import os
import datetime
import getpass

def python_2_html_list(L,type='ol'):
    html_list = '<' + type + '>' + '<li>' + '</li><li>'.join(L) + '</li>' + '</' + type + '>'
    return html_list
	
def python_2_html_dict(D,type='ul'):
    html_list = '<' + type + '>'
    for key,value in D.items():
	    html_list += '<li>' + key + value + '</li>'
    html_list += '</' + type + '>'
    return html_list

def python_2_html_bool(B,type='p'):
	if B:
		B_string = 'Yes'
		color_class = 'text-success'
	else:
		B_string = 'No'
		color_class = 'text-danger'
	html_bool = '<' + type + ' class="' + color_class + '" >' + B_string + '</' + type + '>'
	return html_bool

def download_image(url,filename):
    image_data = requests.get(url).content
    with open(filename, 'wb') as file_handler:
        file_handler.write(image_data)

class InstaAnalytics():
    def __init__(self,username,password):
        # Create a new folder to store current data
        path = os.getcwd()
        now = datetime.datetime.now()
        new_folder = path + '/profile_data/' + username + '_' + now.strftime("%d-%m-%y_%H-%M-%S")
        os.mkdir(new_folder)
        os.chdir(new_folder)
        # Initialize logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fh = logging.FileHandler('InstaAnalytics.log')
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        self.logger.info('-'*28 + '\nInsta Analytics initialized!\n' + '-'*28)
        # Load instagram module
        self.logger.info('Logging in, please wait.')
        self.insta = instaloader.Instaloader()
        self.insta.login(username,password)
        self.profile = instaloader.Profile.from_username(self.insta.context, username)
        self.logger.info('Succesfully logged in!')
        # Fetch instagram data
        self.logger.info('Downloading instagram data, please wait.')
        self.profile_pic_local = 'profile_pic.jpg'
        download_image(self.profile.get_profile_pic_url(),self.profile_pic_local)
        self.profile_details_dict = self.get_profile_details()
        self.followers_count,self.followers_list = self.get_followers()
        self.followees_count,self.followees_list = self.get_followees()
        self.you_dont_follow_back_count,self.you_dont_follow_back_list = self.get_you_dont_follow_back()
        self.not_follows_you_back_count,self.not_follows_you_back_list = self.get_not_follows_you_back()
        self.igtv_posts_count,self.igtv_posts_list = self.get_igtv_posts()
        self.posts_count,self.posts_list = self.get_posts()
        self.logger.info('Succesfully donwloaded instagram data!')      

    def load_web_page(self,template_filename = '../../template.html', web_page_filename='InstaAnalytics.html'):
        self.logger.info('Creating web page.')
        # Load html template
        template = ''
        with open(template_filename, 'r', encoding="utf-8") as file_handler:
            template = file_handler.read()
        # Create local variables with the html data to replace
        TEMPLATE_profile_pic = self.profile_pic_local
        TEMPLATE_user_full_name = self.profile.full_name
        TEMPLATE_username = '@' + self.profile.username
        TEMPLATE_bio = self.profile.biography
        TEMPLATE_profile_details_dict = python_2_html_dict(self.profile_details_dict)
        TEMPLATE_igtv_posts_count = self.igtv_posts_count
        TEMPLATE_posts_count = self.posts_count
        TEMPLATE_followers_count = self.followers_count
        TEMPLATE_followers_list = python_2_html_list(self.followers_list)
        TEMPLATE_followees_count = self.followees_count
        TEMPLATE_followees_list = python_2_html_list(self.followees_list)
        TEMPLATE_not_follows_you_back_count = self.not_follows_you_back_count
        TEMPLATE_not_follows_you_back_list = python_2_html_list(self.not_follows_you_back_list)
        TEMPLATE_you_dont_follow_back_count = self.you_dont_follow_back_count
        TEMPLATE_you_dont_follow_back_list = python_2_html_list(self.you_dont_follow_back_list)
        # Create and open html page
        web_page_content = template.format(**locals())
        with open(web_page_filename, 'w', encoding="utf-8") as file_handler:
            file_handler.write(web_page_content)
            webbrowser.open('file:///'+os.path.abspath(web_page_filename))
            self.logger.info('Done. Enjoy!')
    
    def get_profile_details(self):
        D = dict()
        D['Blocked by viewer:'] = python_2_html_bool(self.profile.blocked_by_viewer)
        D['Followed by viewer:'] = python_2_html_bool(self.profile.followed_by_viewer)
        D['Has blocked viewer:'] = python_2_html_bool(self.profile.has_blocked_viewer)
        D['Has highlight reels:'] = python_2_html_bool(self.profile.has_highlight_reels)
        D['Has public story:'] = python_2_html_bool(self.profile.has_public_story)
        D['Has requested viewer:'] = python_2_html_bool(self.profile.has_requested_viewer)
        D['Has viewable story:'] = python_2_html_bool(self.profile.has_viewable_story)
        D['Is business account:'] = python_2_html_bool(self.profile.is_business_account)
        D['Is private:'] = python_2_html_bool(self.profile.is_private)
        D['Is verified:'] = python_2_html_bool(self.profile.is_verified)
        return D
	
    def get_followers(self):
        followers_list = []
        followers_count = 0
        for follower in self.profile.get_followers():
            followers_list.append(follower.username)
            followers_count += 1
        return (followers_count,followers_list)
        
    def get_followees(self):
        followees_list = []
        followees_count = 0
        for followee in self.profile.get_followees():
            followees_list.append(followee.username)
            followees_count += 1
        return (followees_count,followees_list)

    def get_not_follows_you_back(self):
        not_follows_you_back_list = []
        not_follows_you_back_count = 0
        for followee in self.followees_list:
            if followee not in self.followers_list:
                not_follows_you_back_list.append(followee)
                not_follows_you_back_count += 1
        return (not_follows_you_back_count,not_follows_you_back_list)    

    def get_you_dont_follow_back(self):
        you_dont_follow_back_list = []
        you_dont_follow_back_count = 0
        for follower in self.followers_list:
            if follower not in self.followees_list:
                you_dont_follow_back_list.append(follower)
                you_dont_follow_back_count += 1
        return (you_dont_follow_back_count,you_dont_follow_back_list)

    def get_igtv_posts(self):
        igtv_posts_list = []
        igtv_posts_count = 0
        for igtv_post in self.profile.get_igtv_posts():
            igtv_posts_list.append(igtv_post)
            igtv_posts_count += 1
        return (igtv_posts_count,igtv_posts_list)

    def get_posts(self):
        posts_list = []
        posts_count = 0
        for post in self.profile.get_posts():
            posts_list.append(post)
            posts_count += 1
        return (posts_count,posts_list)
                  
# Unit test
if __name__ == '__main__':
    print('Please log in with your credentials.')
    username = input('Username: ')
    password = getpass.getpass('Password for ' + username + ' : ')
    insta_analytics = InstaAnalytics(username,password)
    insta_analytics.load_web_page()