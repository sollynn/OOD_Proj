import time

class Guest:
    def __init__(self, channel: str, customer_num: int):
        self.channel = channel.upper() #customer channel
        self.customer_num = int(customer_num) #customer amount for each channel

    


class Room:
    def __init__(self, room_id: int, guest: Guest | None):
        self.room_id = int(room_id)
        self.guest = guest  


# ---------- AVL (key = room_id) ----------
class Node:
    def __init__(self, key: int, val: Room):
        self.key = key # Room_ID
        self.val = val # Room
        self.left = None
        self.right = None
        self.h = 1


def _h(n): return n.h if n else 0 # check height
def _bal(n): return _h(n.left) - _h(n.right) if n else 0 # Check Balance Tree


class AVL:
    def __init__(self):
        self.root = None

    def insert(self, room: Room):
        self.root = self._insert(self.root, room.room_id, room)

    def _insert(self, n, k, v):
        if not n:
            return Node(k, v)
        if k < n.key:
            n.left = self._insert(n.left, k, v)
        elif k > n.key:
            n.right = self._insert(n.right, k, v)
        else:
            n.val = v
            return n
        n.h = 1 + max(_h(n.left), _h(n.right)) #Update height
        return self._rebalance(n, k)

    def find(self, room_id: int):
        n = self.root
        while n:
            if room_id == n.key:
                return n.val
            n = n.left if room_id < n.key else n.right
        return None

    def delete(self, room_id: int):
        self.root = self._delete(self.root, room_id)

    def _min(self, n):
        while n.left:
            n = n.left
        return n

    def _delete(self, n, k):
        if not n:
            return None
        if k < n.key:
            n.left = self._delete(n.left, k)
        elif k > n.key:
            n.right = self._delete(n.right, k)
        else:
            if not n.left:
                return n.right
            if not n.right:
                return n.left
            t = self._min(n.right)
            n.key, n.val = t.key, t.val
            n.right = self._delete(n.right, t.key)
        n.h = 1 + max(_h(n.left), _h(n.right))
        return self._rebalance_full(n)

    def inorder(self):
        def dfs(n):
            if not n:
                return
            yield from dfs(n.left)
            yield n.val
            yield from dfs(n.right)
        yield from dfs(self.root)

    # rotations + rebalance
    def _rotL(self, z):
        y, T2 = z.right, z.right.left
        y.left, z.right = z, T2
        z.h = 1 + max(_h(z.left), _h(z.right))
        y.h = 1 + max(_h(y.left), _h(y.right))
        return y

    def _rotR(self, z):
        y, T3 = z.left, z.left.right
        y.right, z.left = z, T3
        z.h = 1 + max(_h(z.left), _h(z.right))
        y.h = 1 + max(_h(y.left), _h(y.right))
        return y

    def _rebalance(self, n, inserted_key):
        b = _bal(n)
        if b > 1 and inserted_key < n.left.key:
            return self._rotR(n)
        if b < -1 and inserted_key > n.right.key:
            return self._rotL(n)
        if b > 1 and inserted_key > n.left.key:
            n.left = self._rotL(n.left)
            return self._rotR(n)
        if b < -1 and inserted_key < n.right.key:
            n.right = self._rotR(n.right)
            return self._rotL(n)
        return n

    def _rebalance_full(self, n):
        b = _bal(n)
        if b > 1 and _bal(n.left) >= 0:
            return self._rotR(n)
        if b > 1 and _bal(n.left) < 0:
            n.left = self._rotL(n.left)
            return self._rotR(n)
        if b < -1 and _bal(n.right) <= 0:
            return self._rotL(n)
        if b < -1 and _bal(n.right) > 0:
            n.right = self._rotR(n.right)
            return self._rotL(n)
        return n


# ---------- Channel registry ----------
class manageCustomer:
    def __init__(self):
        self.counts: dict[str, int] = {}

    def add_batch(self, mapping: dict[str, int]):
        for ch, n in mapping.items():
            if n < 0:
                raise ValueError("count must be >= 0")
            ch = ch.upper()
            self.counts[ch] = self.counts.get(ch, 0) + n

    def total(self) -> int:
        return sum(self.counts.values())

    def sorted_channels(self):
        return sorted(self.counts.keys())

    def __repr__(self):
        return f"{dict(sorted(self.counts.items()))}"


# ---------- Interleaver (A1,B1,...,A2,B2,...) ----------
class HilbertInterleaver:
    @staticmethod
    def assign(reg: manageCustomer, need: int, start_room: int = 1):
        chs = reg.sorted_channels()
        if not chs:
            return
        max_per_ch = max(reg.counts.values())
        room = start_room
        made = 0
        for i in range(max_per_ch):        # ลำดับลูกค้าในแต่ละช่องทาง
            for ch in chs:                 # วนตามลำดับช่องทาง
                if i < reg.counts[ch]:
                    g = Guest(ch, i + 1)
                    yield Room(room, g)
                    room += 1
                    made += 1
                    if made >= need:
                        return


