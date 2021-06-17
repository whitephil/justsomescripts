import pandas as pd

df = pd.read_csv('E:\\Users\\phwh9568\\CUPubs_mailprep\\CUPublications_2017FRPA.csv', encoding = 'iso-8859-1').astype(str)

col_list = ['Name', 'Authors', 'Email', 'Primary group', 'Title OR Chapter Title', 'Canonical journal title', 'Volume', 'Issue', 'DOI']

df = df[col_list]

df['Citation'] = df['Authors'] + '. (2017). ' + df['Title OR Chapter Title'] + '. ' + df['Canonical journal title'].fillna('') + '. ' + df['Volume'].fillna('') + ', ' + df['Issue'].fillna('') + '. ' + df['DOI'].fillna('')

col_list2 = ['Name', 'Citation']

df2 = df[col_list2]

col_list3 = ['Name', 'Primary group', 'Email']

df3 = df[col_list3]

df2 = df2.assign(group = df.groupby('Name').cumcount())

df2wide = df2.pivot(index = 'Name', columns = 'group')

df3dedup = df3.drop_duplicates(subset = ['Name'], keep = 'first')

df2wide.reset_index(inplace = True)

df3dedup.reset_index(inplace = True)

merged = df3dedup.merge(df2wide, how = 'left', left_on = 'Name', right_on = 'Name')

merged = merged.reset_index(level=[0,1])

merged['Last Name'], merged['First_MI'] = merged['Name'].str.split(',').str

merged['First MI title'] = merged['First_MI'].str.title()

merged['First Name'], merged['MI'], merged['OtherName'] = merged['First MI title'].str.split().str

merged = merged.drop(['First_MI', 'First MI title', 'index'], axis = 1)

col_list4 = ['Name', 'Last Name', 'First Name', 'MI', 'OtherName']

names = merged[col_list4]

merged = merged.drop(['Last Name', 'First Name', 'MI', 'OtherName'], axis=1)

finaldf = names.merge(merged, how = 'right', left_on = 'Name', right_on = 'Name')

finaldf = finaldf.drop(['level_0'], axis=1)

finaldf.to_csv('E:\\Users\\phwh9568\\CUPubs_mailprep\\CUPub_Pivot.csv')


#end
