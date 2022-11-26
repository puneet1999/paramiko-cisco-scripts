#!/usr/bin/python3
#importing all of the required libraries
import paramiko, getpass, time, json, datetime
import shutil, os, glob

#The function call to create a directory if not already created/present
def moveAndCreateDir(sourcePath, dstDir):
        if os.path.isdir(dstDir) == False:
                os.makedirs(dstDir);
        shutil.move(sourcePath, dstDir);

#Logs for ssh connection
paramiko.util.log_to_file("ssh_conn.log")

#Opening the file for devices to ssh into
with open("devices3.json", "r") as f:
        devices = json.load(f)

#Using a txt file for commands to input instead of explciitly configuring
#with open('commands2.txt', 'r') as f:
           # commands = [line for line in f.readlines()]

#Time variable
current = datetime.datetime.now()
time1=current.strftime("%Y-%m-%d-%H-%M-%S")
#print (time)

#input for username and password
max_buffer = 655350
with open("users.json", "r") as g:
        users = json.load(g)
username = users["username"]
#print(username)
password = users["password"]
#print(password)
#Old input way of code
#username = raw_input('Username: ')
#password = getpass.getpass('Password: ')

#Clear buffer
def clear_buffer(connection):
        if connection.recv_ready():
                return connection.recv(max_buffer)

import os.path


# Starts the loop for devices
for device in list(devices.keys()):
        try:
                file_exists = os.path.isfile((device)+".txt")
                if file_exists:
                        pass
                else:
                        xx=open((device)+".txt","wb+")
                        xx.close()
                outputFileName = device + '_output.txt'
                print(("Connecting to server : " + device + "."))
                #Sets the connection variables and shells
                connection = paramiko.SSHClient()
                connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                connection.connect(devices[device]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
                new_connection = connection.invoke_shell()
                print("Interactive SSH session established")
                output = clear_buffer(new_connection)
                #YOU MUST USE TIME.SLEEP() FOR ALMOST EVERY SINGLE COMMAND BECAUSE THE SCRIPT RUNS TO FAST FOR THE DEVICE TO INPUT
                #I HAVE WASTED MANY HOURS BECAUSE OF THIS ONE STUPID COMMAND
                time.sleep(12)
                new_connection.send("set cli pager off\n")
                time.sleep(0.500)
                new_connection.send("set cli config-output-format set\n")
                time.sleep(0.500)
                new_connection.send("configure\n")
                time.sleep(0.500)
                output = clear_buffer(new_connection)
                #print(output)
                with open(outputFileName, "wb") as f:
                        #for command in commands:
                        #SEND SHOW RUN AND COMPARE BETWEEN OUTPUT AND THE OLD CONFIG FILE
                        new_connection.send('show\n')
                        time.sleep(2)
                        output = new_connection.recv(max_buffer)
                        #print(output)
                        f.write(output)
                        f1=open((device)+".txt","rb+")
                        x1=f1.read()
                        f1.close()
                        #new_connection.close()
                        #print(x1)
                        if output == x1:
                                print ("same!")
                        else:

                                print ("changed!")
                                f= open((device)+".txt","wb")
                                f.write(output)
                                f.close()
                                #output = clear_buffer(new_connection)
                                #connection.connect(devices[device]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
                                new_connection.send('show\n')
                                time.sleep(2.500)
                                #print(stdout1)
                                output = new_connection.recv(max_buffer)
                                #print(output)
                                connection.close()
                                runing=open(device+"-"+time1+".txt","wb+")
                                runing.write(output)
                                runing.close()
                                #MOVE THE CONFIG FILE INTO THE DIRECTORY UNDER DEVICE NAME
                                moveAndCreateDir(device+"-"+time1+".txt", device)
                                print(("backup config " + (device) + " successful!"))
                new_connection.close()
        #ERROR MESSAGES WHICH I WILL FIX LATER
        #except paramiko.SSHException:
                #print("unable to connect " + str([device]))
        except paramiko.ssh_exception.NoValidConnectionsError:
                print(("unable to connect " + (device)))
        except paramiko.ssh_exception.AuthenticationException:
                print(("unable to connect " + (device) + "wrong credentials"))
