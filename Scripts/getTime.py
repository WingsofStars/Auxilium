from datetime import datetime
def main():
    now = datetime.now()
    return "The Current Time is "+ now.strftime("%H") + " " + now.strftime("%M")