import pathlib
import textwrap
import os
import csv
from os import listdir

import google.generativeai as genai
# from vertexai import generative_models

import PIL.Image

genai.configure(api_key="AIzaSyBhcdHLh-cbMhVGn6N1ID5ULRKFEFVcUz4")

# Load the model
model = genai.GenerativeModel('gemini-pro-vision', )


# keep the head of the test file
def clear_csv_keep_first_row(filename):
    # Read the first row from the CSV file
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader)
    
    # Write only the first row back to the CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(first_row)


# save the result of one single file
def save_to_csv(filename, imagename, response):

    # Open the CSV file in 'append' mode to add a new row
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the data to a new row
        writer.writerow([imagename] + response)



# Generation config
config = genai.GenerationConfig(
    max_output_tokens=20480, temperature=0.4, top_p=1, top_k=32
)

# Safety config
'''
safety_config = {
    genai.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    genai.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
}
'''

clear_csv_keep_first_row("test_data_eng.csv")

# get the path/directory
folder_dir = "/Users/ifsunnyace/Desktop/Mobile-News-Behavior/V4_screenshot/part_1"

# the questions we want to ask
'''
questions = ["這張截圖內是否包含圖片？若為「是」請回答: 1, 「否」則回答: 0", 
"這張截圖內是否看得見任一「留言」內容（非貼文文字）？若為「是」請回答: 1, 若為「否」則回答: 0", 
"此截圖所在的應用程式為何？若為「臉書、Facebook」請答：1，不是「臉書、Facebook」，為外部連結或其他應用程式，請答：0"]
'''

questions = ["Is any image displayed in this screenshot? 1 for yes, 0 for no",
"Any social media comment (not the post text nor comment count) visible in this screenshot? 1 for yes, 0 for no",
"Platform where screenshot is from? 1 for Facebook, 0 for offsite or other platform"]

# iterate through all pictures in folder_dir
for images in os.listdir(folder_dir):
    response = []
 
    # check if the image ends with png
    if (images.endswith(".jpg")):
        print(images)
        img = PIL.Image.open(folder_dir + "/" + images)

        for q in questions:
            # response = model.generate_content(img)
            r = model.generate_content([q, img], generation_config=config, stream=False)
            # print(r.prompt_feedback)
            # r.resolve()
            # print(r.text)
            response.append(r.text)

        save_to_csv("test_data_eng.csv", images, response)


# a dictionary: check whether the picture is processed or not

# 
  