from django.shortcuts import render
from django.core.mail import send_mail
import requests
import json
from decouple import config


GROQ_API_KEY = config("GROQ_API_KEY", default=None)
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"




def meeting_summary(request):
    summary = None
    error = None
    email_sent = None
    prompt = ""

    if request.method == "POST":
       
        if 'generate' in request.POST:
            prompt = request.POST.get('prompt', '')

            
            uploaded_file = request.FILES.get('transcript_file')
            if uploaded_file:
                try:
              
                    transcript = uploaded_file.read().decode('utf-8')

                  
                    summary = generate_summary(transcript, prompt)

                except Exception as e:
                    error = f"Error reading file: {str(e)}"
            else:
                error = "No file uploaded!"

       
        elif 'send_email' in request.POST:
            subject = request.POST.get('subject', 'Meeting Summary')
            message = request.POST.get('message', '')
            recipient = request.POST.get('email', '')

            try:
                send_mail(subject, message, 'your_email@example.com', [recipient])
                email_sent = f"Email sent to {recipient}!"
            except Exception as e:
                error = f"Error sending email: {str(e)}"

    return render(request, "index.html", {
        'summary': summary,
        'error': error,
        'email_sent': email_sent,
        'prompt': prompt
    })


def generate_summary(transcript, prompt):
    """
    Preprocess transcript and call GroqCloud chat completion API for summarization
    """
    try:
       
        lines = transcript.splitlines()
        clean_lines = [line.split(". ", 1)[-1].strip() for line in lines if ":" in line]
        cleaned_transcript = "\n".join(clean_lines)

     
        ai_prompt = f"""
Summarize all discussion points from this meeting.
Include the speaker's name.
Format as separate bullet points.
Do not combine multiple points into one.

Meeting Notes:
{cleaned_transcript}

User Prompt: {prompt}
"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }

        data = {
            "model": "llama-3.3-70b-versatile",  
            "messages": [
                {"role": "system", "content": "You are a helpful meeting summarizer."},
                {"role": "user", "content": ai_prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 500
        }

        response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return f" Groq API Error {response.status_code}: {response.text}"

    except Exception as e:
        return f" Exception while calling Groq API: {str(e)}"
