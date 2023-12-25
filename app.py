from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from openai import OpenAI


import google.generativeai as genai


import PIL.Image

os.environ["OPENAI_API_KEY"] = ""
GOOGLE_API_KEY=""



client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')

app = Flask(__name__)
from trulens_eval import Feedback, Tru, OpenAI
tru = Tru()
tru.reset_database()

openai_provider = OpenAI()

def translate_to_english(text):
    response = client.chat.completions.create(model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a translator to English. Check if the input is in English. If the input is english DO NOTHING and return AS-IS else Translate to English"},
        {"role": "user", "content": text},
    ],stream = False, )
    return response.choices[0].message.content

def gpt35_turbo(prompt):
    response =  client.chat.completions.create(model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "you are an AI bot, answer accurately"},
        {"role": "user", "content": prompt},
    ],stream = False, )
    return response.choices[0].message.content
f_hate = Feedback(openai_provider.moderation_hate, higher_is_better=False).on_input()
f_violent = Feedback(openai_provider.moderation_violence, higher_is_better=False).on_input()
f_selfharm = Feedback(openai_provider.moderation_selfharm, higher_is_better=False).on_input()
f_maliciousness = Feedback(openai_provider.maliciousness_with_cot_reasons, higher_is_better=False).on_input()
feedbacks = [f_hate, f_violent, f_selfharm, f_maliciousness]



from trulens_eval import TruBasicApp
gpt35_turbo_recorder = TruBasicApp(gpt35_turbo, app_id="gpt-3.5-turbo", feedbacks=feedbacks)
tru.run_dashboard()





# Configuration
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from spire.pdf import PdfDocument
from spire.pdf.common import ImageFormat

def extract_images_from_pdf(pdf_path, output_directory):
    # Load the PDF document
    doc = PdfDocument()
    doc.LoadFromFile(pdf_path)

    images = []
    # Iterate through each page in the document
    for i in range(doc.Pages.Count):
        page = doc.Pages.get_Item(i)
        
        # Extract images from the current page
        for image in page.ExtractImages():
            images.append(image)

    image_files = []
    # Save the images to the specified directory
    for idx, image in enumerate(images):
        fname = f'{output_directory}/Image{idx}.png'
        image.Save(fname, ImageFormat.get_Png())
        image_files.append(fname)

    # Close the PDF document
    doc.Close()
    return image_files

# Example usage
output_directory = 'static/extracted_images'  # Current directory

def get_gemini_response(image, text):
    prompt = """
        The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
        Take a deep breath and relax. Look at each picture, remember it, and then answer the question that follows. 
        HARD REQUIREMENTS
        1. Check if the question can be answered with the IMAGE, if not populate answer_present field of json with "No"
        2. Give a detailed answer with reason
        3. Cite to name of the image that from which you obtained the answer
        4. Answer should be atleast 10 words and formatted in HTML 
        5. Answer MUST give the name of the IMAGE from which answer was obtained
        6. Response SHOULD STRICTLY follow JSON format of the SCHEMA
        Json SCHEMA
        answer_present: String options ["Yes", "No"]
        answer: String 
        reason: String
        
        Failing to do this will result in POOR performance""" + text

        # Generate response from the model
    context_plus_prompt = [prompt] + [image]
    response = model.generate_content(context_plus_prompt, stream=False)
    response_text = response.text

    





    return response_text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process text
        text = request.form['text']
        ###processed_text = text.lower()


        # Save files
        files = request.files.getlist('file[]')
        imgs = []
        image_files = []
        img_urls = []
        response_text = ""
        for file in files:

            print (file.filename)
            

            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print (file_path)
                file.save(file_path)
                if filename.endswith(".pdf"):
                    image_files = extract_images_from_pdf(file_path, output_directory)
                    print ("extracted images from pdf")
                    print(image_files)
                    for image_file in image_files:
                        print(image_file)
                        img_urls.append(image_file)
                        img = PIL.Image.open(image_file)
                        imgs.append(img)

        text = translate_to_english(text)

        prompt = """
        The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
        Take a deep breath and relax. Look at each picture, remember it, and then answer the question that follows. 
        HARD REQUIREMENTS
        1. Answer the question with the IMAGEs
        2. Give a detailed answer with reason
        3. Cite to name of the image that from which you obtained the answer
        4. Answer should be atleast 20 words and formatted in HTML 
        5. Answer MUST give the name of the IMAGE from which answer was obtained
        
        
        Failing to do this will result in POOR performance \n Question: """ + text
                
        response = model.generate_content([prompt] + imgs, stream=False)
        response_text = response.text

        with gpt35_turbo_recorder as recording:
            gpt35_turbo_recorder.app(prompt)
            gpt35_turbo_recorder.app(response_text)
        
        # Pass both image URLs and response text to the template
        print(img_urls)
        return render_template('index.html', image_urls=img_urls, response_text=response_text)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

