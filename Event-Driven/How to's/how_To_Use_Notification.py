# How to use notification system: 

# First: Add the necessary imports

# Call the send_Notification function while keeping the following parameters in mind:

# send_Notification (to_Email, subject, body):

# to_Email - A string which denotes the email Id of the receiver.
# subject - A string denoting the content of the subject. 
# body - A string denoting the content of the body. 

# Note: Emails will be sent by Email Id: fornotificationuseseproject3@gmail.com

# Eg : For testing purpose.

from notify import Notify

notify = Notify()
notify.send_Notification("fornotificationuseseproject3@gmail.com", "Please work :)", "Testing Notification System")