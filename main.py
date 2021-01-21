#!/usr/bin/python

# My modules
from bbox import BBox
from shrun import shrun        
from time import sleep
proc = shrun('xdotool search "Yu-Gi-Oh! DUEL LINKS"', capture_output=True)
WID = proc.stdout.decode().strip()

bboxes = BBox.readAll()

shrun("xdotool windowactivate --sync {}".format(WID))
shrun("xdotool windowmove --sync {} 0 0".format(WID))

import bboxes as bs

def error_handle():
    bs.ERROR.click()
    bs.START_GAME.waitAndClick()
    bs.NOTIFICATIONS.waitAndClick()
    sleep(10)
    bs.AOTDS.waitAndClick()

def lottery():
    while True:
        try:
            exc_waitAndClick(bs.DRAW_10)
        except Exception:
            error_handle
            bs.CARD_LOTTERY.waitAndClick()

def exc_waitAndClick(bbox):
    while not bbox.compare():
        if bs.ERROR.compare():
            raise Exception()
    bbox.click()

def auto_duel_procedure():
    exc_waitAndClick(bs.AUTO_DUEL)
    exc_waitAndClick(bs.DUEL_END)
    exc_waitAndClick(bs.DUEL_RESULT)
    sleep(2)
    exc_waitAndClick(bs.DUEL_RESULT)
    exc_waitAndClick(bs.MISSION_CIRCUIT_GRAY_OK)
    exc_waitAndClick(bs.MISSION_CIRCUIT_BLUE_OK)

def main():
    while True:
        try:
            if bs.ERROR.compare():
                raise Exception()

            if bs.AUTO_DUEL.compare():
                auto_duel_procedure()

            # bs.AOTDC_DICE.compareAndClick()
            # if bs.SUPPORT_ITEMS.compare():
            #     bs.SUPPORT_ITEMS.click()
            #     BBox.EMPTY_CLICK_ENABLED = False
            #     exc_waitAndClick(bs.USE_SUPPORT_ITEM)
            #     sleep(8)
            #     BBox.EMPTY_CLICK_ENABLED = True
            #     # auto_duel_procedure()
            #     continue

            bs.SKIP_STORY.compareAndClick()
            bs.TREASURE_ROOM_CONFIRM.compareAndClick()
            bs.LEVEL_SELECTION.compareAndClick()
        except Exception:
            error_handle()
# main()
# print(bs.AOTDC_DICE.compare())
lottery()
