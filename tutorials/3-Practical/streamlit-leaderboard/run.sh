#!/bin/bash

# Start the app
streamlit run src/app.py --server.maxUploadSize=10

# Start the app in debug mode
# streamlit run src/app.py --server.maxUploadSize=10 --logger.level=debug

# Exit with status of process that exited first
exit $?
