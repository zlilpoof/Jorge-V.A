from playsound import playsound
import os
def bip():
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    bip_mp3 = os.path.join(parent_dir, "..", "bip.mp3")
    playsound(bip_mp3)