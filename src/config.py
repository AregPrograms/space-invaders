from time import time
from pypresence import Presence

client_id = "1033573115118235699"
RPC = Presence(client_id)
RPC.connect()

FRAMERATE        = 60
ENEMY_SPAWN_RATE = 100 # In frames, 60fps
START_UNIX_TIME  = time()