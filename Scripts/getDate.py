from datetime import datetime


def main():
    today = datetime.now()
    return "Today is " + today.strftime("%B %d, %Y")

