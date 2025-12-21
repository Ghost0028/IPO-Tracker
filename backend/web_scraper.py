#check and delete all unused packages 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #This will help to stop the tab pop up
from selenium.webdriver.common.by import By
import time
import pandas as pd

url="https://www.investorgain.com/report/ipo-subscription-live/333/all/"
options= Options()
options.add_argument('--headless') #Stops the pop up


driver =webdriver.Chrome(options)

driver.get(url)
time.sleep(3) #sleep for 3 unit of time for js to load

dfs= pd.read_html(driver.page_source)

print(dfs)

driver.quit()