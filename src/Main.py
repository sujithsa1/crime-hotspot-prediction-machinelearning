import pandas as pd
import numpy as np
#Data visualization libraries:
import matplotlib.pyplot as plt 
import seaborn as sns
import cufflinks as cf
from ipywidgets import widgets
from ipywidgets import *
from IPython.display import display,clear_output
from plotly.offline import download_plotlyjs, init_notebook_mode,plot,iplot
cf.go_offline()

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
cag = pd.read_excel('data/Cases Reported under Crimes against Women During 2007-2021.xlsx')
ageGrpVict =  pd.read_csv('data/Age_groups_Incest_other_rape_victim.csv')
cag.head()
cag = cag[cag.columns.drop(list(cag.filter(regex='Unnamed')))]
cag.isnull().values.any()
sns.heatmap(cag.isnull().values)
plt.show()
cag = cag.dropna()
cag.isnull().values.any()
sns.heatmap(cag.isnull().values)
plt.show()
cag.head()
cag['Year'] = cag['Year'].apply(lambda x:int(x))
cag=cag.rename(columns = {'STATE':'State/UT'})
cag.columns
cag.to_csv('data/Cases Reported under Crimes against Women During 2007-2021',index=False)
#Load csv file:
cag = pd.read_csv('data/Cases Reported under Crimes against Women During 2007-2021')
print(ageGrpVict['STATE/UT'].unique())
ageGrpVict = ageGrpVict[ageGrpVict['STATE/UT']!='Total (State)']
ageGrpVict = ageGrpVict[ageGrpVict['STATE/UT']!='Total (UTs)']
ageGrpVict = ageGrpVict[ageGrpVict['STATE/UT']!='Total (All-India)']
print(ageGrpVict.columns)
ageGrpVict = ageGrpVict[ageGrpVict['Crime Head'] != 'Total']
ageGrpVict[ageGrpVict['Total Victims'] != ageGrpVict['No. Of Cases Reported']].head()
ageGrpVict['Unreported Cases'] = ageGrpVict['Total Victims'] - ageGrpVict['No. Of Cases Reported']
ageGrpVict[ageGrpVict['Unreported Cases'] > 0].head()
ageGrpVict.to_csv('data/Age_groups_Incest_other_rape_victim',index=False)
ageGrpVict = pd.read_csv('data/Age_groups_Incest_other_rape_victim')
crimeDictS = {'Rape':sum, 'Kidnapping & Abduction':sum,'Dowry Deaths':sum,'Assault on women with intent to outrage her modesty ':sum,'Insult to modesty of women':sum,'Cruelty by Husband or his Relatives':sum,'Importation of Girls from foreign country':sum,'Immoral Traffic (P) Act':sum,'Dowry Prohibition Act':sum,'Indecent Representation of Women(P) Act':sum,'Commission of Sati Prevention Act':sum}
#Without aggr list:
crimeDict = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths','Assault on women with intent to outrage her modesty ','Insult to modesty of women', 'Cruelty by Husband or his Relatives','Importation of Girls from foreign country', 'Immoral Traffic (P) Act','Dowry Prohibition Act', 'Indecent Representation of Women(P) Act','Commission of Sati Prevention Act']
crimes = cag.groupby(["State/UT"], as_index=False).agg(crimeDictS)
crimes['Total'] = crimes[crimeDict].sum(axis=1)
crimes.head()
plt.figure(figsize=(20,10))
plt.title('Statewise total crime against women in India')
order = crimes.groupby(["State/UT"])['Total'].aggregate(np.median).reset_index().sort_values('Total')
ax=sns.barplot(y='State/UT', x='Total',data=crimes,order=order['State/UT'],palette='Blues')
ax.set(xlabel = 'Total number of Crime against women')
totals = []
for i in ax.patches:
    totals.append(i.get_width())
total = sum(totals)
for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.3, i.get_y()+.19,str(round((i.get_width()/total)*100, 2))+'%', fontsize=10,color='black')
ax.invert_yaxis()
for state in ax.get_yticklabels():state.set_rotation(0)
plt.show()

print('Observations: So as we know the most of the crimes occured in the following top 5 states:')
print('-----------------------------------------------------------------------------------------')
print('[States, Total no. of crimes ]')
x = crimes.sort_values(by='Total', ascending=False).head(5)
x = x[['State/UT','Total']].values
for i in range(0,5):
    print(str(i+1)+'.'+str(x[i]))

