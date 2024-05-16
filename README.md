# Popcode

## How to install & use

Assuming you have python3 and Django installed. It may work better on linux or WSL.

- Clone the repository `git clone https://github.com/OhHuijin/WP_modern-website-.git popcode`

- Go to this folder `cd popcode`

- Open it in VSCode `code .`

- Start server `python3 django/popcode/manage.py runserver`

## How to deploy on the online web server (SSH / SFTP)

Use the credentials given on kakaotalk. The online server is on linux debian.

- Use SFTP to drag and drop files

- Use SSH to restart server if needed :

> **Useful sh commands :**  
> `screen -r popcode` to rattach the console to the popcode session. If you close your terminal, the popcode session won't be terminated.  
> `. ~/venv/bin/activate` to enable venv (often required by django)
> `python3 ~/django/manage.py runserver` to run the django server

