from datetime import datetime

def save_log(message):

    with open("logs/audit.log", "a") as file:
        file.write(
            f"{datetime.now()} : {message}\n"
        )