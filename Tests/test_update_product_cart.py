''' Test case to validate the cart functionality
steps
1.Navigate to the shopify store
2.Enter the store frontpassword to access the website
3.Add a product to the cart
4.Increase the quantity of the product in the cart
5.Varify the updated quantity

Assertions
1.cart quantity is updated successfully
2.quantity reflects correctly on the payment page

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
def test_update_product(browser_setup):
    driver = browser_setup

    # Select the product
    product = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "CardLink-template--17403969110155__featured_collection-7629718290571"))
    )
    product.click()

    # Wait for the 2 Pair option and select it
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.ID, 'prvw__radio__botton_1'))
    ).click()

    # Add to cart
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@name="add"]'))
    ).click()

    # Open cart
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "cart-notification-button"))
    ).click()

    # update the quantity in the cart
    update_quantity = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "plus"))
    )
    num_update = 3
    for _ in range(num_update):
        update_quantity.click()

    # Expected total items in cart
    total_items = 1 + num_update

    # Verify the quantity in the cart
    quantity_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "updates[]"))
    )
    quantity = quantity_element.get_attribute("value")
    assert int(quantity) == total_items, f"Expected quantity to be {total_items}, but got {quantity}"
     # Verify the updated quantity
    discount_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//strong[@class="cart-item__final-price product-option"]'))
    )
    Total_price = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//p[@class="totals__total-value"]'))
    )
    # Now you can interact with it
    discount=discount_element.text
    Total=Total_price.text
    print(discount_element.text, Total_price.text)
    # Extract the numeric values using regex
    new_dis = findall(r"[0-9]+\.[0-9]+", discount)
    new_total_price = findall(r"[0-9]+[,][0-9]+\.[0-9]+", Total)
    print(new_dis,new_total_price)
    expected_total_value = float(new_dis[0]) * float(total_items)
    new_val=""
    for _ in new_total_price[0]:
        if _.isdigit() or _==".":
            new_val+=_
    New_Total = float(new_val)
    # Assert that the discount was correctly applied
    assert New_Total == expected_total_value, f"Discount not applied correctly. Expected {expected_total_value}, but got {new_dis[0]}"

