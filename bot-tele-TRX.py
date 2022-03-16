#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Coded by aqil.almara

# Get your own values from my.telegram.org
api_id = 717425;
api_hash = '322526d2c3350b1d3530de327cf08c07';

#Import Module
import os
import re
import sys
import time
import atexit
import signal
import datetime
try: import telethon
except ModuleNotFoundError:
    __import__("pip").main(["install", "--upgrade", "pip"])
    __import__("pip").main(["install", "telethon"])
from telethon import (
    TelegramClient, sync, events
)
from telethon.tl.types import ReplyInlineMarkup

def console_print(value, color=2, infotype='time'):
    print(f"\r{' '*59}", end="\r\x1b[0;1m");
    if infotype=='time': infotype = datetime.datetime.now().strftime('%H:%M:%S');
    print(f"\r\x1b[0;2;6;30;4{color}m {infotype} \x1b[0;1;3{color}m {value}");

def delay(sec_timer):
    while (time.time()<=sec_timer):
        mins, secs = divmod(sec_timer-time.time(), 60);
        TIMER = f"\x1b[37m{int(mins):02d}\x1b[30m:\x1b[37m{int(secs):02d}";
        print(f"\r \x1b[0;1;36m》\x1b[32mPlease Wait \x1b[30m⟨{TIMER}\x1b[30m⟩ \x1b[32mseconds ☕🚬  \x1b[0;30m", end="");

        try: time.sleep(.3333);
        except KeyboardInterrupt: sys.exit();
        except: pass;

    print(f"\r{' '*59}", end="\r\x1b[0;1m");

class Bot(object):
    """docstring for Bot"""

    TRX_username = "@SmallFaucetTrxFP_bot";
    DGB_username = "@DigiByteFaucetClaimBOT";

    def __init__(self, phone_num, limit=99):
        if not os.path.exists(".ses-SFTFP_bot"):
            os.mkdir(".ses-SFTFP_bot");

        try:
            self.client = TelegramClient(".ses-SFTFP_bot/{}".format(phone_num), api_id, api_hash);
            self.client.start(phone_num);
            me = self.client.get_me();
            self.TRX_entity = self.client.get_entity(self.TRX_username);
            self.DGB_entity = self.client.get_entity(self.DGB_username);
        except Exception as err:
            console_print(err, 1, '[ERROR]');sys.exit();

        signal.signal(signal.SIGTERM, self.disconnect);
        atexit.register(self.disconnect);

        name = f"{me.first_name}{f' {me.last_name}' if me.last_name else ''}" if me.first_name else None;
        print(f"\n \x1b[0;1;30m~ \x1b[32mWelcome Back\x1b[31m: \x1b[37m{name if name else f'({me.username})'}\n");
        self.start(limit);

    def start(self, limit=99):
        try:

            timer = {'Daily':0, 'Claim':0, 'Unlimited':0, 'DGB_entity':0};
            for _ in range(limit):

                if time.time()>=timer['Daily']:
                    self.send_message(self.TRX_entity, "🎉 Daily Giveaway");
                    messages = self.get_messages(self.TRX_username)[0];
                    if "⚠️ Please Wait" in messages.message:
                        timer['Daily'] = time.time();
                        for i, t in enumerate(re.findall(r'([\d.]*\d+)', messages.message)[::-1]):
                            if str(t).isdigit(): timer['Daily'] += int(t)*(60**i);
                    else:
                        self.click(messages, 0);
                        timer['Daily'] = time.time()+86400;

                if time.time()>=timer['Claim']:
                    self.send_message(self.TRX_entity, "💙 Claim Faucet Trx");
                    messages = self.get_messages(self.TRX_username)[0];
                    if "❌ Email Not set" in messages.message:
                        self.send_message(self.TRX_entity, "💼 Set Email");
                        self.click(messages, 0);
                        while True:
                            Email = input("Input Your Faucetpay.io Email: ");
                            if Email:
                                self.send_message(self.TRX_entity, Email);
                                message = self.get_messages(self.TRX_username)[0].message
                                if "Your Faucetpay.io Address Set To" in message:
                                    console_print(message); break;
                        continue;

                    if "⚠️ Please Wait" in messages.message:
                        timer['Claim'] = time.time();
                        for i, t in enumerate(re.findall(r'([\d.]*\d+)', messages.message)[::-1]):
                            if str(t).isdigit(): timer['Claim'] += int(t)*(60**i);
                    else:
                        self.click(messages, 0);
                        timer['Claim'] = time.time()+177;

                if time.time()>=timer['Unlimited']:
                    self.send_message(self.TRX_entity, "😈 Unlimited Faucet");
                    timer['Unlimited'] = time.time()+120;
                    messages = self.get_messages(self.TRX_username, limit=3);
                    if "c7761ee5e3d2bd10f427602774253357dbd2bd4f" in messages[1].message:
                        console_print(messages[1].message.split('\n')[0]);
                    elif "c7761ee5e3d2bd10f427602774253357dbd2bd4f" in messages[0].message:
                        console_print(messages[0].message.split('\n')[0]);
                    elif "c7761ee5e3d2bd10f427602774253357dbd2bd4f" in messages[2].message:
                        console_print(messages[2].message.split('\n')[0]);

                if time.time()>=timer['DGB_entity']:
                    self.send_message(self.DGB_entity, "🆓 FREE Faucet");
                    timer['DGB_entity'] = time.time()+600;
                    console_print(self.get_messages(self.DGB_username)[0].message);

                delay(min(timer.values()));

        except Exception as err:
            console_print(err, 1, '[ERROR]');sys.exit();

    def disconnect(self):
        time.sleep(1);
        self.client.disconnect();

    def send_message(self, channel_entity, message):
        self.client.send_message(
            entity=channel_entity,
            message=message
        );time.sleep(1.25);

    def get_messages(self, channel_username, limit=1):
        time.sleep(1.75);
        return self.client.get_messages(channel_username, limit=limit);

    def click(self, messages, i):
        if hasattr(messages, 'reply_markup') and type(messages.reply_markup) is ReplyInlineMarkup:
            try: messages.click(i);
            except: pass;
        time.sleep(1.25);
        messages = self.get_messages(self.TRX_username, limit=2);
        if "c7761ee5e3d2bd10f427602774253357dbd2bd4f" in messages[1].message:
            console_print(messages[1].message.split('\n')[0]);
        elif "c7761ee5e3d2bd10f427602774253357dbd2bd4f" in messages[0].message:
            console_print(messages[0].message.split('\n')[0]);

if __name__ == '__main__':
    args = sys.argv
    if len(args)==2 and (args[1].startswith('+') or args[1].startswith('0')):
        os.system('clear');Bot(args[1], 9999);
    print("\033[32mUsage: python {} +628...".format(sys.argv[0]));