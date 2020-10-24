import pandas as pd
import csv

df = pd.read_csv('C:\\Users\\phwh9568\\camp\\Master-Table-1.csv', encoding = 'utf-8')
pidList = list(df.PersonID.unique())

with open('C:\\Users\\phwh9568\\camp\\camper_history.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Person ID', 'Last Name', 'First Name', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'])
    for pid in pidList:
        camper = df.loc[df.PersonID==pid].copy()

        a2011 = ''
        a2012 = ''
        a2013 = ''
        a2014 = ''
        a2015 = ''
        a2016 = ''
        a2017 = ''
        a2018 = ''
        a2019 = ''

        y2011 = list(camper['2011'])
        y2012 = list(camper['2012'])
        y2013 = list(camper['2013'])
        y2014 = list(camper['2014'])
        y2015 = list(camper['2015'])
        y2016 = list(camper['2016'])
        y2017 = list(camper['2017'])
        y2018 = list(camper['2018'])
        y2019 = list(camper['2019'])

        if 2011.0 in y2011:
            a2011 = '2011'

        if 2012.0 in y2012:
            a2012 = '2012'

        if 2013.0 in y2013:
            a2013 = '2013'

        if 2014.0 in y2014:
            a2014 = '2014'

        if 2015.0 in y2015:
            a2015 = '2015'

        if 2016.0 in y2016:
            a2016 = '2016'

        if 2017.0 in y2017:
            a2017 = '2017'

        if 2018.0 in y2018:
            a2018 = '2018'

        if 2019.0 in y2019:
            a2019 = '2019'

        firstName = camper['First Name'].iloc[0]
        lastName = camper['Last Name'].iloc[0]

        writer.writerow([pid, lastName, firstName, a2011, a2012, a2013, a2014, a2015, a2016, a2017, a2018, a2019])
