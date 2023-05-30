from pymavlink import mavutil
import time
import random

import logging 
import sys 

logger = logging.getLogger(__name__)

def send_data(mav, data, core):
    """
    Send one core of data at a time
    :param mav: mavlink connection
    :param data: data to send (array of size 24)
    :param core: core index to send
    """

    logger.debug("waiting for heartbeat")

     # wait for a hearbeat to know we are connected
    mav.wait_heartbeat()

    logger.debug("got heartbeat")

    logger.info("sending message")
    # access mav message
    mav.mav.debug_float_array_send(
        int(time.time() * 1e6),
        b"data",
        core,
        data=data
    )

    logger.info("message sent")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="udp:localhost:14550", help="device uri; default: udp:localhost:14550")
    parser.add_argument("--baud", type=int, default=115200, help="baud rate, default: 115200")

    args = parser.parse_args()

    mav = mavutil.mavlink_connection(args.device, baud=args.baud)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


    logger.info("making random data")
    data = [random.random() for i in range(58)]

    send_data(mav, data, 0)

