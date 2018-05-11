# Sicario

Sicario is a C&C server written in Python, with clients in... okay, there are not many clients currently written. Huge TODO. Anyway,
it's main purpose it to manage ~your~ (okay i can't control how you will use it okay) devices with clients installed. Currently it supports
only shell commands executions, but it's WIP. Stay tuned or contribute

## Getting Started 

There is nothing easier than deploying Sicario server. Just clone the repository, and in main directory type:
`python sicario.py`
And this is it. You may use --host and --port parameters. 

After running, it will create sicario.db file in 'db' directory. You may change the name of the file, however it does require a 
few changes in code, and to be honest, I don't see a reason to. 

Anyway. Now you run your clients, and after they'll register, you'll see them registered in the database. Now you can add jobs for them
(there will be CLI for that, maybe even GUI, but remember that this is still very alpha version of this project). But you gotta open 
your database file first. I use "DB Browser for SQLite". I think it's co-platform but not sure. So, after opening file browse
'clients' table and search for the one you want to add job for. Copy his hash and insert record into 'jobs' table. Here's a structure:

```
client_key = the hash you just copied
type = currently only execute_cmd is available 
processed = leave that at 0 or the command will not be executed
payload = the command you want to execute
result = leave that empty
executed_on = leave that empty
```

But when will your command be executed, you'd ask. And I'll be really pleasant to answer you: it won't. Okay, it will, but not
automatically. The idea is for bots to connect to the server every minute (probably only for high-priority bots, it should be also customizable) and ask for their tasks to do. Currently there aren't even clients to do this (excepting that one, shitty python example) so, 
uh, you know. (Remember, you can always contribute. I'd apreciate that)

## TCP/IP, Bitch!

Hell yeah, Sicario has it's own protocol! Already hyped? There's no need for that. Each packet consists of signature, incoming packets count
and the actual data. Here's how does registration packet look like:

`SC00(register)`

Simple as that. You are probably interested about incoming packets count, aren't you? So let me show it to you. I always deliver. 
Server accepts 2048 bytes. Signature, packets count and brackets are 6 bytes equal. 2048-6=2042. So if data you want to send 
exceeds 2042 bytes, you'll have to split it. Look at this code from python example:

```
if (len(result) > 2042): # we have to split data into smaller packets
			packet_count = int(math.ceil(len(result)/2042))
			for x in range(packet_count):
				s.send('SC{}({})'.format(str(packet_count-x).zfill(2), result[x*2042:(x+1)*2042]))
```

Confused? You should be ashamed. Or I should be ashamed. Or no, Craig should be ashamed. Its always Craig.

If your data exceeds 2042 bytes, divide it by 2042 and round up. This is going to be your packets count. 
Now create a for loop with your result as uh, you know. And every iteration, send a packet: 

SCXX(data from x*2042 to (x+1)*2042) 

Where XX is your loop index of course, but with a leading zero. Incoming packets are exactly 2 bytes length and can't be shorter.
What if incoming packets count will exceed 99? 
Well, we're all fucked.

## Server responses 

You already know how protocol works (I'm very proud of myself, I've just created a protocol. A real protocol!)

First, you have to get your unique client ID. So connect to the server and send `register` to it. 
The server should respond with `set key 667FF118EF6D196C96313AEAEE7DA519`. Of course, the key will be different. 
Save this key, it will be required for the next connection. After sending a key, the server will disconnect you. After connecting again, type

`login <the key you saved before>`. And, if there are any jobs for you, you'll get commands from server, if not, you will get disconnected

### Jobs 

Currently the only supported job is shell execution. If your bot was commissioned to do it, after logging in it will receive:

`execute <payload>`. Well, execute the payload and just return it to the server. You don't have to type any commands or anything, 
the server will know what you're returning.  

## Contribute 

What much to say. What is needed is: Windows client, MacOS client, Linux client, Android client.. You can submit to repo whatever you want 
and i'll accept it. But those are the most needed right now. Good luck!