import selenium
from selenium import webdriver
import urllib.request
from PIL import Image
import time
import os

class Box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def test(title, type, num) :
    # if title == "버스" :
    #     # !./ darknet detector test data/obj_bus.data cfg/bicycle_bus_taxi.cfg weights/bus.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt
    # elif title == "택시" :
    #     # !./ darknet detector test data/obj_taxi.data cfg/bicycle_bus_taxi.cfg weights/taxi.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt
    # elif title == "자전거" :
    #     # !./ darknet detector test data/obj_bicycle.data cfg/bicycle_bus_taxi.cfg weights/bicycle.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt
    # elif title == "야자수" :
    #     # !./ darknet detector test data/obj_palmtree.data cfg/car_palm_crosswalk.cfg weights/palmtree.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt
    # elif title == "횡단보도" :
    #     # !./ darknet detector test data/obj_crosswalk.data cfg/car_palm_crosswalk.cfg weights/crosswalk.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt
    # elif title == "차량" or title == "자동차" :
    #     # !./ darknet detector test data/obj_car.data cfg/car_palm_crosswalk.cfg weights/car.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt
    # elif title == "굴뚝" :
    #     # !./ darknet detector test data/obj_car.data cfg/chimney_mountain.cfg weights/car.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt
    # elif title == "산 또는 언덕" :
    #     # !./ darknet detector test data/obj_car.data cfg/chimney_mountain.cfg weights/car.weights test.jpg - i 0 - thresh 0.3 - ext_output - out result.json > result.txt

    f = open('test.txt', 'r')
    lines = f.readlines()
    predictions = []
    indices = []
    for line in lines:
        if "%" in line:
            line = line[:-2]
            coords = line.split("(")[1]
            x = int(coords[7:12].strip())
            y = int(coords[21:27].strip())
            w = int(coords[37:43].strip())
            h = int(coords[52:58].strip())
            predictions.append(Box(x, y, w, h))
    img = Image.open('test.jpg')
    imgWidth = img.width
    for box in predictions :
        if type == 0 :
            indice_arr = getIndex0(box, num, imgWidth)
            for x in indice_arr: indices.append(x)
        else :
            index = getIndex1(box.x, box.y, imgWidth, num)
            indices.append(index)
    return list(set(indices))



def getIndex0(box, num, imgWidth) :
    minX = box.x
    maxX = box.x + box.width
    minY = box.y
    maxY = box.y + box.height
    indices = []

    leftTop = getIndex1(minX, minY, imgWidth, num)
    rightTop = getIndex1(maxX, minY, imgWidth, num)
    leftBottom = getIndex1(minX, maxY, imgWidth, num)
    rowNum = int((leftBottom-leftTop)/num) + 1
    colNum = rightTop - leftTop + 1
    print(leftTop, rightTop, leftBottom)
    for i in range(0, rowNum) :
        for j in range(0, colNum) :
            n = leftTop + num * i + j
            print(n)
            indices.append(n)
    return indices

def getIndex1(x, y, width, num) :
    if num == 3 :
        oneThird = width/3
        twoThirds = oneThird * 2
        if x < oneThird :
            if y < oneThird : return 0
            elif y > oneThird and y < twoThirds : return 3
            else : return 6
        elif x > oneThird and x < twoThirds :
            if y < oneThird : return 1
            elif y > oneThird and y < twoThirds : return 4
            else : return 7
        else :
            if y < oneThird : return 2
            elif y > oneThird and y < twoThirds : return 5
            else : return 8
    else :
        oneQuarter = width / 4
        twoQuarters = oneQuarter * 2
        threeQuarters = oneQuarter * 3
        if x < oneQuarter:
            if y < oneQuarter : return 0
            elif y > oneQuarter and y < twoQuarters : return 4
            elif y > twoQuarters and y < threeQuarters : return 8
            else : return 12
        elif x > oneQuarter and x < twoQuarters :
            if y < oneQuarter : return 1
            elif y > oneQuarter and y < twoQuarters : return 5
            elif y > twoQuarters and y < threeQuarters : return 9
            else : return 13
        elif  x > twoQuarters and x < threeQuarters :
            if y < oneQuarter : return 2
            elif y > oneQuarter and y < twoQuarters: return 6
            elif y > twoQuarters and y < threeQuarters: return 10
            else: return 14
        else :
            if y < oneQuarter : return 3
            elif y > oneQuarter and y < twoQuarters : return 7
            elif y > twoQuarters and y < threeQuarters : return 11
            else : return 15
#
def clickAnswers(title, tag, type) :
    indices = tag.find_elements_by_tag_name("td")
    num = len(indices)
    if num == 9 : num = 3
    else : num = 4
    answers = test(title, type, num)
    print(answers)
    for answer in answers :
        indices[answer].click()
#
#
classes = ["버스", "택시", "자전거", "야자수", "횡단보도", "굴뚝", "산 또는 언덕", "차량", "자동차"]
urlString = "https://www.google.com/recaptcha/api2/demo"
path = os.path.join(os.getcwd(), 'chromedriver.exe')
driver = webdriver.Chrome(path)
# driver = webdriver.Chrome("C:/Users/mypc/PycharmProjects/pythonProject/chromedriver.exe")
driver.get(urlString)
try:
    driver.switch_to.frame(0)
    driver.find_element_by_id('recaptcha-anchor').click()
    driver.switch_to.parent_frame()
    driver.switch_to.frame(2)
    time.sleep(6)
    question = driver.find_element_by_xpath('//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div')
    html = question.get_attribute('innerHTML')
    title = question.find_element_by_tag_name('strong').get_attribute('innerHTML')
    type = 0 # 한 이미지를 여러 그리도 쪼갠것
    if "이미지를" in html : type = 1 #여러 이미지 붙인 것
    while title not in classes :
        driver.find_element_by_id("recaptcha-reload-button").click()
        time.sleep(3)
        question = driver.find_element_by_xpath('//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div')
        html = question.get_attribute('innerHTML')
        title = question.find_element_by_tag_name('strong').get_attribute('innerHTML')
        type = 0  # 한 이미지를 여러 그리도 쪼갠것
        if "이미지" in html: type = 1  # 여러 이미지 붙인 것
        else : type = 0
    imgTag = driver.find_element_by_tag_name('img')
    imgSize = imgTag.get_property('class') # 3x3인지 4x4인지
    imgUrl = imgTag.get_property('src')
    urllib.request.urlretrieve(imgUrl, "test.jpg")
    clickAnswers(title, driver.find_element_by_tag_name('tbody'),type)
    driver.find_element_by_id("recaptcha-verify-button").click()
    driver.find_element_by_id("recaptcha-demo-submit")
except selenium.common.exceptions.NoSuchElementException :
    print("CANNOT FIND")