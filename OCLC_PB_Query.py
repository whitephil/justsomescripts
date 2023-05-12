import time
import os
import csv
import json
import requests

ti = time.time()

os.chdir(r'C:\Users\phwh9568\WorldCat_Locations\DHT_SCUBA')

url = 'http://www.worldcat.org/webservices/catalog/content/libraries/'

qParams = '&location=80309&maximumLibraries=500&wskey=[redacted api key]&format=json'

CUdata = open(r'scuba_test2.txt') #this is my not so smartly named input file, formatted from original to be pipe delimited

inst_list = ['COD', 'AZU', 'NYPIC','FNE', 'JPG', 'VZZ']

# open up output data that will be written on the fly
with open('scuba_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # add columns in first row
    writer.writerow(['oclcNum','ISBN','TITLE','COLLECTION','RECORD#','COD', 'AZU', 'NYPIC', 'FNE', 'JPG', 'VZZ','Total_Libs','Query'])
    
    # iterate over each item building query out of it's oclc number:
    for line in CUdata.readlines(): # can tweak using indexing here to break up into shorter running chunks, if breaking up, change mode to append 'a'       
        
        cols, rec = line.split('|')[0:-1], line.split('|')[-1].strip('\n') # get the columns we need from original data for output data
        cols.extend([rec])
        blob = requests.get(url+cols[0]+'?'+qParams) # send the query to worldcat
        
        # this chunk goes in and gets all the results back, and manages pagination (only 100 results per page, so if the total is >100, repeats until no results return)
        try:
            data = json.loads(blob.text)
            q = url+cols[0]+'?'+qParams
            libraries = data['library']
            
            total_libraries = len(libraries)
            
            if len(libraries) > 99:
                
                for page in range(101, 100001, 100): # loop over pages containing results 101 and onward, up to 100000 results
                    
                    blob = requests.get(url+cols[0]+'?'+'startLibrary='+str(page)+qParams) # subsequent query for additional pages
                    
                    try:
                        data = json.loads(blob.text)
                    
                        if 'diagnostic' in data['library'][0]:    #if no results, presume we've reached the end and move on
                            break

                        else: # get all pages of results onto one json blob
                            data = json.loads(blob.text) 
                            moreLibs = data['library']
                            total_libraries+=len(moreLibs)
                            [libraries.append(lib) for lib in moreLibs]
                            q = url+cols[0]+'?'+'startLibrary='+str(page)+qParams
                        
                    except:
                        q = url+cols[0]+'?'+'startLibrary='+str(page)+qParams   
            
            # for each query, check if our institutions are there, then create a boolean yes/no list for each
            inst_present = [inst for inst in inst_list if inst in [code['oclcSymbol'] for code in libraries]] #put loops into this double pack of list comprehension for speed
            inst_bool = ['Yes' if inst in inst_present else 'No' for inst in inst_list] #for loop packed into list comprehension for speed
            
        except: #this exception is when the json response is broken aka bad data back from oclc
            inst_bool = ['error','error','error','error','error','error']
            q = url+cols[0]+'?'+qParams
        
        # prep the boolean list for writing to the output csv, adding total libraries, and query url, then writing it
        inst_bool.extend([total_libraries])
        inst_bool.extend([q])
        cols.extend(inst_bool)
        writer.writerow(cols)
        
CUdata.close()

print(time.time() - ti)