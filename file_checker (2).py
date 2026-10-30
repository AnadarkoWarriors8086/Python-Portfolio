import smtplib
from email.message import EmailMessage
from collections import deque

file_path = "C:/Users/Racadio/Documents/file_checker/test_file_2.txt"
target_string = "Summary of Account Activity"

num_notices = 0
buffer_size = 6
line_buffer = deque(maxlen=buffer_size)
names_in_notices = []

try:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line_buffer.append(line)
            if len(line_buffer) == buffer_size and target_string in line_buffer[-1]:
                if (line_buffer[0])[10:37] != "":
                    new_name = (line_buffer[0])[10:37]
                    if new_name not in names_in_notices:
                        names_in_notices.append((line_buffer[0])[10:37])          
    num_notices = len(names_in_notices)
         
#         #content = file.read()
#         #num_notices = content.count(target_string)
#         #print(f"File read successfully. Found {num_notices} occurrences.")

except Exception as e:
     print(f"An error occurred: {e}")


msg = EmailMessage()
msg["Subject"] = "Verification Totals FSNB LOCs"
msg["From"] = "jamesrracadio@gmail.com"
msg["To"] = "jamesrracadio@gmail.com"
msg.set_content(f"File has been sent. The number of notices is {num_notices}.")

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        server.login("jamesrracadio@gmail.com", "aqwm ixwn wzqy bszn")
        
        server.send_message(msg)
        print("Email sent succesfully")
except Exception as e:
    print(f"Error: [{e}")
