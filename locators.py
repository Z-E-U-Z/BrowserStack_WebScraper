from webelement import Element


class Locators:
    
    COOKIE_ACCEPT_BUTTON = Element("xpath", "//button[contains(text(), 'Accept') or contains(text(), 'Aceptar')]")
    OPINION_LINK = Element("xpath", "//a[contains(text(), 'OPINIÓN') or contains(text(), 'Opinión')]")
    ARTICLE_LINKS = Element("xpath", "//article//header//h2//a[contains(@href, '/opinion/')]")
    TITLE = Element("xpath", "//*[@id='main-content']/header/div/h1")
    CONTENT_PARAGRAPHS = Element("xpath", "//div[contains(@class,'a_c')]//p | //div[@class='a_e']//p | //article//p")
    CONTENT_SUMMARY = Element("xpath", "//*[@id='main-content']/header/div/h1/following-sibling::h2")
    IMAGE = Element("xpath", "//*[@id='main-content']/header/div/following-sibling::div/figure/span/img") 
