''' Test case to validate the cart functionality
steps
1.Navigate to the shopify store
2.Enter the store frontpassword to access the website
3.select 2 items or pair of items to get 10% discount
4.Add a product to the cart
5.Varify the cart items got proper discount and selected item is 2

Assertions
1.as selecting pair of items the quantity on cart should be 2
2.Discount for pair of items is 10% should be applied
'''
from re import findall
from time import sleep
from pytest import fixture
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

@fixture(autouse=True, scope="module")
def browser_setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://diq0y1-gv.myshopify.com/")

    # Wait for and click on the password field to log in
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//div[@class="modal__toggle-open password-link link underlined-link"]'))
    ).click()

    # Wait for the password field to appear and log in
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "Password"))
    ).send_keys("abc@123")

    # Click the submit button
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "commit"))
    ).click()

    # Wait for login to complete
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(("xpath",'//span[text()="Cherry Toys"]'))
    )

    yield driver
    driver.quit()
def test_pair_10percent_offer(browser_setup):
    driver = browser_setup

    # Select the product
    product = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "CardLink-template--17403969110155__featured_collection-7629718290571"))
    )
    product.click()

    # Wait for the 2 Pair option and select it
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//h5[contains(text(),"2 Pair")]/../../../..//div[@id="prvw__radio__botton_2"]'))
    ).click()

    # Add to cart
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@name="add"]'))
    ).click()

    # Open cart
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "cart-notification-button"))
    ).click()

    # Verify the quantity in the cart
    quantity_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "updates[]"))
    )
    quantity = quantity_element.get_attribute("value")
    assert quantity == "2", f"Expected quantity to be 2, but got {quantity}"

    # Verify the discount is applied
    discount_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//strong[@class="cart-item__final-price product-option"]'))
    )
    regular_price = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//s[@class="cart-item__old-price product-option"]'))
    )
    discount=discount_element.text
    regular_prize=regular_price.text
    print(discount_element.text, regular_price.text)
    # Extract the numeric values using regex
    new_dis = findall(r"[0-9]+\.[0-9]+", discount)
    new_reg_price = findall(r"[0-9]+\.[0-9]+", regular_prize)
    print(new_dis,new_reg_price)
    expected_discount_value = float(new_reg_price[0]) * 0.10
    # Assert that the discount was correctly applied (10% off)
    assert float(new_dis[0]) + expected_discount_value == float(new_reg_price[0]), f"Discount not applied correctly. Expected {expected_discount_value}, but got {discount_value}"
