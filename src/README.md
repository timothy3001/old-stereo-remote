## Preparation

1. Install venv via `pip install virtualenv`
2. Change to project directory (in which the setup.py is)
3. Create venv via `virtualenv venv`
4. Activate venv (`source venv/bin/activate` (Linux),
   `venv\Scripts\activate`(Windows) or say 'yes' in VSC)
5. Install requirements via `pip install -r requirements.txt`

## Installation 
1. Copy `src` content to `/etc/old-stereo-remote/`
2. Run venv preparation in that folder
3. Copy `old-stereo-remote-server.service` to `/etc/systemd/system/`