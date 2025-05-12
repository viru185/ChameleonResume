
# config related to logging
"""
Log levels:
    DEBUG: Detailed information, typically of interest only when diagnosing problems.
    INFO: Confirmation that things are working as expected.
    WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still functioning as expected.
    ERROR: Due to a more serious problem, the software has not been able to perform some function.
    CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
    
"""

LOG_LEVEL = None  # Default is set to INFO
LOG_TO_FILE = None  # Default is set to True to log to file
LOG_TO_CONSOLE = True # Default is set to False to not log to console


# CONFIGURATION FOR LLM
LLM_MODEL = None  # Defalut is set to mistral