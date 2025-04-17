from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
groq=Groq()
def classify_with_LLM(log_msg) :
    prompt =  f'''Classify the log message into one of these categories: 
    (1) Workflow Error, (2) Deprecation Warning.
    If you can't figure out a category, use "Unclassified".
    Only return the category name. No preamble.Put the category inside <category> </category> tags. 
    Log message: {log_msg}'''

    chat_completion = groq.chat.completions.create(

    messages=[
    {
        "role": "user",
        "content": prompt
    }
    ],
    model="llama-3.3-70b-versatile"
    )

    content = chat_completion.choices[0].message.content
    match = re.search(r'<category>(.*)<\/category>', content, flags=re.DOTALL)
    category = "Unclassified"
    if match:
        category = match.group(1)

    return category

# if __name__ == "__main__":
#     print(classify_with_LLM(
#         "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."))
#     print(classify_with_LLM(
#         "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"))
#     print(classify_with_LLM("System reboot initiated by user 12345."))