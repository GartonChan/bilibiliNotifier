### A Notifier for Bilibili Subscriptions

#### Prerequisites
Creating a virtual environment of Python is a better way for deploying.
``` shell
pip install -r requirements.txt
# if you need to change mirrors, then append this:
# -i https://pypi.tuna.tsinghua.edu.cn/simple
```
#### Usage
Step 1. 

Configure `user_config.py` to your settings.

Write down the uploaders' mid in `mid.txt`

Note that set scheduled tasks for notifying in `main.py`

Here are templates for these two files, see `user_config.py.template` and `mids.txt.template`.


Step 2. 
``` shell
# if needed, activate your virtual environment.
python main.py
```

#### Deploy at the backend
A simple way to do this:
``` shell
screen -S bilibiliNotifier
python main.py
# Press Ctrl+A and then press D to exit
# return using "screen -r bilibiliNotifier"
```