print('Observations: Below 5 states for having lesser number of crimes:')
print('---------------------------------------------------------------')
print('[States, Total no. of crimes ]')
x = crimes.sort_values(by='Total').head(5)
x = x[['State/UT','Total']].values
for i in range(0,len(x)):
     print(str(i+1)+'.'+str(x[i]))

crimesYear = cag.groupby(["State/UT","Year"], as_index=False).agg(crimeDictS)
#Making alnl the crime heads as a single categorical column:
crimesYear_1 = crimesYear.melt(id_vars = ["State/UT", "Year"], value_vars = crimeDict, var_name = 'Crime Head',value_name='no. of crimes')
crimesYear_1.head()

plt.figure(figsize=(20,15))
plt.title('Year wise Crime Head')
sns.set(style="ticks",rc={"lines.linewidth": 0.7})
sns.pointplot(data=crimesYear_1, x = 'Year',  y = 'no. of crimes', hue = 'Crime Head',palette='deep',markers=['v','h','X','P','D','1','2','s','x','o','>'],scale = 3)
plt.show()

states = ["Andhra Pradesh","Uttar Pradesh","West Bengal","Rajasthan","Madhya Pradesh"]
select_variable = widgets.Dropdown(
    options=states,
    value=states[0],
    description='Select State:',
    disabled=False,
    button_style=''
)
def get_and_plot(b):
    clear_output()
    display(select_variable)
    #print(select_variable.value)
    state = select_variable.value
    apYear = cag.groupby(["State/UT","Year"], as_index=False).agg(crimeDictS)
     #Making all the crime heads as a single categorical column:
    apYear_1 = apYear.melt(id_vars = ["State/UT", "Year"], value_vars = crimeDict, var_name ='Crime Head',value_name='no. of crimes') 
    plt.figure(figsize=(15,10))
    plt.title('Crimes against women in '+state)
    order = apYear_1.groupby(["Crime Head"])['no. of crimes'].aggregate(np.sum).reset_index().sort_values('no. of crimes')
    ax = sns.barplot(y='Crime Head', x=apYear_1[apYear_1['State/UT']==state]['no. of crimes'],data=apYear_1,order=order['Crime Head'],palette='viridis')
    # create a list to collect the plt.patches data
    totals = []
    # find the values and append to list
    for i in ax.patches:
         totals.append(i.get_width())
    # set individual bar lables using above list
    total = sum(totals)
    # set individual bar lables using above list
    for i in ax.patches:
    # get_width pulls left or right; get_y pushes up or down
        ax.text(i.get_width()+.3, i.get_y()+.33,str(round((i.get_width()/total)*100, 2))+'%', fontsize=15,color='black')
# invert for largest on top 
ax.invert_yaxis()
display(select_variable)
select_variable.observe(get_and_plot, names='value')
plt.show()
slice = cag[(cag['State/UT']=='Andhra Pradesh') | (cag['State/UT']=='Uttar Pradesh')| (cag['State/UT']=='West Bengal')| (cag['State/UT']=='Rajasthan')|(cag['State/UT']=='Madhya Pradesh')]
slice = slice[(slice['Year']==2019)|(slice['Year']==2020)|(slice['Year']==2013)]
plt.figure(figsize=(20,10))
ax=sns.barplot(y='State/UT', x='Total Crimes Against Women',hue='Year',data=slice,palette='viridis')
ax.set(xlabel = 'Total number of Crime against women')
# create a list to collect the plt.patches data
totals = []
# find the values and append to list
for i in ax.patches:totals.append(i.get_width())
# set individual bar lables using above list
total = sum(totals)
# set individual bar lables using above list
for i in ax.patches:
# get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.3, i.get_y()+.1, \
            str(round((i.get_width()/total)*100, 2))+'%', fontsize=15,
color='black')
# invert for largest on top 
ax.invert_yaxis()
for state in ax.get_yticklabels():state.set_rotation(0)

caw = pd.read_excel('data/caw.xlsx')

sliceCAW = caw[(caw['Year']==2019)|(caw['Year']==2020)]
#Removing 'Year' column and grouping statewise by aggregating the columns values as sum
crimeSlice = sliceCAW.groupby(["State/UT"], as_index=False).agg(crimeDictS)
#adding new column with sum of crimes for each state
crimeSlice['Total'] = crimeSlice[crimeDict].sum(axis=1)

