class iPrint:
    def event(msg, start=''):
        print(f"{start}{Fore.BLUE}[*]{Fore.WHITE} {msg}")
    def info(msg, start=''):
        print(f"{start}{Fore.GREEN}[+]{Fore.WHITE} {msg}")
    def confi(msg, start=''):
        print(f"{start}{Fore.MAGENTA}[x]{Fore.WHITE} {msg}")
    def error(msg, start=''):
        print(f"{start}{Fore.RED}[-]{Fore.WHITE} {msg}")

def uncolor(str):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', str)

try:
    import re
    import os
    import sys
    import socket
    import _thread
    import datetime
    from colorama import *
    chat_opened = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    prompt = f"{Fore.BLUE}[>]{Fore.WHITE} {Fore.GREEN}x0x{Fore.WHITE} {Fore.YELLOW}>>>{Fore.WHITE} "
    username = os.getlogin()
    chat_history = {f"": []}
    chat_history["INFO"] = [f"[{Fore.GREEN}{chat_opened}{Fore.WHITE}] {Fore.GREEN}INFO{Fore.WHITE} Created a new chat session"]

    def append_info(msg):
        msgsent = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        old_history = list(chat_history.get("INFO")) 
        old_history.append(f"["+Fore.GREEN+msgsent+Fore.WHITE+"]"+Fore.BLUE+" "+"INFO"+" "+Fore.WHITE+msg)
        chat_history["INFO"] = old_history

    def on_new_client(conn, addr, uin, key, nocolor):
        uname = ""
        try:
            iaddr = addr[0].strip()

            print(f"{Fore.GREEN}[+]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}/{Fore.MAGENTA}unknown{Fore.WHITE}) has connected")

            uinp = f"""{Fore.MAGENTA}
___.   ____   ________________      ___ ___  
\_ |__/_   | /  |  \__    ___/___  /   |   \ 
 | __ \|   |/   |  |_|    |_/ ___\/    ~    \\
 | \_\ \   /    ^   /|    |\  \___\    Y    /
 |___  /___\____   | |____| \___  >\___|_  / 
     \/         |__|  {Fore.YELLOW}v1.0.0.0{Fore.MAGENTA}  \/       \/  
{Fore.WHITE}
""" + uin.replace("x0x", f"{Fore.GREEN}Enter a name + secret{Fore.WHITE}")
            
            if nocolor:
                conn.send(uncolor(uinp).encode())
            else:
                conn.send(uinp.encode())

            index = 0
            last_message = ""
            while True:
                sent = False
                tryed_to_send_join = False

                response = ""

                msg = conn.recv(1024)

                msgsent = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                message = msg.decode()
                message = message[0:message.__len__() - 1]
                
                if index == 0:
                    try:
                        if message.split()[1] == key:
                            if message.split()[0].lower() != "info":
                                pass
                            else:
                                print(f"{Fore.RED}[-]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}) does not know the key!")
                                conn.send(f"{Fore.RED}[-]{Fore.WHITE} Not allowed!".encode())
                                conn.close() 
                                break
                        else:
                            print(f"{Fore.RED}[-]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}) does not know the key!")
                            conn.send(f"{Fore.RED}[-]{Fore.WHITE} Wrong key no chat!".encode())
                            conn.close()
                            break
                    except:
                        conn.send(f"{Fore.RED}[-]{Fore.WHITE} No key no chat!".encode())
                        conn.close()
                        break
                    uname = message.split()[0].strip()
                    print(f"{Fore.GREEN}[+]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}) has selected the username ({Fore.MAGENTA}{uname}{Fore.WHITE})")
                    append_info(f"{Fore.MAGENTA}{uname}{Fore.WHITE} Joined!")
                    
                    try:
                        if chat_history[uname] == None:
                            pass
                    except:
                        chat_history[uname] = [f"[{Fore.GREEN}{msgsent}{Fore.WHITE}]{Fore.MAGENTA} {uname}{Fore.WHITE} Joined!"]

                else:
                    if message.strip() != ".." and message.strip() != "": 
                        if message.strip().lower() == "joined!":
                            tryed_to_send_join = True
                            print(f"{Fore.GREEN}[+]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}/{Fore.MAGENTA}{uname}{Fore.WHITE}) sent {Fore.GREEN}'{message}'{Fore.RED} (will not be shown){Fore.WHITE}")
                        else:
                            print(f"{Fore.GREEN}[+]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}/{Fore.MAGENTA}{uname}{Fore.WHITE}) sent {Fore.GREEN}'{message}'{Fore.WHITE}")
                    else: 
                        message = ".."
                        print(f"{Fore.GREEN}[+]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}/{Fore.MAGENTA}{uname}{Fore.WHITE}) wants to read more messages")
                    old_history = list(chat_history.get(uname))
                    old_history.append(f"["+Fore.GREEN+msgsent+Fore.WHITE+"]"+Fore.BLUE+" "+uname+" "+Fore.WHITE+message)
                    chat_history[uname] = old_history
                    sent = True


                sorted_messages = []
                unordered_messages_dic = {}
                unordered_messages = []
                for name in chat_history:
                    for msg in chat_history[name]:
                        nocolors_msg = uncolor(msg)
                        unordered_messages.append(nocolors_msg)

                for msg in unordered_messages:
                    msg_only = msg_date = msg[21:].strip()

                    msg_date = msg[:20].strip()
                    msg_date = msg_date[1:]

                    unordered_messages_dic[msg] = "Created", msg_date
                
                sorted_messages = sorted(unordered_messages_dic, key=lambda x: datetime.datetime.strptime(x[:20][1:].strip(), "%d-%m-%Y %H:%M:%S"))
                
                read = False
                for msg in sorted_messages:
                    if last_message.strip() == "":
                        read = True
                        last_message = "["+ msgsent +f"] {uname} Joined!"

                    if msg == last_message and read != True:
                        read = True
                        continue
                    elif read == False:
                        continue
     
                    msg_only = msg[21:].strip()

                    msg_date = msg[:20].strip()
                    msg_date = msg_date[1:]
                    usernm = msg_only.split()[0].strip()
                    msg_msg_only = msg_only[usernm.__len__():].strip()
                    if usernm.lower() == "info":
                        usernm = f"{Fore.GREEN}INFO {Fore.BLUE}(V){Fore.BLUE}"
                    full_colored_message = f"[{Fore.GREEN}{msg_date}{Fore.WHITE}] {Fore.MAGENTA}{usernm}{Fore.WHITE} {msg_msg_only}"
                
                    if read:
                        if msg_msg_only != ".." and msg_msg_only.strip().lower() != "joined!": 
                            response += full_colored_message + "\n"
                    

                if response.strip() == "" and sent == True and message.strip() != "..":
                    if tryed_to_send_join:
                        response = f"{Fore.YELLOW}[!]{Fore.WHITE} WARNING: Your message will not be displayed for others!\n"
                    else:
                        response = f"["+Fore.GREEN+msgsent+Fore.WHITE+"]"+Fore.MAGENTA+" "+uname+" "+Fore.WHITE+message + "\n"

                response = response + uin.replace("x0x", f"{Fore.MAGENTA}{uname}{Fore.WHITE}")

                if index != 0:
                    last_message = "["+ msgsent +f"] {uname} " + message
                else:
                    last_message == ""

                if nocolor:
                    response = uncolor(response)

                conn.send(response.encode())
                
                index += 1
            conn.close()
        except BrokenPipeError:
            print(f"{Fore.RED}[-]{Fore.WHITE} ({Fore.BLUE}{iaddr}{Fore.WHITE}/{Fore.MAGENTA}{uname}{Fore.WHITE}) has disconnected")
            append_info(f"{uname} has disconnected!")

    print(f"""{Fore.MAGENTA}
___.   ____   ________________      ___ ___  
\_ |__/_   | /  |  \__    ___/___  /   |   \ 
 | __ \|   |/   |  |_|    |_/ ___\/    ~    \\
 | \_\ \   /    ^   /|    |\  \___\    Y    /
 |___  /___\____   | |____| \___  >\___|_  / 
     \/         |__|  {Fore.YELLOW}v1.0.0.0{Fore.MAGENTA}  \/       \/  
{Fore.WHITE}""")

    s = socket.socket()

    if sys.argv.__len__() < 5:
        print("\nbiatch.py (host) (port) (key) (nocolor(Tr/Fl))")
        exit()

    try:
        host    = str(sys.argv[1])   # "0.0.0.0"
        port    = int(sys.argv[2])   # 7777
        key     = str(sys.argv[3])   # "vvE4$!CuNv4"
        nocolor = bool(sys.argv[4])  # False
    except ValueError:
        print(f"{Fore.RED}[-]{Fore.WHITE} Cannot convert from int(port) to str(port)")
        exit()

   
    payload = f"nc {host} {port}"

    iPrint.confi("Configuring server")

    if nocolor:
        iPrint.confi("Selected no-color mode")

    print("")

    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
    except OverflowError:
        iPrint.error("Port cannot be over 65535")
        exit()
    except OSError:
        iPrint.error(f"You are not allowed to use that address ({Fore.BLUE}{host}{Fore.WHITE})")
        exit()

    iPrint.event("Staring server\n")

    s.listen(5)

    iPrint.info(f"Server is Running on port {Fore.BLUE}{port}{Fore.WHITE}")
    iPrint.info(f"PAYLOAD ==> {Fore.BLUE}{payload}{Fore.WHITE}")

    iPrint.event("Waiting for clients\n", start='\n')

    
    while True:
       c, addr = s.accept()
       _thread.start_new_thread(on_new_client,(c, addr, prompt, key, nocolor))

    s.close()
except KeyboardInterrupt:
    pass

iPrint.error("Closing Server!", start='\n')