# ---------- Repository (File I/O) ----------
class manageFile:
    def __init__(self, filename="hotel_data.txt"):
        self.filename = filename

    def load(self):
        reg, rooms = manageCustomer(), []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                first = f.readline().strip()
                if first.startswith("Channels:"):
                    raw = first[len("Channels:"):].strip()
                    pairs = [p for p in raw.split(",") if p.strip()]
                    m = {}
                    for p in pairs:
                        if "=" in p:
                            ch, c = p.split("=")
                            m[ch.strip()] = int(c.strip())
                    reg.add_batch(m)

                next(f, None)  # skip header
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    ch, cust, room = line.split("\t")
                    guest = Guest(ch, int(cust))
                    rooms.append(Room(int(room), guest))
        except FileNotFoundError:
            pass
        return reg, rooms

    def save(self, reg: manageCustomer, rooms: list[Room]):
        with open(self.filename, "w", encoding="utf-8") as f:
            chs = ",".join(f"{ch}={reg.counts[ch]}" for ch in reg.sorted_channels())
            f.write(f"Channels: {chs}\n")
            f.write("Channel\tCustomerNum\tRoomID\n")
            for r in sorted(rooms, key=lambda x: x.room_id):
                if r.guest:
                    f.write(f"{r.guest.channel}\t{r.guest.customer_num}\t{r.room_id}\n")
                else:
                    f.write(f"-\t-\t{r.room_id}\n")


# ---------- Application Facade ----------
class recievedCommand:
    def __init__(self, repo=None):
        self.repo = repo or manageFile()
        self.registry, existing_rooms = self.repo.load()
        self.rooms = AVL()
        for r in existing_rooms:
            self.rooms.insert(r)

    @staticmethod
    def parse_add(s: str):
        # รูปแบบ: "50/ A10 B15 D5"
        if "/" not in s:
            raise ValueError("expected 'N/ A10 B15'")
        left, right = s.split("/", 1)
        left = left.strip()
        if not left.isdigit():
            raise ValueError("N must be int")
        need = int(left)
        mm = {}
        for tok in right.replace(",", " ").split():
            ch = "".join(filter(str.isalpha, tok)).upper()
            num = "".join(filter(str.isdigit, tok))
            if not ch or not num:
                raise ValueError(f"bad token '{tok}'")
            mm[ch] = mm.get(ch, 0) + int(num)
        return need, mm

    def cmd_add(self, arg: str):
        need, newmap = self.parse_add(arg)
        total_x = sum(newmap.values())
        if need != total_x:
            print(f"Error: N ({need}) does not match the sum of X values ({total_x})")
            return
        print(f"Before: {self.registry}")
        self.registry.add_batch(newmap)
        print(f"After : {self.registry}")

        # rebuild rooms by interleave
        existing_count = len(list(self.rooms.inorder()))
        self.rooms = AVL()
        assigned = list(HilbertInterleaver.assign(self.registry, need=self.registry.total()))
        for r in assigned:
            self.rooms.insert(r)
        rooms_after = len(list(self.rooms.inorder()))

        self.repo.save(self.registry, list(self.rooms.inorder()))
        print(f"Assigned {len(assigned)} / requested {need} (total guests={self.registry.total()})")
        print("Pattern: A1,B1,D1,A2,B2,D2,...")

    def cmd_addroom(self, room_id: int):
        if self.rooms.find(room_id):
            print(f"Room {room_id} exists.")
            return
        self.rooms.insert(Room(room_id, None))
        self.repo.save(self.registry, list(self.rooms.inorder()))
        print(f"Room {room_id} added.")

    def cmd_delete(self, room_id: int):
        if not self.rooms.find(room_id):
            print(f"Room {room_id} not found.")
            return
        self.rooms.delete(room_id)
        self.repo.save(self.registry, list(self.rooms.inorder()))
        print(f"Room {room_id} deleted.")

    def cmd_find(self, room_id: int):
        r = self.rooms.find(room_id)
        if r and r.guest:
            g = r.guest
            print(f"Room {room_id} → Channel {g.channel}, Customer {g.customer_num}")
        elif r:
            print(f"Room {room_id} is empty.")
        else:
            print("Room not found.")

    def cmd_show(self):
        any_data = False
        for r in self.rooms.inorder():
            any_data = True
            if r.guest:
                print(f"{r.guest.channel}\t{r.guest.customer_num}\t{r.room_id}")
            else:
                print(f"-\t-\t{r.room_id}")
        if not any_data:
            print("No data.")

    def cmd_show_file(self):
        self.repo.save(self.registry, list(self.rooms.inorder()))
        print(f"Saved to {self.repo.filename}")


# ---------- mini CLI (รันทันที) ----------
svc = recievedCommand()
print("\n--- Hotel Command ---")
print("add N/ A10 B5 ... | addroom ID | delete ID | find ID | show | show_file | exit\n")

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
            svc.cmd_add(arg)
        elif cmd == "addroom":
            svc.cmd_addroom(int(arg))
        elif cmd == "delete":
            svc.cmd_delete(int(arg))
        elif cmd == "find":
            svc.cmd_find(int(arg))
        elif cmd == "show":
            svc.cmd_show()
        elif cmd == "show_file":
            svc.cmd_show_file()
        else:
            print("unknown command:", cmd)

        print(f"\nRun time : {time.time() - t0:.6f} s\n")
    except Exception as e:
        print("error:", e)
