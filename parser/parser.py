import os
import time
import json
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://examenpdd.com/tickets/"
DATA_PATH = "../data/"

driver = webdriver.Firefox()

def saveExam (examNumber: int) -> dict:
    driver.get(f"{URL}{examNumber}")
    questions = []

    for i in range (20):

        driver.implicitly_wait(2) 
        driver.find_element(by=By.CSS_SELECTOR, value="a.hint-button").click()  

        question = driver.find_element(by=By.CSS_SELECTOR, value="div.text")
        hintText = driver.find_element(by=By.CSS_SELECTOR, value="div.hint-text")
        answers = driver.find_elements(by=By.CSS_SELECTOR, value=".answer")
        questionDict = {
                "question": question.text,
                "hint": hintText.text,
                "answers": [],
                "image": False
        }
        for answer in answers:
            questionDict["answers"].append (answer.text)
    
        try:        
            image = driver.find_element(by=By.CSS_SELECTOR, value=".question img")
            src = image.get_attribute("src")
            imageData = requests.get(src).content
            
            filename = f"{DATA_PATH}images/{examNumber}/{i}.jpg"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open (filename, "wb") as file:
                file.write (imageData) 

            questionDict["image"] = True
        except Exception as err:
            print (err)
            print (f"EXAM: {examNumber}\tQUESTION: {i+1}\thave no img.")

        driver.implicitly_wait(2) 
        answers[0].click()
        driver.implicitly_wait(2) 

        try: 
            correctAnswer = driver.find_element(by=By.CSS_SELECTOR, value=".answer.correct")
            for i, answer in enumerate(answers):
                if answer.text == correctAnswer.text: questionDict["correctIndex"] = i
        except: questionDict["correctIndex"] = 0
            
        questions.append (questionDict)

        if questionDict["correctIndex"] == 0: continue
        
        driver.implicitly_wait(2)
        driver.find_element(by=By.CSS_SELECTOR, value=".next-button").click()

    with open (f"{DATA_PATH}/tickets/{examNumber}.json", "w") as file:
        file.write(json.dumps(questions))
        
def __main__ ():
    print ("SAVING EXAMS...\n")
    for i in range (1, 41):
        print (f"Saving exam No {i}...")
        saveExam (i)

if __name__ == "__main__":
    __main__ ()

driver.quit() 
