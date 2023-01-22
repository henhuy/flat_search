
# Wohnungssuche

Scans WBM and GEWOBAG homepages for flats.
Criteria for flats must be adopted in `wbm.py` or `gewobag.py` (should be transferred to config file instead -> future me).
In order to send link to flat to telegram you must add your TOKEN (from telegram Bot) and a CHAT_ID (a chat where Bot is present) to environment variables.
Already found flats are saved in _found_flats folder_ as plain CSV files.

## CRON

Instructions to run script every 10min via crontab:
```bash
sudo crontab -e
```

In cronfile:
```
*/10 * * * * <path to wbm.sh>
```

In wbm.sh:
```
cd <path to package>
<path to python (i.e. /home/<user>/miniconda/envs/<envname>/bin/python)> wbm.py
<path to python (i.e. /home/<user>/miniconda/envs/<envname>/bin/python)> gewobag.py
```