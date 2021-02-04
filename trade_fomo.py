stoploss = 30 # Percentage that you are willing to lose

import config
import entry_exit_condition
import get_minute
import get_position
import pencil_wick
import binance_futures
from datetime import datetime
from termcolor import colored

def stoploss():
    position_info = get_position.get_position_info()
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("LONG", stoploss)
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit_condition.EXIT_LONG(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("SHORT", stoploss)
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit_condition.EXIT_SHORT(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()

        if entry_exit_condition.ENTER_LONG(one_minute, five_minute):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if config.live_trade: binance_futures.open_position("LONG")

        elif entry_exit_condition.ENTER_SHORT(one_minute, five_minute):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if config.live_trade: binance_futures.open_position("SHORT")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def no_stoploss():
    position_info = get_position.get_position_info()
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        if entry_exit_condition.EXIT_LONG(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if entry_exit_condition.EXIT_SHORT(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if entry_exit_condition.ENTER_LONG(one_minute, five_minute):
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
            if config.live_trade: binance_futures.open_position("LONG")

        elif entry_exit_condition.ENTER_SHORT(one_minute, five_minute):
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
            if config.live_trade: binance_futures.open_position("SHORT")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

