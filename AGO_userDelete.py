# PROCEED WITH CAUTION
#Transfers a user's content to another account.
#If a user in the delete list is an admin, they will get passed on.
#This will first check to see if the user is part of any groups and transfer any group content to the dump account,
#updating these group items to public. Then it will remove the user from any groups.
#Next it look through the user's root folder and move those items
#then through each of the user's folders moving those items
#Then it will delete the user's empty folders
#Finally, it will revoke all licenses and priveleges and delete the user account.
#If a user can't be deleted for some reason it will print out the username

from arcgis.gis import #GIS https://developers.arcgis.com/python/guide/install-and-set-up/
from arcgis.gis import ContentManager
import pandas as pd
import os

os.chdir('C:\\Users\\phwh9568\\AGOLpy')

ucb_ago = GIS("https://ucboulder.maps.arcgis.com", "philip.white_ucboulder", "#####")

cm = ContentManager(ucb_ago)

df = pd.read_csv('deleteList_2020_06_09.csv')
deleteList = df['userName'].tolist()

for userName in deleteList:
    user = ucb_ago.users.get(userName)
    if user.role == 'org_admin':
        pass
    else:
        cm.create_folder(folder = userName, owner = 'sitelic')


        groups = user.groups
        groupItems = []

        for group in groups:
            groupContent = group.content()
            for item in groupContent:
                if item['owner'] == user.username:
                    groupItems.append(item)
            if group.owner == user.username:
                group.reassign_to('sitelic')
            group.remove_users([user.username])

        for item in groupItems:
            try:
                item.reassign_to('sitelic', target_folder = userName)
                item.share(everyone=True)
            except:
                pass

        userContent = user.items()
        userFolders = user.folders


        for item in userContent:
            try:
                item.reassign_to('sitelic', target_folder = userName)
            except:
                pass

        for folder in userFolders:
            folderName = (folder['title'])
            folderItems = user.items(folderName)
            for item in folderItems:
                try:
                    item.reassign_to('sitelic', target_folder = userName)
                except:
                    pass
            cm.delete_folder(folder=folderName, owner = user.username)

        pro_license.revoke(username=userName, entitlements='*')
        community_license.revoke(username=userName, entitlements = '*')
        business_license.revoke(username=userName, entitlements = '*')

        try:
            user.delete()
        except:
            print(userName)
            pass
