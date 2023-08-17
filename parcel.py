# %% PROTOTYPING VARIOUS STUFF FOR PARCEL PROJECT THIS IS HUGE MESS
import geopandas as gpd
import pandas as pd
import os
from glob import glob
import time
import math
import random
import parcelfunks
import csv
# %%
mhomesPath = r'C:\Users\phwh9568\Data\ParcelAtlas\Mobile_Home_Parks\MHPgeocoded.shp'
parcelsPaths = glob(r'C:\Users\phwh9568\Data\ParcelAtlas\CO_2022\Counties\*')
blocksPath = r'C:\Users\phwh9568\Data\Census2020\tl_2020_08_all\tl_2020_08_tabblock10.shp'
externalDrive = r'D:/'

# %% splitting mobile homes data to counties

stateFips = pd.read_csv(r'C:\Users\phwh9568\Data\ParcelAtlas\stateFips.csv', dtype={'STATEFP':str})
stateFipsList = stateFips['STATEFP'].tolist()
pInventory = pd.read_csv(os.path.join(externalDrive,'parcelInventory.csv'), dtype={'STATE':str,'COUNTY':str})

# perhaps set up for loop first over stateFipsList here to form all paths? Or maybe run one state at a time.
# Colorado:    
CO_path = r'C:\Users\phwh9568\Data\ParcelAtlas\CO_2022\Counties'
CO_pInventory = pInventory.loc[pInventory['STATE']=='08']
CO_pInventory_True = CO_pInventory.loc[CO_pInventory['DATA_PRESENT']==True]
CO_pInventory_False = CO_pInventory.loc[CO_pInventory['DATA_PRESENT']==False]
CO_pInventory_False.to_csv(os.path.join(CO_path,'missingParcelData.csv'))
fipsList = CO_pInventory_True['COUNTY'].tolist()   
parcelsPaths = [os.path.join(CO_path,fips) for fips in fipsList]


#%%
mobileHomes = gpd.read_file(mhomesPath)
#%%
countyFips = pd.read_csv(r'C:\Users\phwh9568\Data\ParcelAtlas\fips-by-state.csv', dtype={'fips':str}, encoding='iso-8859-1')

#%%
countyFipsList = countyFips['fips'].tolist()
#%%
stateFips = pd.read_csv(r'C:\Users\phwh9568\Data\ParcelAtlas\stateFips.csv', dtype={'STATEFP':str})
stateFipsList = stateFips['STATEFP'].tolist()

#%% troubleshooting final table merge

stateFinalDF = pd.DataFrame()
for path in parcelsPaths:
    if os.path.exists(os.path.join(path,'MHP_'+path.split('\\')[-1]+'_final.csv')):
        countyDF = pd.read_csv(os.path.join(path,'MHP_'+path.split('\\')[-1]+'_final.csv'), dtype={'STATEFP10':str,'COUNTYFP10':str,'TRACTCE10':str,'BLOCKCE10':str,'GEOID10':str,'MTFCC10':str,'UACE10':str,'GEOID10':str,'GEOID10':str, })
        stateFinalDF = pd.concat([stateFinalDF,countyDF])
stateFinalDF.to_csv(r'c:/users/phwh9568/data/parcelatlas/CO_2022/Colorado.csv')

#%% fixing column names in final files

boco = pd.read_csv(r'c:/users/phwh9568/data/parcelatlas/CO_2022/counties/08013/MHP_08013_final.csv')

#%%
renames_x = boco.filter(regex='_x$').columns
renames = [x.split('_x')[0] for x in renames_x]
renames = dict(zip(renames_x,renames))

boco2 = boco.rename(renames,axis='columns')
boco2.drop(boco2.filter(regex='Unnamed*').columns,axis=1, inplace=True)

print(boco2.columns)

#%% SPLITTING MHPS TO INDIVIDUAL STATES
for fips in stateFipsList:
    if os.path.exists(os.path.join(externalDrive,'State_'+fips)):
        print('yes')
        stateMHPs = mobileHomes.loc[mobileHomes['USER_COU_1'].str.startswith(fips)]
        if len(stateMHPs) > 0:
            stateMHPs.to_file(os.path.join(externalDrive,'State_'+fips, fips+'_MHPs.gpkg'),driver='GPKG',layer=fips+'_MHPs')

#%% DEBUGGING FINAL CONCAT

countyFinal = pd.read_csv(r'C:\Users\phwh9568\Data\ParcelAtlas\CO_2022\Counties\08013\MHP_08013_final.csv')




