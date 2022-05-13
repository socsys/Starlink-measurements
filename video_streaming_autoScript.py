from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

ABR_Alg = sys.argv[1]
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--headless")
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)
driver.get("https://video-server.duckdns.org/dash.js/samples/dash-if-reference-player/index.html")
print(driver.title)

time.sleep(5)
elem = driver.find_element_by_xpath('/html/body/div[2]/div[1]').click()
time.sleep(2)


driver.execute_script("document.getElementById('run_count').setAttribute('value', arguments[0])",sys.argv[2]);
time.sleep(5)
driver.execute_script("document.getElementById('starlink_name').setAttribute('value', arguments[0])", "Starlink-Alan_"+str(sys.argv[1]));

time.sleep(5)

stats_bt = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div[4]/div/div[1]/div/div[13]/button')
driver.execute_script("arguments[0].click();", stats_bt);

time.sleep(5)

if ABR_Alg == "abrThroughput":
	abr_thr = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[2]/label[3]/input')
	driver.execute_script("arguments[0].click();", abr_thr);
	time.sleep(5)

if ABR_Alg == "abrBola":
	abr_thr = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div[2]/div[1]/div[2]/label[2]/input')
        driver.execute_script("arguments[0].click();", abr_thr);
        time.sleep(5)

start_bt = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/span/button[3]')
driver.execute_script("arguments[0].click();", start_bt);

while 1:
	duration = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[1]/div/div[2]/span[1]')
	if duration.text == "02:38":
		print("End of this itration")
		print(driver.title)
		driver.quit()
