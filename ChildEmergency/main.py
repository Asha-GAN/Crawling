from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv


# 엑셀 파일 생성
def Excel_make():
    f = open('./result.csv', 'w', newline='', encoding="utf-8-sig")
    wtr = csv.writer(f)

    # 행 제목
    wtr.writerow(['이름', '주소', '응급실 소아 병상 여부', '소아 야간진료 여부'])
    f.close()


# 엑셀 파일에 병원명, 소아병상 여부 정보 추가
def Excel_add(data):
    f = open('./result.csv', 'a', newline='', encoding="utf-8-sig")
    wtr = csv.writer(f)

    wtr.writerow(data)

    f.close()


chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)
driver = webdriver.Chrome(service=service)

# 사이트 이동
driver.get("https://www.e-gen.or.kr/egen/main.do")

time.sleep(1)

# 보이지 않는 메뉴바(display: none) 때문에 클릭 -> '응급실 찾기' 클릭 -> '일반' 클릭
driver.find_element(By.CLASS_NAME, "lnb-depth1").click()

xpath = "/html/body/div[2]/div[3]/div/div[2]/ul/li[1]/div/ul/li[1]/a"
driver.find_element(By.XPATH, xpath).click()

time.sleep(2)

# '일반' 클릭
xpath = "/html/body/div[4]/div[2]/div[2]/span[2]/a"
driver.find_element(By.XPATH, xpath).click()

time.sleep(2)

# '서울특별시' 옵션 선택
choice = Select(driver.find_element(By.ID, "generalSidoCode"))
choice.select_by_value('11')

# '검색' 버튼 클릭
driver.find_element(By.ID, "btnSearch").click()

time.sleep(2)

# 엑셀 파일 생성
Excel_make()

num = 1
while True:
    # 정보를 저장할 리스트
    data = []

    # 병원명 추출
    xpath = (
            "/html/body/div[4]/div[2]/div[3]/div/div[2]/div/div[2]/div/ul/li[" + str(num) + "]/div[2]/h5/a"
    )

    # 해당 요소를 못 찾을 수도 있으니 예외 처리
    try:
        name = driver.find_element(By.XPATH, xpath)

    except NoSuchElementException as e:
        break

    data.append(name.text.replace('상세보기', ''))

    # 주소 추출
    xpath = (
            "/html/body/div[4]/div[2]/div[3]/div/div[2]/div/div[2]/div/ul/li[" + str(num) + "]/div/p[3]"
    )

    address = driver.find_element(By.XPATH, xpath)
    data.append(address.text)

    name.click()

    # '응급실소아병상' 이 있을 시 o, 없으면 x
    if "응급실소아병상" in driver.page_source:
        fact = "o"
    else:
        fact = "x"

    data.append(fact)

    # 뒤로 가기
    driver.back()

    # 소아 야간 진료 여부 추출
    xpath = (
            "/html/body/div[4]/div[2]/div[3]/div/div[2]/div/div[2]/div/ul/li[" + str(num) + "]/div/p[4]/em[4]"
    )

    # 해당 요소를 못 찾을 수도 있으니 예외 처리
    try:
        night = driver.find_element(By.XPATH, xpath)
        night_fact = "o"
        data.append(night_fact)

    except NoSuchElementException as e:
        pass

    Excel_add(data)
    print(data)

    num += 1
    time.sleep(1)

print()
print("크롤링이 완료되었습니다.")

driver.close()
