# Peer-to-peer-UDP-Broadcasting-chat
Github: https://github.com/artak10t/Peer-to-peer-UDP-Broadcasting-chat.git

## Purpose
This program creates a peer-to-peer chat application on a local network without the use of a server. It is lightweight, simple, and utilizes the UDP and TCP protocols to broadcast and listen. It then creates sockets to facilitate messages between two connected clients.

## Installation
To run this program, you must have Python installed on your system. Get Python here: https://www.python.org/downloads/ 

Download the repository into your local machine/workspace, there are a few ways to do this:

1. git clone:
   - go to the workspace you want to run the program from
   - open terminal
   - run `git clone https://github.com/artak10t/Peer-to-peer-UDP-Broadcasting-chat.git`

2. download zip file:
   - go to the repository (link is provided)
   - click on "download zip"
   - extract the zip file to your workspace
  
3. Github Desktop:
   - click on file on the top left
   - go to "clone repository"
   - enter `https://github.com/artak10t/Peer-to-peer-UDP-Broadcasting-chat.git` into the URL
   - specify local path

## Usage
The point of entry of the program is `authorize.py`. Run the file, and you will be prompted to enter your name and the port number to use
  - list of current users will be displayed
  - select the user you want to chat with and click "Chat"
  - communication channel is established between the user and you
      **there is currently no functionality to allow group chat (more than two users can chat with eachother)**
  - click on disconnect to end the chat
  - home screen displays all users
  - you quit the program or initiate another chat


  - if someone else would like to chat with you, you will receive a popup notification, and can choose to accept or decline the chat

## Configuration
The program runs on the local network, and sockets need to be enabled on the user's device in order to chat

## Contribution
The project is publicly available on Github, and anyone is free to contribute as long as original credit is given

*README updated Dec 4, 2023
