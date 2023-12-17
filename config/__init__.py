import os

log_path = "config/logs"
debug_path = "config/logs/debug_logs.log"
session_path = "config/logs/session_logs.log"
if not os.path.exists(log_path):
    os.mkdir(log_path)
    
if not os.path.exists(debug_path):
    with open(debug_path, 'w'): pass

if not os.path.exists(session_path):
    with open(session_path, 'w'): pass