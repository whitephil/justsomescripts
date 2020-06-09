from arcgis.gis import GIS #https://developers.arcgis.com/python/guide/install-and-set-up/
from arcgis.gis import ContentManager
import csv
import os
import time

os.chdir('C:\\Users\\phwh9568\\AGOLpy')
timestamp = time.strftime('%Y_%m_%d')

ucb_ago = GIS("https://ucboulder.maps.arcgis.com", "philip.white_ucboulder", "#####")

cm = ContentManager(ucb_ago)

ucb_users = ucb_ago.users.search(max_users = 2500)

print ('total users=', len(ucb_users)) # print (ucb_users) would list every user name

ignore_list = ['sitelic', 'philip.white_ucboulder'] #myself and another admin account

#Date needs to be in unix epoch time
#See https://www.epochconverter.com to come up with your unix date (or do it in Python I guess)
#Accounts created prior to Sept 1 2018 that have never logged in.
Created1yrago_Never = list([])
for user in ucb_users:
    if not user.username in ignore_list:
        if user.created < 1504569600000:
            if user.lastLogin < 1:
                Created1yrago_Never.append(user.username)
                #print(user.username)
                #print(user.created)
print("Created past year but never logged-in: ", len(Created1yrago_Never))

#Accounts created since Sept 1 2018 that have never logged in
CreatedPastYear_Never = list([])
for user in ucb_users:
    if not user.username in ignore_list:
        if user.created > 1504569600000:
            if user.lastLogin < 1:
                CreatedPastYear_Never.append(user.username)
                #print(user.username)
                #print(user.created)
print('Created prior to 1 year ago, never logged-in: ', len(CreatedPastYear_Never))

#Accounts created prior to Sept 1 2018, have not logged in since before Sept 1 2018 and have no content
OneYrNoLogIn_NoContent = list([])
for user in ucb_users:
    if not user.username in ignore_list:
        if user.created < 1504569600000:
            if user.lastLogin < 1504569600000:
                if len(user.items()) <1:
                    OneYrNoLogIn_NoContent.append(user.username)
                    #print(user.username)
                    #print(user.created)

print('Created prior to 1 year ago, have not logged-in in 1 year, but have content: ', len(OneYrNoLogIn_NoContent))

#Accounts that have logged in since Sept 1 2018 and have no content
OneYrLogIn_NoContent = list([])
for user in ucb_users:
    if not user.username in ignore_list:
        if user.lastLogin > 1504569600000:
            if len(user.items()) <1:
                OneYrLogIn_NoContent.append(user.username)
                #print(user.username)
                #print(user.created)

print('Logged-in in past year but have no content: ', len(OneYrLogIn_NoContent))

#Accounts created prior to Sept 1 2018, have not logged in since before Sept 1 2018 and HAVE content
OneYrNoLogIn_Content = list([])
for user in ucb_users:
    if not user.username in ignore_list:
        if user.lastLogin > 1:
            if user.lastLogin < 1504569600000:
                if len(user.items()) > 0:
                    OneYrNoLogIn_Content.append(user.username)
                    #print(user.username)
                    #print(user.created)

print ('Have not logged-in during past year but have content: ', len(OneYrNoLogIn_Content))

#Accounts created prior to Sept 1 2018, HAVE logged in since Sept 1 2018 and HAVE content
OneYrLogIn_Content = list([])
for user in ucb_users:
    if not user.username in ignore_list:
        if user.lastLogin > 1504569600000:
            if len(user.items()) > 0:
                OneYrLogIn_Content.append(user.username)
                #print(user.username)
                #print(user.created)

print('Have logged on in past year, have content (aka active users): ', len(OneYrLogIn_Content))

#CHECK to make sure all of the lists add up to total ucb_users list:
allUsers = len(OneYrLogIn_Content)+len(OneYrNoLogIn_Content)+len(OneYrLogIn_NoContent)+len(OneYrNoLogIn_NoContent)+len(CreatedPastYear_Never)+len(Created1yrago_Never)

if allUsers == len(ucb_users) - len(ignore_list):
    print ('Sum of lists: ', allUsers, '; ucb_users:', len(ucb_users), '; Yay!')
else:
    print ('Sum of lists: ', allUsers, '; ucb_users:', len(ucb_users), '; ...Oops!')

#Write the OneYrNoLOgIn_Content to a csv so you can email those users and tell them to log-in to keep their Accounts
with open('OneYrNoLogIn_Content_'+timestamp+'.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['Name','User Name','Email', 'Role'])
    for user in OneYrNoLogIn_Content:
        account = ucb_ago.users.get(user)
        if account.role == 'org_admin': #Just in case there is an admin on this list, we will skip them.
            pass
        else:
            fullName = account.fullName
            email = account.email
            role = account.role
            writer.writerow([fullName, user, email, role])

#Happy? Okay, proceed...
#Create delete list & keep list:
deleteList = OneYrNoLogIn_Content + OneYrNoLogIn_NoContent + Created1yrago_Never
keepList = CreatedPastYear_Never + OneYrLogIn_NoContent + OneYrLogIn_Content

print('deleteList length: ', len(deleteList))
print('keepList length: ', len(keepList))

#Do math to double check that lists are correct:

if len(deleteList) == (len(ucb_users) - len(ignore_list)) - len(keepList):
    print ('ucb_users = ', len(ucb_users) - len(ignore_list))
    print (len(deleteList), "+", len(keepList), "=", (len(keepList)+len(deleteList)))
    print ('All good!')
else:
    print ('ucb_users = ', len(ucb_users))
    print (len(deleteList), "+", len(keepList), "=", (len(keepList)+len(deleteList)))
    print ('...woops')

#Write the delete list to a csv:
with open('deleteList_'+timestamp+'.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['userName'])
    for user in deleteList:
        account = ucb_ago.users.get(user)
        if account.role == 'org_admin': #Just in case there is an admin on this list, we will skip them.
            pass
        else:
            writer.writerow([user])
