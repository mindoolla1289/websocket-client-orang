import asyncio
from websockets.sync.client import connect
import websockets
import json
import time
import os
from loguru import logger

# log_loc = f'{os.path.dirname(__file__)}/logs/controller.log'
# logger.add(log_loc, format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
#            level='INFO', rotation='5:00', backtrace=True, colorize=True)
# logger.info('System started !!!')

# настройки пульса
PULSE = 5
HiLev = 0.075
LowLev = 0.075
PulCost = 10

OBJECT_ID = ""

msg = {"msg_t":"connecting","payload":{
        "id":OBJECT_ID
    }}

msg = json.dumps(msg)
msg2 = {"msg_t":"connecting","payload":{"id":OBJECT_ID}}

async def main():
    logger.info("ws-client started")
    while True:
        try:
            
            async with websockets.client.connect("ws://") as websocket:
                logger.info("Connected to the server")
                await websocket.send(msg)
                logger.info("Send message with id to server")

                while True:
                    data = await  websocket.recv()

                    logger.info("There is new message from server")
                    logger.info(data)
                    data = json.loads(data)
                    try:
                        if data["msg_t"] == 'pay':
                            payload = data['payload']
                            amount = int(payload['amount'])

                            msg22 = {"msg_t":"confirmed", "payload":{"id_payment":payload["id_payment"]}}

                            await websocket.send(json.dumps(msg22))
                            logger.info("Send confirm message to the server")

                            await pay(amount)
                        elif data["msg_t"] == 'test_pay':
                            logger.info("There is new message from server:Test-pay")
                        elif data["msg_t"] == 'update':
                            logger.info("There is new message from server:Update")
                            logger.info("But I'm orange client!")
                        

                    except websockets.ConnectionClosed:
                        continue
        except:
            logger.warning("Disconnected, there some problem with network")
            time.sleep(3)
            continue




async def pay(amount):

    for _ in range(amount//PulCost):
        logger.info("in pulss pulss")
        os.system(f'gpio write {PULSE} 1')
        time.sleep(HiLev)
        os.system(f'gpio write {PULSE} 0')
        time.sleep(LowLev)
    os.system(f'gpio write {PULSE} 0')


    

if __name__=="__main__":
    asyncio.run(main())