import streamlit as st
import openai
from reportlab.pdfgen import canvas


from openai import AsyncOpenAI
from openai import OpenAI

client = AsyncOpenAI(
    api_key=st.secrets["API_key"],
)

async def generate_response(question, context):
  model = "gpt-4-0125-preview"
  #model - "gpt-3.5-turbo"

  completion = await client.chat.completions.create(model=model, messages=[{"role": "user", "content": question}, {"role": "system", "content": context}])
  return completion.choices[0].message.content


async def app():
  st.title("OpenAI Text Generation App")
  
  # Text input for user question
  question = st.text_input("Enter your question:")
  
  # Text area input for the context
  context = st.text_area("Enter the context:")
  
  # Button to generate response
  if st.button("Generate Response"):
      if question and context:
          response = await generate_response(question, context)
          st.write("Response:")
          st.write(response)
          generate_pdf(response)
          with open("report.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()
          download_link = create_download_link(pdf_data, "my_report")
          st.markdown(download_link, unsafe_allow_html=True)
          st.success("Your PDF is ready to download!")
    else:
          st.error("Please enter both question and context.")




def generate_pdf(text):
  """Generates a PDF document with the provided text content"""
  pdf = canvas.Canvas("report.pdf")
  pdf.setFont("Helvetica", 12)
  pdf.drawString(50, 700, text)
  pdf.save()

def create_download_link(val, filename):
  """Creates a downloadable link from a byte string"""
  b64 = base64.b64encode(val).decode("utf-8")
  return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}.pdf">Download PDF</a>'

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())
