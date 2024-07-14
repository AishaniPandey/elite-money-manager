# How to use monitoring system: 

# First: Add the necessary imports

# Second : Create a thread and run the following function within the thread. 

# Subsystem names should be : 
# For Authentication : authentication
# For Budget Manager : budget-manager
# For Data View Subsystem : data-view
# For Feedback and Support : feedback-support
# For Monitoring : monitoring
# For Notification : notification
# For Payment Logger : payment-logger
# For Testing : test

# Eg : For testing purpose.

from monitor import Monitor
import threading

monitor = Monitor()
t_Standard = threading.Thread(target=monitor.heartbeat_Generator, args=("test", ))
t_Standard.start()