'''
converts raw faculty publication data from elements
into format ready for mailmerge
'''

import os
import pandas as pd

os.chdir('C:/Users/phwh9568/CUPubs_mailprep') #set the directory to your folder with the pub data

# fill in these variables each year with new file names and year.
# Each file needs to be in same directory
year = '2020' #be sure to leave the quotes here
pub_file_name = 'Publications_UserObjectPairs_From20200101_To20201231_20210702.csv'
do_not_file_name = 'DoNotContactList2020.csv'

# Provide a name for the output csv (no extension)
output_name = 'CUPubs2020_demo'

# read in the input file and do not contact file. If there is an encoding error, replace 'utf-8' with 'iso-8859-1'
pubs_data_df = pd.read_csv(pub_file_name, encoding = 'utf-8', low_memory = False)
dnc = pd.read_csv(do_not_file_name)

# rename the publication date field to pubDate
pubs_data_df.rename(columns={'Publication date OR Publication date or Presentation Date OR Presentation date OR Presented date OR Date awarded OR Date': 'pubDate'}, inplace=True)

# fill empty column with blanks to avoid nan values later
pubs_data_df.fillna('', inplace=True)

# Pre-filters:
# Drop articles published by AMS
pubs_data_df = pubs_data_df.loc[(pubs_data_df['Publisher'] != 'American Meteorological Society') & (pubs_data_df['Publisher'] != 'AMER METEOROLOGICAL SOC')]
# drop anything that is not a journal article or conference proceeding
pubs_data_df = pubs_data_df.loc[(pubs_data_df['Publication type'] == 'Journal article') | (pubs_data_df['Publication type'] == 'Conference Proceeding')]
# drop anything already indexed by DOAJ
pubs_data_df = pubs_data_df.loc[(pubs_data_df['Indexed in DOAJ'] != 'Yes') & (pubs_data_df['Indexed in DOAJ'] != '')]
# drop articles not published in the year specified above (articles with blank pubDate field will remain)
pubs_data_df = pubs_data_df.loc[(pubs_data_df['pubDate']=='') | (pubs_data_df['pubDate'].str.match(fr'\b{year}\b')==True) | (pubs_data_df['pubDate'].str.endswith(fr'/{year[2:]}')==True)]
# drop if reporting data is blank
pubs_data_df = pubs_data_df.loc[pubs_data_df['Reporting date 1'] != '']

# read do not contact names into a list
dnc_list = dnc['Elements_Name'].to_list()
# iterate over do not contact list names and drop them
for name in dnc_list:
    pubs_data_df = pubs_data_df.loc[pubs_data_df['Name']!=name]

# drop all unnecessary columns
col_list = ['Name', 'Authors', 'Email', 'Primary group', 'Title OR Chapter Title', 'Canonical journal title', 'Volume', 'Issue', 'DOI', 'Primary group', 'Email']
pubs_data_df = pubs_data_df[pubs_data_df.columns.intersection(col_list)]

# function that finds publication metadata and concatenates them into a citation
def cite(row):
    '''
    Parameters
    ----------
    row : a row in the pubs_data_df (elements input data post-filtering).


    Returns
    -------
    citation : a concatenation of various article metadata
        elements to produce a full citation

    '''

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

    '''
    Splits single name field into first, middle, and last names separately and returns each.
    Meant to be ran from a dataframe, and adds new data to the dataframe

    Parameters
    ----------
    row : a row in the pubs_data_df (elements input data post-filtering).

    Returns
    -------
    name_last,name_first,name_middle : first, middle, and last names separately.
    '''

    if len(row) == 0:
        name_last = ''
        name_first = ''
        name_middle = ''

    else:
        name_full = row['Name'].title()

        name_last = name_full.split(', ')[0]

        if len(name_full.split(', ')) > 1:

            name_first_middle = name_full.split(', ')[1]

            if len(name_first_middle.split(' ')) > 1:
                name_first = name_first_middle.split(' ')[0]
                name_middle = name_first_middle.split(' ')[1]
            else:
                name_first = name_first_middle
                name_middle = ''
        else:
            name_first =''
            name_middle =''

    return name_last,name_first,name_middle

# Apply the functions across rows in the dataframe
pubs_data_df['Pub'] = pubs_data_df.apply(lambda row: cite(row), axis = 1)
pubs_data_df['Last Name'] = pubs_data_df.apply(lambda row: names(row)[0], axis = 1)
pubs_data_df['First Name'] = pubs_data_df.apply(lambda row: names(row)[1], axis = 1)
pubs_data_df['Middle Name'] = pubs_data_df.apply(lambda row: names(row)[2], axis = 1)

#Now create new dataframe of just authors and citations
col_list2 = ['Name', 'Pub']
authors_citations_df = pubs_data_df[col_list2].copy() #create the new daframe named authors_citations_df

#creating the groups and adding a new 'group' column
authors_citations_df = authors_citations_df.assign(group = pubs_data_df.groupby('Name').cumcount())

#pivot function with names in the index position (vertical) and groups become columns (horizontal)
citations = authors_citations_df.pivot(index = 'Name', columns = 'group')

#pivot creates multi-index dataframe. This will reset it to a single index (or in other words takes the 2 header row and makes 1 header row)
citations.columns =  [col[0] + '_' + str(col[1]+1) for col in citations.columns.values]

#the columns we need for our new dataframe
col_list3 = ['Name', 'Last Name', 'First Name', 'Middle Name', 'Primary group', 'Email']
contacts = pubs_data_df[col_list3] #create new contacts dataframe that consists of just names, departments, and emails from original df

# deduplicate, reindex, drop unneeded 'index' column
contacts = contacts.drop_duplicates(subset = ['Name'], keep = 'first')
contacts.reset_index(inplace=True)
contacts = contacts.drop(columns=['index'])

#merge the citations back to the names & contact info
contacts_citations_df = contacts.merge(citations, how= 'left', left_on = 'Name', right_on = 'Name')
contacts_citations_df.to_csv(output_name+'.csv', encoding='utf-8') #view the results
