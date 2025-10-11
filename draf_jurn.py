import time, sys    

class Node:
    def __init__(self,customer_num,channel, ID = None, left =None , right =None):
        self.customer_num = customer_num
        self.channel = channel
        self.roomID = self.ID(customer_num,channel) if ID is None else ID
        self.left =None if left is None else left
        self.right =None if right is None else right
        self.height = 1


    def ID(self, customer_num, channel):
        if not channel.isalpha():
            return f'error: channel must be letters A-Z'

        ch = channel.upper()
        code = 0
        for c in ch:
            code = code * 26 + (ord(c) - ord('A') + 1)

        try:
            num = int(customer_num)
        except ValueError:
            return f'error: customer_num must be number'

        if num < 1:
            return f'error: customer_num must be positive'

        self.channel = ch
        self.customer_num = num
        self.ID = code * 1_000_000 + num

        return self.ID


class AVL :
    def __init__(self):
        self.root = None

    def insert(self, node):
        if self.root is None:
            self.root = node
        else:
            self.root = self._insert(self.root, node)

    def _insert(self, current, node):
        if current is None:
            return node

        if node.roomID < current.roomID:
            current.left = self._insert(current.left, node)
        else:
            current.right = self._insert(current.right, node)

        current.height = 1 + max(self._get_height(current.left), self._get_height(current.right))

        balance = self._get_balance(current)

        # Left Left
        if balance > 1 and node.roomID < current.left.roomID:
            return self._right_rotate(current)

        # Right Right
        if balance < -1 and node.roomID > current.right.roomID:
            return self._left_rotate(current)

        # Left Right
        if balance > 1 and node.roomID > current.left.roomID:
            current.left = self._left_rotate(current.left)
            return self._right_rotate(current)

        # Right Left
        if balance < -1 and node.roomID < current.right.roomID:
            current.right = self._right_rotate(current.right)
            return self._left_rotate(current)

        return current

    def _get_height(self, node):
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def print_tree(self):
        """Print the tree structure"""
        self._print_tree(self.root, 0)

    def _print_tree(self, node, level):
        if node is not None:
            self._print_tree(node.left, level + 1)
            print(' ' * 4 * level + f'-> {node.roomID}')
            self._print_tree(node.right, level + 1)

    def display_all_nodes(self):
        """Display information of all nodes in inorder traversal"""
        print("All rooms in the hotel:")
        self._display_all_nodes(self.root)

    def _display_all_nodes(self, node):
        if node is not None:
            self._display_all_nodes(node.left)
            print(f"Customer Num: {node.customer_num}, Channel: {node.channel}, RoomID: {node.roomID}")
            self._display_all_nodes(node.right)

    def show_tree_and_nodes(self):
        """Draw the tree and then display all node information"""
        print("Tree Structure:")
        self.print_tree()
        print("\n" + "="*50 + "\n")
        self.display_all_nodes()

    def find_room(self, room_id):
        # Find a room by its ID in the AVL tree
        return self._find_room(self.root, room_id)

    def _find_room(self, node, room_id):
        if node is None:
            return None
        if room_id == node.roomID:
            return node
        elif room_id < node.roomID:
            return self._find_room(node.left, room_id)
        else:
            return self._find_room(node.right, room_id)

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, room_id):
        self.root = self._delete(self.root, room_id)

    def _delete(self, node, room_id):
        if node is None:
            return node

        if room_id < node.roomID:
            node.left = self._delete(node.left, room_id)
        elif room_id > node.roomID:
            node.right = self._delete(node.right, room_id)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: Get the inorder successor
            temp = self._min_value_node(node.right)
            node.roomID = temp.roomID
            node.customer_num = temp.customer_num
            node.channel = temp.channel
            # Delete the inorder successor
            node.right = self._delete(node.right, temp.roomID)

        if node is None:
            return node

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Get the balance factor
        balance = self._get_balance(node)

        # Balance the tree
        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

hotel = AVL()

print("\n--- Hotel Command ---\n" \
    "\nadd : Manual add customer" \
    "\naddroom : Manual add room" \
    "\ndelete : Manual delete room" \
    "\nfind : Search room by number" \
    "\nshow : show customer data" \
    "\nshow_file : show customer data in file\n" \
    "\n---------------------\n")

