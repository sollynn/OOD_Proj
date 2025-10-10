# Use Node to store both customer and room information
# Only Add function is implemented
# # Line 117 - 143 for debugging and visualization
class Node:
    def __init__(self,customer_num,channel, ID = None, left =None , right =None):
        self.customer_num = customer_num
        self.channel = channel
        self.roomID = self.ID(customer_num,channel) if ID is None else ID
        self.left =None if left is None else left
        self.right =None if right is None else right
        self.height = 1


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
        print("All nodes in the tree:")
        self._display_all_nodes(self.root)
        print("")
    def _display_all_nodes(self, node):
        if node is not None:
            self._display_all_nodes(node.left)
            print(f"Customer Num: {node.customer_num}, Channel: {node.channel}, RoomID: {node.roomID}, Height: {node.height}")
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
            new_node = Node(num, ch)
            # Check if room already exists before inserting
            if hotel.find_room(new_node.roomID) is not None:
                print(f"Error: Room with ID {new_node.roomID} already exists. Skipping insertion.")
            else:
                hotel.insert(new_node)
                print(f"Added customer: Channel {ch}, Num {num}, RoomID {new_node.roomID}")

        pass
    
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
        pass

    elif cmd == "showcustomerdata":
        pass

    else:
        print("error command arai wa:", cmd)
    
"""
input pattern : add A1,A2,B1,B2 (channel=char,customer_num=int, seperate by ,)
input pattern : addRoom 00
input pattern : delete 001 ( Room wanna delete)
input pattern : find 001 ( Room wanna search)
"""
