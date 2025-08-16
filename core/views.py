from django.shortcuts import render
from django.core.mail import send_mail

def meeting_summary(request):
    summary = None
    error = None
    email_sent = None
    prompt = ""

    if request.method == "POST":
        # Check if generating summary
        if 'generate' in request.POST:
            prompt = request.POST.get('prompt', '')

            # Handle uploaded file
            uploaded_file = request.FILES.get('transcript_file')
            if uploaded_file:
                try:
                    # Read the file content
                    transcript = uploaded_file.read().decode('utf-8')

                    # Now call your AI summarizer function (replace this with your logic)
                    summary = generate_summary(transcript, prompt)

                except Exception as e:
                    error = f"Error reading file: {str(e)}"
            else:
                error = "No file uploaded!"

        # Check if sending email
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


# Dummy AI summary function for now
def generate_summary(transcript, prompt):
    # Replace this with your real AI logic
    return f"Summary of transcript:\n{transcript[:200]}...\n(Prompt: {prompt})"
