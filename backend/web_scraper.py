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

urls=["https://www.investorgain.com/report/live-ipo-gmp/331/",
      "https://ipowatch.in/ipo-subscription-status-today/"] 


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

    

    close_date,month_str =date_str.split('-')[:2]
    month_str=month_str.split(' ')[0] # This line added since they modified the data , it should still work after they fix
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

def scrape_url(url, idx):
    options= Options()
    options.add_argument('--headless') #Stops the pop up
    options.add_argument('--no-sandbox')            
    options.add_argument('--disable-dev-shm-usage')  
    options.add_argument('--disable-gpu')          
    options.add_argument('--window-size=1920,1080') 
    driver =webdriver.Chrome(options)
    print(f"\n🔄 Driver {idx}: {url}")
    driver.get(url)
    
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        print("✅ Table detected!")
    except:
        print("❌ No table")
        driver.quit()
        return None
    
    time.sleep(3)#sleep for 3 unit of time for js to load
    dfs = pd.read_html(StringIO(driver.page_source))
    driver.quit()  # Clean quit per URL
    
    return dfs[0]

def merge_dataframes(gmp_df, subs_df):
    # print(gmp_df.columns)
    gmp_df['Merge_key'] = gmp_df['Name▲▼'].str.split().str[0].str.lower()
    subs_df['Merge_key'] = subs_df['IPO Name'].str.split().str[0].str.lower()

    merged=gmp_df.merge(subs_df,on='Merge_key',how='left') #adding a new column in both df and then using it to do join and then select req cols
    # print(merged.columns)
    return merged[['IPO Name', 'GMP▲▼', 'Price (₹)▲▼', 'Lot▲▼', 'Close▲▼',
                   'Type', 'QIB', 'NII / HNI', 'Retail']]

def collect_and_merge():
    date_column='Close▲▼'
    #Will use the above column to filter the data 
    upcoming_ipos=scrape_url(urls[0],0)
    upcoming_ipos[date_column]=upcoming_ipos[date_column].apply(modify_ipo_date)
    today=date.today()
        #print(today)
        # print("\n After changing \n")
        # print(main_dfs[date_column])

    upcoming_ipos=upcoming_ipos[upcoming_ipos[date_column].dt.date >= today].copy() #creating copy of data by filtering it
    # print(upcoming_ipos[['Name▲▼','GMP▲▼','Listing▲▼']] )

    raw_df=scrape_url(urls[1],1)
    
    headers = raw_df.iloc[0]  # Row 0 = actual headers
    data_df = raw_df.iloc[1:].reset_index(drop=True)  # Data starts row 1
    
    data_df.columns=headers #Doing proper assignment of header
    
    merged_df=merge_dataframes(upcoming_ipos,data_df)
   
    column_mapping = {
    'IPO Name':'Name',    
    'GMP▲▼': 'GMP', 
    'Close▲▼': 'Close_date',
    'Listing▲▼': 'Listing_date',
    'Price (₹)▲▼':'Price',
    'IPO Size (₹ in cr)▲▼': 'Ipo_size',
    'Lot▲▼':'Lot_size',
    'NII / HNI':'NII'
    
    }

    merged_df = merged_df.rename(columns=column_mapping)
    merged_df['Close_date'] = merged_df['Close_date'].dt.strftime('%d-%b-%Y')
    merged_df.to_json('ipo_dashboard.json', orient='records', indent=2)
    
    
    

collect_and_merge()



   

 

