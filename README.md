build with
```
pyinstaller -D -n GVU --contents-directory _GVU --uac-admin --add-data _GVU/locale/localization.json:locale main.py
```