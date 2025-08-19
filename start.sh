#!/bin/sh
# Start backend and frontend simultaneously
python -m backend.server &
BACK_PID=$!

npm --prefix frontend run dev &
FRONT_PID=$!

trap 'kill $BACK_PID $FRONT_PID' INT TERM
wait $BACK_PID $FRONT_PID
