#!/bin/bash
gnome-terminal -- python3 destination_service/app.py
gnome-terminal -- python3 user_service/app.py
gnome-terminal -- python3 auth_service/app.py



#bash run_services.sh