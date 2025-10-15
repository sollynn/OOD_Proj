import time
import sys # for memory calculation

# ---------- Data Models ----------
class Guest:
    def __init__(self, channel: str, customer_num: int):
        self.channel = channel.upper()  # customer channel
        self.customer_num = int(customer_num)  # customer amount for each channel
        

class Room:
    def __init__(self, room_id: int, guest: Guest | None, status = 'NEW'):
        self.room_id = int(room_id)
        self.guest = guest
        self.status = status

# ---------- AVL Tree Implementation (key = room_id) ----------
class AVLNode:
    def __init__(self, key: int, val: Room):
        self.key = key  # Room_ID
        self.val = val  # Room
        self.left = None
        self.right = None
        self.height = 1


def get_height(node):
    return node.height if node else 0


def get_balance_factor(node):
    return get_height(node.left) - get_height(node.right) if node else 0


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, room: Room):
        self.root = self.insert_node(self.root, room.room_id, room)

    def insert_node(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self.insert_node(node.left, key, value)
        elif key > node.key:
            node.right = self.insert_node(node.right, key, value)
        else:
            node.val = value
            return node
        node.height = 1 + max(get_height(node.left), get_height(node.right))  # Update height
        return self.rebalance_after_insert(node, key)

    def find(self, room_id: int):
        node = self.root
        while node:
            if room_id == node.key:
                return node.val
            node = node.left if room_id < node.key else node.right
        return None

    def delete(self, room_id: int):
        self.root = self.delete_node(self.root, room_id)

    def find_minimum(self, node):
        while node.left:
            node = node.left
        return node

    def delete_node(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self.delete_node(node.left, key)
        elif key > node.key:
            node.right = self.delete_node(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            temp = self.find_minimum(node.right)
            node.key, node.val = temp.key, temp.val
            node.right = self.delete_node(node.right, temp.key)
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        return self.rebalance_after_delete(node)

    def inorder_traversal(self):
        def dfs(node):
            if not node:
                return
            yield from dfs(node.left)
            yield node.val
            yield from dfs(node.right)
        yield from dfs(self.root)

    # Rotations and rebalancing
    def rotate_left(self, z):
        y, T2 = z.right, z.right.left
        y.left, z.right = z, T2
        z.height = 1 + max(get_height(z.left), get_height(z.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        return y

    def rotate_right(self, z):
        y, T3 = z.left, z.left.right
        y.right, z.left = z, T3
        z.height = 1 + max(get_height(z.left), get_height(z.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))
        return y

    def rebalance_after_insert(self, node, inserted_key):
        balance = get_balance_factor(node)
        if balance > 1 and inserted_key < node.left.key:
            return self.rotate_right(node)
        if balance < -1 and inserted_key > node.right.key:
            return self.rotate_left(node)
        if balance > 1 and inserted_key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and inserted_key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def rebalance_after_delete(self, node):
        balance = get_balance_factor(node)
        if balance > 1 and get_balance_factor(node.left) >= 0:
            return self.rotate_right(node)
        if balance > 1 and get_balance_factor(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and get_balance_factor(node.right) <= 0:
            return self.rotate_left(node)
        if balance < -1 and get_balance_factor(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node


# ---------- Customer Registry ----------
class CustomerRegistry:
    def __init__(self):
        self.counts: dict[str, int] = {}

    def add_customers(self, mapping: dict[str, int]):
        
        for channel, count in mapping.items():
            if count < 0:
                raise ValueError("count must be >= 0")
            channel = channel.upper()
            self.counts[channel] = self.counts.get(channel, 0) + count

    def get_total_customers(self) -> int:
        return sum(self.counts.values())

    def get_sorted_channels(self):
        return sorted(self.counts.keys())

    def __repr__(self):
        return f"{dict(sorted(self.counts.items()))}"


# ---------- Room Assigner ----------
class HilbertInterleaver:
    @staticmethod
    def assign_rooms(registry: CustomerRegistry, need: int, start_room: int = 1):
        channels = registry.get_sorted_channels()
        if not channels:
            return
        total_channels = len(channels)
        assigned = 0

        for i in range(max(registry.counts.values())):
            for idx, channel in enumerate(channels):
                if i < registry.counts[channel]:
                    room_id = start_room + (total_channels * i) + idx
                    guest = Guest(channel, i + 1)
                    yield Room(room_id, guest)
                    assigned += 1
                    if assigned >= need:
                        return


# ---------- File I/O ----------
class ManageFile:
    def __init__(self, filename="hotel_data.txt"):
        self.filename = filename

    def load_data(self):
        registry, rooms = CustomerRegistry(), []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                first = f.readline().strip()
                if first.startswith("Channels:"):
                    raw = first[len("Channels:"):].strip()
                    pairs = [p for p in raw.split(",") if p.strip()]
                    mapping = {}
                    for p in pairs:
                        if "=" in p:
                            channel, count = p.split("=")
                            mapping[channel.strip()] = int(count.strip())
                    registry.add_customers(mapping)

                next(f, None)  # skip header
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    channel, customer_num, room_id, status = line.split("\t")
                    if channel == "-":
                        rooms.append(Room(int(room_id), None, status))
                    else:
                        guest = Guest(channel, int(customer_num))
                        rooms.append(Room(int(room_id), guest, status))
        except FileNotFoundError:
            pass
        return registry, rooms

    def save_data(self, registry: CustomerRegistry, rooms: list[Room]):
        with open(self.filename, "w", encoding="utf-8") as f:
            channels = ",".join(f"{ch}={registry.counts[ch]}" for ch in registry.get_sorted_channels())
            f.write(f"Channels: {channels}\n")
            f.write("Channel\tCustomerNum\tRoomID\tStatus\n")
            for room in sorted(rooms, key=lambda x: x.room_id):
                if room.guest:
                    f.write(f"{room.guest.channel}\t{room.guest.customer_num}\t{room.room_id}\t{room.status}\n")
                else:
                    f.write(f"-\t-\t{room.room_id}\t{room.status}\n")


# ---------- Main Method ----------
class HotelCommandHandler:
    def __init__(self, repo=None):
        self.repo = repo or ManageFile()
        self.registry, existing_rooms = self.repo.load_data()
        self.rooms = AVLTree()
        for room in existing_rooms:
            self.rooms.insert(room)

    @staticmethod
    def parse_add_command(command: str):
        # รูปแบบ: "50/ A10 B15 D5"
        if "/" not in command:
            raise ValueError("expected 'N/ A10 B15'")
        left, right = command.split("/", 1)
        left = left.strip()
        if not left.isdigit():
            raise ValueError("N must be int")
        need = int(left)
        mapping = {}
        for token in right.replace(",", " ").split():
            channel = "".join(filter(str.isalpha, token)).upper()
            num = "".join(filter(str.isdigit, token))
            if not channel or not num:
                raise ValueError(f"bad token '{token}'")
            mapping[channel] = mapping.get(channel, 0) + int(num)
        return need, mapping

    def add_customers(self, arg: str):
        need, new_mapping = self.parse_add_command(arg)
        total_new = sum(new_mapping.values())
        if need != total_new:
            print(f"Error: N ({need}) does not match the sum of X values ({total_new})")
            return
        print(f"Before: {self.registry}")
        for room in self.rooms.inorder_traversal():
            room.status = 'OLD'

        self.registry.add_customers(new_mapping)
        print(f"After : {self.registry}")

        # Assign new rooms for new customers
        max_room = max((room.room_id for room in self.rooms.inorder_traversal()), default=0)
        temp_registry = CustomerRegistry()
        temp_registry.add_customers(new_mapping)
        new_assigned = list(HilbertInterleaver.assign_rooms(temp_registry, need=total_new, start_room=max_room + 1))
        for room in new_assigned:
            room.status = 'NEW'
            if not self.rooms.find(room.room_id):
                self.rooms.insert(room)

        self.repo.save_data(self.registry, list(self.rooms.inorder_traversal()))
        print(f"Assigned {len(new_assigned)} / requested {need} (total guests={self.registry.get_total_customers()})")
        
    def add_manual_room(self, room_id):
        try:
            num = self.registry.counts["MANUAL"]+1
        except:
            num = 1
        new_room = Room(room_id, Guest("Manual", num), 'NEW')
        if self.rooms.find(new_room.room_id):
            print(f"Room {new_room.room_id} already exists.")
            return False
        for r in self.rooms.inorder_traversal():
            r.status = 'OLD'
        self.rooms.insert(new_room)
        print(f"Before: {self.registry}")
        try:
            val = self.registry.counts["MANUAL"]
            self.registry.add_customers({"MANUAL":1})
        except:
            self.registry.add_customers({"MANUAL":1})
        
        self.repo.save_data(self.registry, list(self.rooms.inorder_traversal()))
        print(f"After : {self.registry}")
        print(f"Room {new_room.room_id} added manually.")
        return True
        

    def delete_room(self, room_id: int):
        if not self.rooms.find(room_id):
            print(f"Room {room_id} not found.")
            return
        self.rooms.delete(room_id)
        self.repo.save_data(self.registry, list(self.rooms.inorder_traversal()))
        print(f"Room {room_id} deleted.")

    def find_room(self, room_id: int):
        room = self.rooms.find(room_id)
        if room and room.guest:
            guest = room.guest
            print(f"Room {room_id} → Channel {guest.channel}, Customer {guest.customer_num}")
        elif room:
            print(f"Room {room_id} is empty.")
        else:
            print("Room not found.")

    def show_rooms(self):
        any_data = False
        for room in self.rooms.inorder_traversal():
            any_data = True
            if room.guest:
                print(f"{room.guest.channel}\t{room.guest.customer_num}\t{room.room_id}")
            else:
                print(f"-\t-\t{room.room_id}")
        if not any_data:
            print("No data.")

    def save_to_file(self):
        self.repo.save_data(self.registry, list(self.rooms.inorder_traversal()))
        print(f"Saved to {self.repo.filename}")

    def reset(self):
        self.registry = CustomerRegistry()  
        self.rooms = AVLTree()  
        self.repo.save_data(self.registry, [])
        print("All data wiped.")

    @staticmethod
    def get_deep_size(obj, seen=None):
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0  # กัน Infinite recursion
        seen.add(obj_id)
        size = sys.getsizeof(obj)
        if hasattr(obj, '__dict__'):
            # สำหรับ Object ที่มี __dict__
            size += sum(HotelCommandHandler.get_deep_size(v, seen) for v in obj.__dict__.values())
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
            # สำหรับ Object ที่เป็น iterable (เช่น list, dict, set)
            try:
                size += sum(HotelCommandHandler.get_deep_size(item, seen) for item in obj)
            except TypeError:
                pass  # ข้ามถ้าไม่สามารถ iterate ได้
        return size

    def display_memory_usage(self):
        # Memory for CustomerRegistry (dict of counts)
        registry_size = self.get_deep_size(self.registry)
    
        # Memory for AVLTree (traverse nodes)
        tree_size = 0
        for room in self.rooms.inorder_traversal():
            tree_size += self.get_deep_size(room)
    
        total_size = registry_size + tree_size
    
        print(f"Memory Usage:")
        print(f"  CustomerRegistry (Dict): {registry_size} bytes")
        print(f"  AVLTree (Rooms): {tree_size} bytes")
        print(f"  Total Data: {total_size} bytes")


# ---------- Mini CLI (รันทันที) ----------

service = HotelCommandHandler()
print("\n--- Hotel Command ---")
print("add N/ A10 B5 ... | delete ID | find ID | show | show_file | memory | reset | exit\n")

while True:
    try:
        raw = input("enter command : ").strip()
        if not raw:
            continue
        if raw.lower() in ("exit", "quit"):
            break

        t0 = time.time()
        parts = raw.split(maxsplit=1)
        cmd = parts[0]
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd == "add":
            service.add_customers(arg)
        elif cmd == "delete":
            service.delete_room(int(arg))
        elif cmd == "find":
            service.find_room(int(arg))
        elif cmd == "show":
            service.show_rooms()
        elif cmd == "show_file":
            service.save_to_file()
        elif cmd == "memory":
            service.display_memory_usage()
        elif cmd == "reset":
            service.reset()
        elif cmd == "add_manual":
            service.add_manual_room(int(arg))
        else:
            print("unknown command:", cmd)

        print(f"\nRun time : {time.time() - t0:.6f} s\n")
    except Exception as e:
        print("error:", e)