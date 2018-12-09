# limiting_script
Script for limiting use of specified apps (the list of apps is in the script itself) written for linux

To set it up, one needs to put downloaded the script and specify 1) the applications you want to manage 2) the path to the uselog the 3) time-limit in your script.

One also needs to install psutils: if you are using pip then typing the following in the terminal should install the package:
```
bash
python3 -m pip install psutils
```


Open the terminal and change allow an execution of the script:

```
bash
sudo chmod +x limit_script.py

```

Go to your applications and search for "Startup Applications" to add this script for running at the startup of your system.

Done!