plt.figure(figsize=(20,10))
ax=sns.barplot(y='State/UT', x='Total',data=sliceCAW,palette='deep')
ax.set(xlabel = 'Total number of Crime against women')
# create a list to collect the plt.patches data
totals = []
# find the values and append to list
for i in ax.patches:totals.append(i.get_width())
# set individual bar lables using above list
total = sum(totals)
# set individual bar lables using above list
for i in ax.patches:
# get_width pulls left or right; get_y pushes up or down
    ax.text(i.get_width()+.3, i.get_y()+.1, \
            str(round((i.get_width()/total)*100, 2))+'%', fontsize=15,
color='black')
# invert for largest on top 
ax.invert_yaxis()
for state in ax.get_yticklabels():state.set_rotation(0)
plt.show()

plt.figure(figsize=(10,6))
sns.heatmap(caw.corr(),annot=True)
plt.show()

unreported_victims_by_state = ageGrpVict.groupby('STATE/UT').sum()
unreported_victims_by_state.drop('YEAR', axis = 1, inplace = True)
plt.figure(figsize = (15, 6))
ct = unreported_victims_by_state[unreported_victims_by_state['Unreported Cases'] 
                                 > 0]['Unreported Cases'].sort_values(ascending = False)
print(ct)
#ax = ct.plot.bar()
#ax.set_xlabel('State/UT')
#ax.set_ylabel('Total Number of Unreported Rape Victims from 2007 to 2019')
#ax.set_title('Statewise total Unreported Rape Victims throughout 2007 to 2019')
#plt.show()

rape_victims_by_state = unreported_victims_by_state
rape_victims_by_state.sort_values(by = 'No. Of Cases Reported', ascending = False).head()

rape_victims_heatmap = rape_victims_by_state.drop(['No. Of Cases Reported', 
                                                   'Total Victims', 
                                                   'Unreported Cases'], axis = 1)
plt.subplots(figsize = (10, 10))
ax = sns.heatmap(rape_victims_heatmap, cmap="RdPu")
ax.set_xlabel('Age Group')
ax.set_ylabel('States/UT')
ax.set_title('Statewise Victims of Rape Cases based on Age Group')
plt.show()

plt.subplots(figsize = (15, 8))
ax = sns.barplot(y = rape_victims_by_state.index, x = rape_victims_by_state['No. Of Cases Reported'],palette='deep')
ax.set_ylabel('State/UT')
ax.set_xlabel('Total Number of Reported Rape Victims')
ax.set_title('Statewise total Reported Rape Victims throught the Years 2007 to 2013')
plt.show()

casedict = {
    'No. Of Cases Reported':sum,
    'Unreported Cases':sum
}
# adding back "Year" column to our data
rapeYear = ageGrpVict.groupby(["STATE/UT","YEAR"], as_index=False).agg(casedict)
# #Making all the crime heads as a single categorical column:
rapeYear_1 = rapeYear.melt(id_vars = ["STATE/UT", "YEAR"], value_vars = ['No. Of Cases Reported', 'Unreported Cases'],
                           var_name = 'Type',value_name='no. of rape cases')
rapeYear_1.head()

plt.figure(figsize=(15,8))
plt.title('Year wise no. of Rape Cases')
sns.set(style="ticks",rc={"lines.linewidth": 0.7})
sns.pointplot(data=rapeYear_1, x = 'YEAR',  y = 'no. of rape cases', hue = 'Type',palette='deep',markers=['v','h','X'],scale = 3)
plt.show()

victdictS = {'No. of Victims upto 10 years':sum, 'No. of Victims 10-14 years':sum,'No. of Victims 14-18 years':sum, 'No. of Victims 18-30 years':sum,'No. of Victims 30-50 years':sum, 'No. of Victims above 50 years':sum}
victlist = [ 'No. of Victims upto 10 years', 'No. of Victims 10-14 years','No. of Victims 14-18 years', 'No. of Victims 18-30 years','No. of Victims 30-50 years', 'No. of Victims above 50 years']
# adding back "Year" column to our data
victYear = ageGrpVict.groupby(["STATE/UT","YEAR"], as_index=False).agg(victdictS)
# #Making all the crime heads as a single categorical column:
victYear_1 = victYear.melt(id_vars = ["STATE/UT", "YEAR"], value_vars = victlist,
                           var_name = 'Victim Age groups',value_name='no. of Victims')
