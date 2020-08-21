
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": "/Users/michaelwood/Documents",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/Users/michaelwood/Documents/GenerationData/scripts/chromedriver")

# change the <path_to_place_downloaded_file> to your directory where you would like to place the downloaded file
download_dir = "/Users/michaelwood/Documents"

# function to handle setting up headless download
enable_download_headless(driver, download_dir)

# get request to target the site selenium is active on
driver.get("https://elections.sos.ga.gov/Elections/voterabsenteefile.do")


wait = WebDriverWait(driver, 10)


element = wait.until(EC.visibility_of_element_located((By.ID, "nbElecYear")))

select = Select(element)
select.select_by_value("2020")


gacat = wait.until(EC.visibility_of_element_located((By.ID, "cdElecCat")))

catselect = Select(gacat)
catselect.select_by_value("SW")


gaelectionname = wait.until(EC.visibility_of_element_located((By.ID, "idElection")))

gaselect = Select(gaelectionname)
gaselect.select_by_value("35213")


search_input =  driver.find_element_by_xpath('//a[@href="'+'javascript:downLoadFile();'+'"]')

search_input.click()