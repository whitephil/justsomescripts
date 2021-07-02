import pandas as pd
import os

os.chdir('C:/Users/phwh9568/CUPubs_mailprep') #set the directory to your folder with the pub data

# fill in these variables each year with new file names and year. Each file needs to be in same directory
year = '2020' #be sure to leave the quotes here
pub_file_name = 'Publications_UserObjectPairs_From20200101_To20201231_20210702.csv'
do_not_file_name = 'DoNotContactList2020.csv'

# Provide a name for the output csv (no extension)
output_name = 'CUPubs2020_output5'

# read in the input file and do not contact file. If there is an encoding error, replace 'utf-8' with 'iso-8859-1'
df = pd.read_csv(pub_file_name, encoding = 'utf-8', low_memory = False)
dnc = pd.read_csv(do_not_file_name)

# rename the publication date field to pubDate
df.rename(columns={'Publication date OR Publication date or Presentation Date OR Presentation date OR Presented date OR Date awarded OR Date': 'pubDate'}, inplace=True)

# fill empty column with blanks to avoid nan values later
df.fillna('', inplace=True)

# Pre-filters:
# Drop articles published by AMS
df = df.loc[(df['Publisher'] != 'American Meteorological Society') & (df['Publisher'] != 'AMER METEOROLOGICAL SOC')]
# drop anything that is not a journal article or conference proceeding
df = df.loc[(df['Publication type'] == 'Journal article') | (df['Publication type'] == 'Conference Proceeding')]
# drop anything already indexed by DOAJ
df = df.loc[(df['Indexed in DOAJ'] != 'Yes') & (df['Indexed in DOAJ'] != '')]
# drop articles not published in the year specified above (articles with blank pubDate field will remain)
df = df.loc[(df['pubDate']=='') | (df['pubDate'].str.match(fr'\b{year}\b')==True) | (df['pubDate'].str.endswith(fr'/{year[2:]}')==True)]
# drop if reporting data is blank
df = df.loc[df['Reporting date 1'] != '']

# read do not contact names into a list
dnc_list = dnc['Elements_Name'].to_list()
# iterate over do not contact list names and drop them
for name in dnc_list:
    df = df.loc[df['Name']!=name]

# drop all unnecessary columns
col_list = ['Name', 'Authors', 'Email', 'Primary group', 'Title OR Chapter Title', 'Canonical journal title', 'Volume', 'Issue', 'DOI', 'Primary group', 'Email']
df = df[df.columns.intersection(col_list)]

# function that finds publication metadata and concatenates them into a citation
def cite(row):
    if row['Authors'] == '':
        auths = ''
        date = ''
    else:
        auths = row['Authors']+'.'
        date = ' ('+year+').'

    if row['Title OR Chapter Title'] == '':
        title = ''
    else:
        title = ' '+row['Title OR Chapter Title']+'.'

    if row['Canonical journal title'] == '':
        pub = ''
    else:
        pub = ' '+row['Canonical journal title']+'.'

    if row['Volume'] == '':
        vol = ''
    else:
        vol = ' '+row['Volume']+'.'

    if row['Issue'] == '':
        iss = ''
    else:
        iss = ' '+row['Issue']+'.'

    if row['DOI'] == '':
        doi = ''
    else:
        doi = ' '+row['DOI']+'.'

    citation = auths + date + title + pub + vol + iss + doi

    return citation

# function that splits full names into individual first, middle, last name fields
def names(row):

    if len(row) == 0:
        nl = ''
        nf = ''
        nm = ''

    else:
        n = row['Name'].title()

        nl = n.split(', ')[0]

        if len(n.split(', ')) > 1:

            nfm = n.split(', ')[1]

            if len(nfm.split(' ')) > 1:
                nf = nfm.split(' ')[0]
                nm = nfm.split(' ')[1]
            else:
                nf = nfm
                nm = ''
        else:
            nf =''
            nm =''

    return nl,nf,nm

# Apply the functions across rows in the dataframe
df['Pub'] = df.apply(lambda row: cite(row), axis = 1)
df['Last Name'] = df.apply(lambda row: names(row)[0], axis = 1)
df['First Name'] = df.apply(lambda row: names(row)[1], axis = 1)
df['Middle Name'] = df.apply(lambda row: names(row)[2], axis = 1)

#Now create new dataframe of just authors and citations
col_list2 = ['Name', 'Pub']
df2 = df[col_list2].copy() #create the new daframe named df2

#creating the groups and adding a new 'group' column
df2 = df2.assign(group = df.groupby('Name').cumcount())

#pivot function with names in the index position (vertical) and groups become columns (horizontal)
citations = df2.pivot(index = 'Name', columns = 'group')

#pivot creates multi-index dataframe. This will reset it to a single index (or in other words takes the 2 header row and makes 1 header row)
citations.columns =  [col[0] + '_' + str(col[1]+1) for col in citations.columns.values]

#the columns we need for our new dataframe
col_list3 = ['Name', 'Last Name', 'First Name', 'Middle Name', 'Primary group', 'Email']
contacts = df[col_list3] #create new contacts dataframe that consists of just names, departments, and emails from original df

# deduplicate, reindex, drop unneeded 'index' column
contacts = contacts.drop_duplicates(subset = ['Name'], keep = 'first')
contacts.reset_index(inplace=True)
contacts = contacts.drop(columns=['index'])

#merge the citations back to the names & contact info
finaldf = contacts.merge(citations, how= 'left', left_on = 'Name', right_on = 'Name')
finaldf.to_csv(output_name+'.csv', encoding='utf-8') #view the results
