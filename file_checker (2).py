#This script is created to scan a text document filled with FI customer notices. 
#This text document contains multiple notices, and the vendor needs to know the number expected.
#This script will then construct an email and send it to the vendor for verification.



#Import smtplib and EmailMessage to send the verification email.
import smtplib
from email.message import EmailMessage
#Import deque to allow the ability to search the prior lines for unique names.
from collections import deque

#File path should be changed for each system used on for the location of the text document.
file_path = "C:/Users/Racadio/Documents/file_checker/test_file_2.txt"
#The target string to be searched int he text document.
target_string = "Summary of Account Activity"

#Create variables for the number of notices, set the number of lines to retain in the buffer, and create a list to store unique names.
num_notices = 0
buffer_size = 6
line_buffer = deque(maxlen=buffer_size)
names_in_notices = []

#Open the text document and scan line-by-line for the target string.
#The line buffer is the number of lines (current and prior) to retain and be able to search.
try:
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line_buffer.append(line)
            if len(line_buffer) == buffer_size and target_string in line_buffer[-1]:
                #Ensure there is a name found.
                if (line_buffer[0])[10:37] != "":
                    #Set the new name to a variable and check if it already exists in the list of unique names.
                    new_name = (line_buffer[0])[10:37]
                    if new_name not in names_in_notices:
                        names_in_notices.append((line_buffer[0])[10:37])     
    #Set the num_notices to the length of the list of unique names.                    
    num_notices = len(names_in_notices)
         
#         #content = file.read()
#         #num_notices = content.count(target_string)
#         #print(f"File read successfully. Found {num_notices} occurrences.")

except Exception as e:
     print(f"An error occurred: {e}")

#Construct the email.
msg = EmailMessage()
msg["Subject"] = "Verification Totals LOCs"
msg["From"] = "xxxxxxxxxxxxxx@gmail.com"
msg["To"] = "xxxxxxxxxxxxxx@gmail.com"
msg.set_content(f"File has been sent. The number of notices is {num_notices}.")

#Send the email.
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        server.login("xxxxxxxxxxxxxx@gmail.com", "xxxx xxxx xxxx xxxx")
        
        server.send_message(msg)
        print("Email sent succesfully")
except Exception as e:
    print(f"Error: [{e}")
