import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st

path = 'https://docs.google.com/forms/d/e/1FAIpQLScaCjPPEZ3ICLtO488-rWaWD_y35ayVxH8buj086jouPLplag/viewform'
def model(path):
    driver = webdriver.Chrome()
    driver.set_window_size(1920, 1080)
    driver.get(path)
    driver.save_screenshot("images/s.png")
    y_relative_coord = []
    x_absolute_coord = []
    contours = []

    list_of_visible_elements = driver.find_elements(By.XPATH,"//div[not(contains(@style,'display:none'))]")



    def lister(list_of_visible_elements):
        for element in list_of_visible_elements:
            y_relative_coord = element.location['y']
            size = element.size
            w, h = size['width'], size['height']
            browser_navigation_panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
            y_absolute_coord = y_relative_coord + browser_navigation_panel_height
            x_absolute_coord = element.location['x']
            if x_absolute_coord != 0 and y_absolute_coord != 0 and w != 0 and h != 0:
                x = [x_absolute_coord, y_absolute_coord, w, h]
                contours.append(x)
        return contours

    def plot_bounding_boxes(image, coordinates_list):
        # Create figure and axes
        fig, ax = plt.subplots(1)

        # Display the image
        ax.imshow(image)

        # Plot bounding boxes
        for coord in coordinates_list:
            x, y, width, height = coord
            rect = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

        plt.savefig('images/ax.png')
        plt.show()
    contours = lister(list_of_visible_elements)
    print(contours)

    img = cv2.imread('images/s.png')
    result = img.copy()
    plot_bounding_boxes(result, contours)
    driver.quit()


st.title("Boundary Boxer")
link = st.text_input("Enter some text:")
if st.button("Click me"):
    model(link)
    st.image('images/ax.png')