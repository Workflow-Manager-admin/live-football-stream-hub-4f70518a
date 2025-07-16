#!/bin/bash
cd /home/kavia/workspace/code-generation/live-football-stream-hub-4f70518a/football_stream_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