#%% trouble shooting column renames

columns = ['USER_MHPID', 'USER_NAME','USER_ADDRE', 'USER_CITY', 'USER_STATE', 'USER_ZIP', 'USER_STATU', 'USER_COU_1','USER_LATIT', 'USER_LONGI','X','Y','geometry']
renames = ['MHPID', 'MH_NAME','MH_ADDRESS', 'MH_CITY', 'MH_STATE', 'MH_ZIP', 'MH_STATUS','MH_COUNTY_FIPS','MH_LATITUDE', 'MH_LONGITUDE','MH_Geocoded_X','MH_Geocoded_Y']
drops = [c for c in mobileHomes.columns if c not in columns] 
renames = dict(zip(columns,renames))

#%%


mobileHomes.drop(drops,axis=1, inplace=True)
mobileHomes.rename(renames, axis='columns',inplace=True)

#%% figuring out if county parcel data exists (THIS CAN BE MODIFIED TO FORM PARCEL PATHS)

with open(os.path.join(externalDrive,'parcelInventory.csv'),'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['STATE','COUNTY','DATA_PRESENT'])
    for sfips in stateFipsList:
        st_co_fips = countyFips.loc[countyFips['fips'].str.startswith(sfips)]
        countyfipsList = st_co_fips['fips'].tolist()
        for cfip in countyfipsList:
            if os.path.exists(os.path.join(externalDrive,'State_'+sfips, cfip)) :
                writer.writerow([sfips,cfip,'True'])
            else:
                writer.writerow([sfips,cfip,'False'])
            
#%%

pInventory = pd.read_csv(os.path.join(externalDrive,'parcelInventory.csv'))

#%%

missingCounties = pInventory.loc[pInventory['DATA_PRESENT']==False]
missingCountiesList = missingCounties

#%%
with open(os.path.join(externalDrive,'missingCounties.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for fips in stateFips:
        #st_co_fips = countyFips.loc[countyFips['fips'].str.startswith(fips)]
        #countyFipsList = st_co_fips['fips'].tolist()
        stateMHPs = mobileHomes.loc[mobileHomes['USER_COU_1'].str.startswith(fips)]
        stateMHPs.to_file(os.path.join(externalDrive,'State_'+fips, fips+'_MHPs.gpkg'),driver='GPKG',layer=fips+'_MHPs')



#%%
comobileHomes = mobileHomes.loc[mobileHomes['USER_COU_1'].str.startswith('08')]

#%%
comobileHomes.to_file(os.path.join(r'C:\Users\phwh9568\Data\ParcelAtlas\CO_2022','StateMHPs.gpkg'),driver='GPKG', layer='mhps')


# %%

mobileHomes = parcelfunks.mhomes_prepper(mhomesPath)

#%%

comobileHomes = mobileHomes.loc[mobileHomes['MH_COUNTY_FIPS'].str.startswith('08')]

#mhomes.to_crs(crs='EPSG:4269', inplace=True)
# %%
parcel = gpd.read_file(os.path.join(parcelsPaths[0],'parcels.shp'))
parcel.drop_duplicates(subset=['APN'], inplace=True)
columns = ['APN', 'APN2', 'geometry']
drops = [c for c in parcel.columns if c not in columns]
parcel.drop(drops, axis=1)
if parcel.crs != mobileHomes.crs:
    parcel.to_crs(mobileHomes.crs, inplace=True)
phomes = gpd.sjoin(parcel,mobileHomes)

# %% read in blocks

blocks = gpd.read_file(blocksPath)

#%%
blocksAlbers = blocks.to_crs(crs='ESRI:102003')
#%%
phomesAlbers = phomes.to_crs(blocksAlbers.crs)

#%%
blocksAlbers['blockArea_m'] = blocksAlbers['geometry'].area

#%%

# %% union

union = blocksAlbers.overlay(phomesAlbers, how='intersection')
union['unionArea_m'] = union['geometry'].area
 
#%%

union['blockParcel_ratio'] = (union['unionArea_m']/union['blockArea_m']) *100


#%% splitting mobile homes into county files
OGmhps = pd.read_csv(r'C:\Users\phwh9568\Data\ParcelAtlas\Mobile_Home_Parks\MobileHomeParks.csv', dtype={'COUNTYFIPS':str})

#%%

COmhps = OGmhps.loc[OGmhps['COUNTYFIPS'].str.startswith('08')]

#%%
COmhps.to_csv(r'c:/users/phwh9568/data/parcelatlas/COmhps.csv')

#%% 

for path in parcelsPaths:
    fips = path.split('\\')[-1]
    countyDF = COmhps.loc[COmhps['COUNTYFIPS']==fips].copy()
    columns = ['MHPID','NAME','ADDRESS', 'CITY', 'STATE', 'ZIP', 'STATUS', 'COUNTYFIPS','LATITUDE', 'LONGITUDE']
    renames = ['MHPID','MH_NAME','MH_ADDRESS', 'MH_CITY', 'MH_STATE', 'MH_ZIP', 'MH_STATUS','MH_COUNTY_FIPS','MH_LATITUDE', 'MH_LONGITUDE']
    drops = [c for c in countyDF.columns if c not in columns] 
    renames = dict(zip(columns,renames))
    countyDF.drop(drops,axis=1, inplace=True)
    countyDF.rename(renames, axis='columns',inplace=True)
    countyDF.to_csv(os.path.join(path,'MHP_'+str(fips)+'.csv'))

#%% merging union tables back with mhp table:

mhp0 = pd.read_csv(os.path.join(parcelsPaths[0],'MHP_08001.csv'), dtype={'MH_COUNTY_FIPS':str, 'MHPID':str})

union0 = pd.read_csv(os.path.join(parcelsPaths[0],'union_csv.csv'), dtype={'GEOID10':str,'STATEFP10':str, 'COUNTYFP10':str, 'TRACTCE10':str,'BLOCKCE10':str, 'MHPID':str})

#%% MERGE

mhp_union_merge = mhp0.merge(union0, on='MHPID', how = 'outer')


#%% work out how to keep unmatched



#%%
mhp_union_merge.to_csv(r'c:/users/phwh9568/data/parcelatlas/testMerge.csv')


#%%concating all county finals to one state final:

stateFinalDF = pd.DataFrame()
for path in parcelsPaths:
    if os.path.exists(os.path.join(path,'MHP_'+path.split('\\')[-1]+'_final.csv')):
        countyDF = pd.read_csv(os.path.join(path,'MHP_'+path.split('\\')[-1]+'_final.csv'))
        stateFinalDF = pd.concat([stateFinalDF,countyDF])

#%%

stateFinalDF.to_csv(r'c:/users/phwh9568/data/parcelatlas/testFINAL.csv')

#%%
union.to_file(r'c:/users/phwh9568/data/parcelatlas/testUnion.shp')

# %%
parcelsPaths[0]

# %%

dest = gpd.GeoDataFrame(crs='EPSG:4269')

# %%

for path in parcelsPaths[0]:
    parcel = gpd.read_file(os.path.join(path,'parcels.shp'))
    if parcel.crs != dest.crs:
        parcel.to_crs(dest.crs, inplace=True)
    #print(parcel.crs)
    phomes = gpd.sjoin(parcel,mhomes)
    dest = pd.concat([dest,phomes])

# %%

dest.to_file('parceltest.shp')

# %%
p0 = gpd.read_file(os.path.join(parcelsPaths[0],'parcels.shp'))

# %% 
phomes = gpd.sjoin(p0,mhomes)
# %%
phomes.to_file('parceltest.shp')

# %% Multiprocessing stuff

# first make a function:

def parcelMHPJoin(pFilePath):
    parcel = gpd.read_file(os.path.join(pFilePath,'parcels.shp'))
    if parcel.crs != mhomes.crs:
        parcel.to_crs(mhomes.crs, inplace=True)
    phomes = gpd.sjoin(parcel,mhomes)
    if len(phomes) > 0:
        phomes.to_file(os.path.join(pFilePath,'MP_MH_parcles.shp'))

# %%

parcelMHPJoin(parcelsPaths[0],'parcels.shp',mhomes)
# %%

with Pool() as pool:
    pool.map(parcelMHPJoin,parcelsPaths)

# %%

with Pool() as pool:
    pool.map(parcelMHPJoin,parcelsPaths)
# %%

for p in parcelsPaths:
    parcelMHPJoin(p)

# %%



# %%

def piFunk(num):
    return(num * math.pi)
# %%

testList = []
# %%
for x in range(1,100001):
    testList.append(random.randint(0,1001))
# %%

ti = time.time()

outList = []
for item in testList:
    outList.append(piFunk(item))

print(time.time() - ti)
# %%

ti = time.time()
with Pool() as pool:
    thing = pool.map(piFunk,testList)

print(time.time()-ti)
# %%
