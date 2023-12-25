# talk_to_images_with_gemini
Flask web application built with Gemini and Spire to talk to images in PDF

Steps
1. Get an OPEN AI API KEY for TruLens evaluation
2. Get Google API KEY to use Gemini Pro Vision
3. add the keys in line 11 and 12 respectively of the code
4. pip install -r requirements.txt
5. export FLASK_APP=app.py
6. flask run

   
Demo screenshots
English question : How much did Contrastive COT score in Arithematic Reasoning? 
Uploaded PDF: https://github.com/Raghavan1988/talk_to_images_with_gemini/blob/main/uploads/Survey_of_prompt_engineering_techniques_and_challenges.docx.pdf
Spanish Translation: ¿Cuánto obtuvo COT contrastivo en razonamiento aritmético?

Ask the question in Spanish to Gemini
![Screenshot from 2023-12-24 16-53-44](https://github.com/Raghavan1988/talk_to_images_with_gemini/assets/493090/eaf8928e-f0ce-4be3-bb3e-c74dde6ff792)

Gemini's response
Gemini responded in english saying Contrastive COT scored 79. 
![Screenshot from 2023-12-24 16-56-44](https://github.com/Raghavan1988/talk_to_images_with_gemini/assets/493090/eae95f37-9d01-4db8-b74e-f34c4ce99520)

Relevant image from the PDF![Image8](https://github.com/Raghavan1988/talk_to_images_with_gemini/assets/493090/aa88e1f6-8b68-4f65-929c-a7256b75bcaf)

Trulens Eval dashboard 
![Screenshot from 2023-12-24 16-59-06](https://github.com/Raghavan1988/talk_to_images_with_gemini/assets/493090/3a813117-cbdc-4c2b-83b4-4f85cd329e67)


Terminal Log for verification
![Screenshot from 2023-12-24 16-58-23](https://github.com/Raghavan1988/talk_to_images_with_gemini/assets/493090/ceb979f4-51d9-4133-a155-21af88af2bc4)

