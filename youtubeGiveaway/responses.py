from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ('ciao'):
        return "ciao bro"
    
    if user_message in ('come stai'):
        return "sto bene bro"

    if user_message in ('bro'):
        return "cosa c'è bro?"

    if user_message in ("ora", "ora?"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")
        clockEmoji = '⏰'

        return str("Bro, l'ora è " + date_time + " " + clockEmoji)
    if user_message in ("bho", "non lo so", "nn lo so", "boh"):
        return 'sei sus bro 🤨'
        
    return "Bro che cazzo significa?"
