import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
load_dotenv()
myapikey=os.getenv("GROQ_API_KEY")

if not myapikey:
    raise ValueError("API Error")
client=Groq(api_key=myapikey)
model= "llama-3.3-70b-versatile"

class Resume(BaseModel):
    name:str
    email:str
    phone:str
    percentage_hire:int
    should_hire_or_not:str
    reason:str

schema=Resume.model_json_schema()
response_format={"type": "json_object"}
from pypdf import PdfReader
reader1=PdfReader(r"C:\Users\Sumit\Downloads\Data_Scientist_Skills_for_HR.pdf")
text1=""
for i in reader1.pages:
    p=i.extract_text()
    if p:
        text1+=p + "\n"
text2=""
reader2=PdfReader(r"C:\Users\Sumit\Downloads\Sample_Data_Scientist_Resume.pdf")
for i in reader2.pages:
    p=i.extract_text()
    if p:
        text2+=p +"\n"
message_system={"role":"system","content":f"""You are an experienced HR. Text1 {text1} is your requirement and standard for a candidate's resume. I want you to judge the candidate's skills according to text1 and see if he is fit to be a data scientist. Give me the output in json format. The output should follow this schema {schema}"""}

message={"role":"user","content":f"""This is a candidate's resume here in this text {text2}"""}

messages=[message_system,message]
response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer=response.choices[0].message.content
print(answer)
