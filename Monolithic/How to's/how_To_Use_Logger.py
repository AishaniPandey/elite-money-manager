# How to use logging system: 

# First: Add the necessary imports

# Call the log_Message function while keeping the following parameters in mind:

# log_Message(subsystem_Name, severity, message)

# Subsystem names should be : 
# For Authentication : authentication
# For Budget Manager : budget-manager
# For Data View Subsystem : data-view
# For Feedback and Support : feedback-support
# For Monitoring : monitoring
# For Notification : notification
# For Payment Logger : payment-logger
# For Testing : test

# Severity types should be :
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL 

# Message can be any string.

# Eg : For testing purpose.


from logger import Logger

logger = Logger()
logger.log_Message("test", "INFO", "Hopefully everything is working :)")
logger.log_Message("test", "INFO", "Thankfully everything is working :)")
