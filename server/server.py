#!/bin/python3
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from colorama import Fore, init
from time import sleep
import serverdictctl
import configctl
import logging
import asyncio
import socket
import sys


init(autoreset=True)
serverdict_file = serverdictctl.ServerDict('ServerDictionary.json')
config_file = configctl.Config('ServerConfig.json')
config = config_file.load()
class ColorFormatter(logging.Formatter):
    fmt = config['logfmt']

    FORMATS = {
        logging.DEBUG: Fore.GREEN + fmt + Fore.RESET,
        logging.INFO: Fore.WHITE + fmt + Fore.RESET,
        logging.WARNING: Fore.YELLOW + fmt + Fore.RESET,
        logging.ERROR: Fore.RED + fmt + Fore.RESET,
        logging.CRITICAL: Fore.BLUE + fmt + Fore.RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger('Server')
ch = logging.StreamHandler()
eval(f'logger.setLevel(logging.{config["logLevel"]})')
eval(f'ch.setLevel(logging.{config["logLevel"]})')
ch.setFormatter(ColorFormatter())
logger.addHandler(ch)

async def recvall(client, loop):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = (await loop.sock_recv(client, BUFF_SIZE))
        data += part
        if len(part) < BUFF_SIZE and data:
            # either 0 or end of data
            break
    return data


# Get RSA-Crypt connection
async def handle_client(client):
    loop = asyncio.get_event_loop()

    private_server_key = RSA.generate(2048)
    if (await recvall(client, loop)).decode() == 'GET_SPUB':
        await loop.sock_sendall(client, private_server_key.public_key().export_key())
        if (await recvall(client, loop)).decode() == 'PUB_OK':
            await loop.sock_sendall(client, 'GET_CPUB'.encode())
            try:
                public_client_key = RSA.import_key(await recvall(client, loop))
                await loop.sock_sendall(client, 'PUB_OK'.encode())
            except:
                client.close()
                loop.stop()

    cipher_Enc = PKCS1_OAEP.new(public_client_key)
    cipher_Dec = PKCS1_OAEP.new(private_server_key)

    async def send(msg: bytes) -> None:
        await loop.sock_sendall(client, cipher_Enc.encrypt(msg))
    
    async def recv() -> bytes:
        return bytes(cipher_Dec.decrypt(await recvall(client, loop)))
    
    def split_data(data):
        data_list = []
        while data != b'':
            data_list.append(data[:214])
            data = data[214:]
        return len(data_list), data_list

    if (await recv()).decode() == 'START':
        logger.info('Client connected!')
        await send('WHOIS'.encode())
        username = (await recv()).decode()
        config = config_file.load()
        if username in config['users']:
            await send('OK'.encode())
            if (await recv()).decode() == config['users'][username]:
                logger.debug(f'Client authorized: {username}/{config["users"][username]}')
                await send('OK'.encode())
                mode = (await recv()).decode()
                logger.info(f'Client mode: {mode}')
                if mode == 'SENDING':
                    await send('OK'.encode())
                    parts = []
                    for _ in range(int((await recv()).decode())):
                        await send('OK'.encode())
                        parts.append(await recv())
                    pickled_dict = b''
                    for part in parts:
                        pickled_dict += part    
                    serverdict_file.dump(pickled_dict)
                elif mode == 'RECEIVING':
                    data = serverdict_file.load()
                    data_len, data_list = split_data(data)
                    await send(str(data_len).encode())
                    print(data_len)
                    for part in data_list:
                        if (await recv()).decode() == 'OK':
                            await send(part)

    client.close()


async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 45652))
    server.listen(80)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(handle_client(client))


if __name__ == '__main__':
    logger.info('Started!')
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.critical('Exit!')
        sys.exit(0)