while True:
    command = input("enter command : ").strip()
    
    if not command:
        continue

    if command.lower() in ("exit", "quit"):
        print("Exiting program...")
        break

    start_time = time.time()    # start counting time

    parts = command.split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if cmd == "add":
            # รูปแบบ: add 50/ A10 M15 RU15 LOP14 KP6
            # 50 = guest_amount, ตัวอักษร = ชื่อช่องทาง (เก็บเป็น set), ตัวเลข = จำนวนแขกของช่องทางนั้น

            if "/" not in args:
                print("error: expected 'guest_amount/ channels', e.g. 50/ A10 M15")
                continue

            left, right = args.split("/", 1)
            left, right = left.strip(), right.strip()
            
            if not left.isdigit():
                print("error: guest_amount must be an integer")
                continue

            guest_amount = int(left)

            # แปลงรายการช่องทาง: รองรับเว้นวรรคหรือคอมมา
            raw_tokens = [t.strip() for t in right.replace(",", " ").split() if t.strip()]
            if not raw_tokens:
                print("error: no input channels provided")
                continue

            # โครงสร้างเก็บข้อมูล
            if not hasattr(hotel, "channel_count"):
                hotel.channel_count = {}
            if not hasattr(hotel, "channels"):
                hotel.channels = set()

            # นับจำนวนแขกต่อช่องทาง + เก็บชื่อช่องทางใน set
            temp_counts = {}
            for tok in raw_tokens:
                ch = ''.join(filter(str.isalpha, tok)).upper()
                num = ''.join(filter(str.isdigit, tok))
                if not ch or not num:
                    print(f"error: invalid token '{tok}', expected like A10 or RU15")
                    continue
                hotel.channels.add(ch)
                temp_counts[ch] = temp_counts.get(ch, 0) + int(num)

            # อัปเดต dict หลัก
            hotel.channel_count = temp_counts

            # เพิ่มตัวแปรจำนวนช่องทาง
            channel_amount = len(hotel.channels)

            # รีบิลด์ AVL ใหม่ โดยจำกัดจำนวนตาม guest_amount
            hotel.root = None
            print("\nRebuilding hotel room assignments...")

            inserted = 0
            for ch, total in hotel.channel_count.items():
                for i in range(1, total + 1):
                    if inserted >= guest_amount:
                        break
                    new_node = Node(str(i), ch)
                    hotel.insert(new_node)
                    inserted += 1
                if inserted >= guest_amount:
                    break

            print(f"\nGuests requested: {guest_amount}, assigned: {inserted}")
            print("Channels:", sorted(hotel.channels))
            print(f"Total channels: {channel_amount}")   
            print("\nUpdated all room assignments successfully.\n")


    elif cmd == "addroom":
        if not args.strip().isdigit():
            print("error: room ID must be a number")
        else:
            room_id = int(args.strip())
            # Check if room already exists before inserting
            if hotel.find_room(room_id) is not None:
                print(f"Error: Room with ID {room_id} already exists. Skipping insertion.")
            else:
                new_node = Node(None, None, ID=room_id)
                hotel.insert(new_node)
                print(f"Room {room_id} added successfully")

    elif cmd == "delete":
        if not args.strip().isdigit():
            print("error: room ID must be a number")
        else:
            room_id = int(args.strip())
            if hotel.find_room(room_id) is None:
                print(f"Error: Room with ID {room_id} does not exist.")
            else:
                hotel.delete(room_id)
                print(f"Room {room_id} deleted successfully")

    elif cmd == "find": 
        if not args.strip().isdigit():
            print("error: room ID must be a number")
        else:
            room_id = int(args.strip())
            result = hotel.find_room(room_id)
            if result:
                print(f"Room found → Channel: {result.channel}, Customer Num: {result.customer_num}, Room ID: {result.roomID}")
            else:
                print("Room not found.")

    elif cmd == "show":
        start_time = time.time()
        if hotel.root is None:
            print("No data in the hotel.")
        else:
            hotel.display_all_nodes()

    elif cmd == "show_file":
        if hotel.root is None:
            print("No customer data in the hotel.")
        else:
            filename = "hotel_data.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("Channel\tCustomerNum\tRoomID\n")

                def inorder_write(node):
                    if node:
                        inorder_write(node.left)
                        if node.channel and node.customer_num:
                            f.write(f"{node.channel}\t{node.customer_num}\t{node.roomID}\n")
                            print(f"Channel {node.channel:<3} | Customer {node.customer_num:<3} → Room {node.roomID}")
                        inorder_write(node.right)

                inorder_write(hotel.root)

            print(f"\nOutput saved to '{filename}' successfully.")

    else:
        print("error command arai wa:", cmd)

     # counting time
    elapsed = time.time() - start_time
    print(f"\nRun time : {elapsed:.8f} seconds\n")    
    
"""
input pattern : add A1,A2,B1,B2 (channel=char,customer_num=int, seperate by ,)
input pattern : addRoom 00
input pattern : delete 001 ( Room wanna delete)
input pattern : find 001 ( Room wanna search)
"""