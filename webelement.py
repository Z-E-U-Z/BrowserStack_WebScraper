from selenium.webdriver.common.by import By


class Element:
    def __init__(self, strategy, locator):
        self.strategy = strategy
        self.locator = locator
        self.by_strategy = getattr(By, strategy.upper().replace(" ", "_"))
    
    def find_element(self, driver):
        return driver.find_element(self.by_strategy, self.locator)
    
    def find_elements(self, driver):
        return driver.find_elements(self.by_strategy, self.locator)
    
    def get_element(self, driver):
        """Get single element or None if not found"""
        elements = driver.find_elements(self.by_strategy, self.locator)
        return elements[0] if elements else None
    
    def click(self, driver):
        self.find_element(driver).click()
    
    def click_js(self, driver):
        """Click using JavaScript to bypass overlay issues"""
        element = self.find_element(driver)
        driver.execute_script("arguments[0].click();", element)
    
    def text(self, driver):
        return self.find_element(driver).text
    
    def get_attribute(self, driver, attribute):
        return self.find_element(driver).get_attribute(attribute)
    
    def send_keys(self, driver, keys):
        self.find_element(driver).send_keys(keys) 