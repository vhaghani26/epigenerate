# Connecting to the L-Drive

## UC Davis Health Systems Log-In

In order to connect to the L-drive, a health systems log-in is required. To get one, email Lawrence Ma(lwma@ucdavis.edu) and request one. We also have a lab-specific log-in that can be used if you are having trouble getting one.

## Mac OS
To connect your MAC to the L-Drive, follow the steps spelled out below:

1. Open the Finder

2. Click on Go and select Connect to Server

![github](https://github.com/vhaghani26/epigenerate/blob/main/L-Drive/Finder_Go.png)

3. You will see the connect to server window, add a new server

![github](https://github.com/vhaghani26/epigenerate/blob/main/L-Drive/Connect_to_server.png)

4. For the folder path, input `smb://hshome.ucdmc.ucdavis.edu/shared/som/medmicro/labs/lasalle lab`

5. Once you connect to the server, please enter the directory that has your name, if it doesnt exist, create one

6. An example of such a directory is here:

![github](https://github.com/vhaghani26/epigenerate/blob/main/L-Drive/Enter_(yourname)_directory.png)

Congratulations! You've finally connected to the mystical L-Drive! You can now use `rsync` in terminal to transfer files to and from the L-drive

## Windows

I recommend following [these](https://support.microsoft.com/en-gb/windows/map-a-network-drive-in-windows-29ce55d1-34e3-a7e2-4801-131475f9557d) instructions. To briefly summarize in case the link is not supported in the future:

1. Open the File Explorer

2. Select "This PC" from the left-side panel

3. Select the "Map network drive" option from the menu bar.

![github](https://github.com/vhaghani26/epigenerate/blob/main/L-Drive/find_map_network_drive.png)

4. Select a letter for the drive that does not interfere with your current drives. In this case, "L" is appropriate if it is not already taken

5. For the folder path, input `\\hshome.ucdmc.ucdavis.edu\shared\som\medmicro\labs\lasalle lab`

![github](https://github.com/vhaghani26/epigenerate/blob/main/L-Drive/map_network_drive.png)

6. This will prompt you to type your username and password. Note that your username will actually have to begin with `hs\`. This means you should type `hs\username` and your password to log in. This will connect the File Explorer to the L-Drive, which is great for local transfers, but not for transferring between Epigenerate and the L-Drive. Therefore, you will need to mount it if you plan to do anything with Epigenerate or Ubuntu and the L-Drive

7. Assuming you chose "L" as the drive letter, run the following commands:

```
mkdir /mnt/l/
sudo mount -t drvfs L: /mnt/l/
```

This creates a new directory in your mounted drives folder and connects the L-Drive to your terminal. You may need to rerun the second command whenever you want to access the L-Drive, as this usually only lasts while you're logged in. There are further instructions [here](https://www.public-health.uiowa.edu/it/support/kb48568/) if you would like to mount the drive permanently.

Congratulations! You've finally connected to the mystical L-Drive!
