#check and delete all unused packages 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #This will help to stop the tab pop up
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
import pandas as pd
from io import StringIO
from datetime import datetime,date

url="https://www.investorgain.com/report/live-ipo-gmp/331/"
options= Options()
options.add_argument('--headless') #Stops the pop up


driver =webdriver.Chrome(options)

driver.get(url)
wait = WebDriverWait(driver, 15)
try:
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    print("✅ Table detected!")
except:
    print("❌ No table found after 15s")

time.sleep(3) #sleep for 3 unit of time for js to load

#wraping in stringio to supress warnings
dfs= pd.read_html(StringIO(driver.page_source)) #Returns a list of dataframes

driver.quit()

main_dfs=dfs[0] #first item of the list

date_column='Close▲▼'
#Will use the above column to filter the data 
def modify_ipo_date(date_str):  
    '''Convert the date format from 31-Dec kind to the standard python date form'''
    """Parse '30-Dec' → datetime (handles NaN, None, non-strings)"""
    # ✅ FIX: Handle NaN/missing values FIRST
    current_year = date.today().year
    current_month = date.today().month
    current_date = date.today().day
    #Since we need to sort data based on dates, we fill it with past date which will get filtered
    
    if pd.isna(date_str) or date_str is None:
        return datetime(current_year-1,current_month,current_date)
    
    # ✅ FIX: Convert to string safely
    date_str = str(date_str).strip()
    if not date_str or date_str.lower() in ['nan', 'none','null']:
        return datetime(current_year-1,current_month,current_date)
    
    if '-' not in date_str:
        return datetime(current_year-1,current_month,current_date)

    

    close_date,month_str =date_str.split('-')

    #print(f"DEBUG: close_date='{close_date}', month_str='{month_str}'")  

    month_map ={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
                'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    month=month_map[month_str]
    if(current_month!=12):
        return  datetime(current_year,month,int(close_date)) #since date is string 
    elif(current_month==12 and month==1): # this means we move to next year
        return datetime(current_year+1,month,int(close_date))
    else:  #Was skipping the case where the month is dec , this was causing issue
        return datetime(current_year, month, int(close_date)) 
    

# print(main_dfs[date_column])
main_dfs[date_column]=main_dfs[date_column].apply(modify_ipo_date)
today=date.today()
#print(today)
# print("\n After changing \n")
# print(main_dfs[date_column])

upcoming_ipos=main_dfs[main_dfs[date_column].dt.date >= today].copy() #creating copy of data by filtering it


print(upcoming_ipos)