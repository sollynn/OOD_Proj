class Node:
    def __init__(self,data,left =None , right =None):
        self.data = data
        self.left =None if left is None else left
        self.right =None if right is None else right
class AVL :
    pass
class Customer:
    def __init__(self,customer_num,channel, ID = None ,room_id = None):
        self.customer_num = customer_num
        self.channel = channel
        self.ID = ID
        

    def ID(self,customer_num,channel):
       
        ch = channel.upper()
        if not ch.isalpha():
            return f'error: channel must be letters A-Z'
        else:
            code = 0
            for c in ch:
                if 'A' <= c <= 'Z':
                    code = code * 26 + (ord(c) - ord('A') + 1)

        if not customer_num.isdigit():
            
            return f'error: customer_num must be number'

        num = int(customer_num)
        if not ( 1 <= num <= 999):
            return f'error: channel or customer_num out of range'

        self.channel = ch
        self.customer_num = num
        self.ID = int(f"{code:03d}{num:03d}")
       
        return self.ID

    class Room:
        def __init__ (self,room_id = None):
            self.room_id = None
        def manage_room(self,ID):
            pass

        def add_room(self):
            pass

        def del_room(self):
            pass

        def find_room(self):
            pass

        def memmory(self):
            pass



hotel = Customer(None, None)

while True:
    command = input("enter command : ").strip()
    if not command:
        continue

    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if cmd == "add":  # pattern: add A1,A2,B1,B2
       
        items = [x.strip() for x in args.split(",")] if args else []
        parsed = [(it[0], it[1:]) for it in items if it]
        for ch, num in parsed:
            new_id = Customer.ID(hotel,num, ch)
            print(new_id) 

        pass
    
    elif cmd == "addroom": 
        pass

    elif cmd == "delete":  

        pass

    elif cmd == "find": 
        room = args.strip()
        hotel.room_id = room
        hotel.find_room()
        pass

    elif cmd == "show":
        pass

    elif cmd == "showcustomerdata":
        pass

    else:
        print("error command arai wa:", cmd)
"""
input pattern : add A1,A2,B1,B2 (channel=char,User=num)
input pattern : addRoom 00
input pattern : delete 001 ( Room wanna delete)
input pattern : find 001 ( Room wanna search)
"""