victYear_1.head()
#Number of each crimes dependent on year for each states altogether
plt.figure(figsize=(15,8))
plt.title('Year wise Crime Head')
sns.set(style="ticks",rc={"lines.linewidth": 0.7})
sns.pointplot(data=victYear_1, x = 'YEAR',  y = 'no. of Victims', hue = 'Victim Age groups',markers=['D','1','2','s','x','o'],palette='deep',scale = 2)

plt.show()
pop = pd.read_excel('Data/CensusPopulation2007to2021.xlsx')
pop.head()

sr = pd.read_excel('Data/SexRatio2007to2021.xlsx')

cag['SYID']=cag['State/UT']+(cag['Year'].apply(lambda x:str(x)))
cag.head()

sr['SYID'] = sr['State/UT']+(sr['Year'].apply(lambda x:str(x)))

cag.set_index('SYID').head()
sr.set_index('SYID').head()

new = pd.merge(cag,sr,how='inner',on='SYID')
new.drop(['State/UT_y', 'Year_y'],axis=1,inplace=True)

yearList = [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]
pop_1 = pop.melt(id_vars = ["State/UT"], value_vars = yearList, var_name = 'Year',value_name='Population(in K)')
pop_1.head(2)

pop_1['SYID'] = pop_1['State/UT']+(pop_1['Year'].apply(lambda x:str(x)))

pop_1.set_index('SYID').head(2)

pop_1.drop(['State/UT','Year'],inplace=True,axis=1)

pop_1.set_index('SYID',inplace=True)

new = pd.merge(new,pop_1,how='inner',on='SYID')
newCorr = new.drop([ 'Importation of Girls from foreign country','Immoral Traffic (P) Act', 'Dowry Prohibition Act','Indecent Representation of Women(P) Act','Commission of Sati Prevention Act'],axis=1)

l = newCorr.corr(method='kendall')

l = l.drop(['Year_x', 'Rape', 'Kidnapping & Abduction', 'Dowry Deaths',
       'Assault on women with intent to outrage her modesty ',
       'Insult to modesty of women', 'Cruelty by Husband or his Relatives',
       'Total Crimes Against Women'],axis=1)
l = l.drop('Year_x')

plt.figure(figsize=(5,5))
sns.heatmap(l,annot=True)
plt.show()

stateCluster  = crimes
stateCluster.head()
stateCluster.columns

fp = stateCluster.drop(['Total'],axis=1)

sns.clustermap(fp.set_index('State/UT'),cmap='RdPu')
plt.show()

df = pd.read_csv('data/crimeAgainstWomeninIndia.csv')
y1 = df['Year'].max()
y2 = y1-1
y3 = y2-1
y4 = y3-1
def pattern(a,b,c):
    if(a == 1):
            if(b == 1):
                if(c==1):return "Higher chances of an increase"
                else:return "Medium chances of an decrease"
            elif(b == 0):
                if(c == 1):return "Medium chances of an increase"      
                else:return "Lower chances of an increase"
    elif(a == 0):
            if(b == 0):
                if(c == 0):return "Lower chances of increase"
                else:return "Medium chances of increase"
            elif(b==1):
                if(c == 0):return "Medium chances of decrease"
                else:return "Higher chances of increase"
x = input('Enter the State/Ut:')
y = input('Enter the crime name:')
x1 = list(df[(df['State/UT']==x) & (df['Year']==y1)][y])
x2 = list(df[(df['State/UT']==x) & (df['Year']==y2)][y])
x3 = list(df[(df['State/UT']==x) & (df['Year']==y3)][y])
x4 = list(df[(df['State/UT']==x) & (df['Year']==y4)][y])
if((x=='Telangana') & (y1 == 2021)):
    s1=0
    s2=0
    if((x1[0] - x2[0]) > 0):
         s3 = 1
    else:
         s3 = 0
else:
    if((x3[0] - x4[0]) > 0):
        s1 = 1
    else:
        s1 = 0
    if((x2[0] - x3[0]) > 0):
         s2 = 1
    else:
         s2 = 0
    if((x1[0] - x2[0]) > 0):
         s3 = 1
    else:
         s3 = 0
    
res = pattern(s1,s2,s3)
print(x+' has '+res+' in '+y+' in the year '+str(y1+1)+' ,considering constant current policies.')

a = df[df['State/UT']==x]
plt.figure(figsize=(10,6))
sns.lineplot(x=a['Year'],y=a[y],data=a)
plt.show()
