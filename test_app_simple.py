import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class TestDashApp(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.url = 'http://127.0.0.1:8053/'

    def tearDown(self):
        self.driver.quit()

    def test_header_present(self):
        """Test that the header is present in the app"""
        self.driver.get(self.url)
        header = self.driver.find_element(By.TAG_NAME, 'h1')
        self.assertEqual(header.text, 'Soul Foods Sales Dashboard')

    def test_visualization_present(self):
        """Test that the visualization is present in the app"""
        self.driver.get(self.url)
        graph = self.driver.find_element(By.ID, 'sales-chart')
        self.assertIsNotNone(graph)

    def test_region_picker_present(self):
        """Test that the region picker is present in the app"""
        self.driver.get(self.url)
        region_picker = self.driver.find_element(By.ID, 'region-radio')
        self.assertIsNotNone(region_picker)

if __name__ == '__main__':
    unittest.main() 