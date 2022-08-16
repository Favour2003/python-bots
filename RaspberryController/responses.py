from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('ciao'):
        return "ciao"
    
    if user_message in ('come stai'):
        return "sto bene"

    if user_message in ("ora", "ora?"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")
        utf8emoji = '⏰'

        return str(date_time + " " + utf8emoji)
    if user_message in ("bho", "non lo so", "nn lo so", "boh"):
        utf8emoji = '\xF0\x9F\x98\xA0'
        return 'sei sus 🤨'
        
    return "Che cazzo significa?"

