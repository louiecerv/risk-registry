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
  question = """Follow recommend content of the risk registry exactly.  Create a risk registry for the 
    Management Information System Office. Format the output as a table."""
  
  # Text area input for the context
  context = """Here's the recommended content and structure for your risk register:
  Content:
  Risk ID: A unique identifier for each risk (optional but helpful for tracking).
  Risk Description: A clear and concise statement describing the potential issue that could affect your QMS.
  Risk Source: The origin or cause of the risk (e.g., process failure, supplier issue, regulatory change).
  Risk Category: Grouping similar risks together (e.g., operational, financial, compliance).
  Risk Probability: Likelihood of the risk occurring, rated using a scale (e.g., low, medium, high) or a probability range (e.g., 1-10%).
  Risk Impact: Severity of the consequences if the risk materializes, rated similar to probability.
  Risk Detection Method: How the risk will be identified (e.g., process monitoring, customer feedback).
  Risk Owner: The individual or department responsible for managing the risk.
  Control Measures: Specific actions planned to reduce the likelihood or impact of the risk.
  Monitoring and Review: A plan for tracking the effectiveness of the control measures, including the frequency of review (e.g., monthly, quarterly).
  Action Effectiveness: Record the success of implemented controls in mitigating the risk."""
  
  # Button to generate response
  if st.button("Generate Risk Registry"):
      if question and context:
        response = await generate_response(question, context)
        st.write("Response:")
        st.write(response)

        generate_pdf(response)
        with open("report.pdf", "rb") as pdf_file:
          pdf_data = pdf_file.read()

        st.download_button(
            label="Download PDF",
            data=pdf_data,
            mime="application/pdf",
            key="download-pdf-button",
        )

        st.success("Your PDF is ready to download!")
      else:
        st.error("Please enter both question and context.")

def generate_pdf(text):
  """Generates a PDF document with the provided text content"""
  pdf = canvas.Canvas("report.pdf")
  pdf.setFont("Helvetica", 12)
  pdf.drawString(50, 700, text)
  pdf.save()

#run the app
if __name__ == "__main__":
  import asyncio
  asyncio.run(app())
