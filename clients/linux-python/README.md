# Overview
This is a python-based Sicario client. It supports and will support all features, but it's not a hidden client (leaves it's traces in /etc/, has it's own service). It's written in Python 2.7

## Config file 

Config file is located in /etc/sicario/sicario.conf. It is not generated automatically, you have to create it by yourself or client will not start. Syntax is simple: host,port,userkey,interval (you can leave userkey blank if you want it to be generated automatically). Default interval is 60 seconds. The config file 
isn't encrypted in any way.

## Making it more light-weight 

If you don't need all of it's features (for example, camera module because you know that the target won't have it) you can just remove them from modules/, the client will deal with it. (It would be nice to mention, that currently this client doesn't support modules)