from pymavlink import mavutil

import send_ekf
import request_ekf

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("from_mav", help="device uri for the receiver mav")
    parser.add_argument("to_mav", help="device uri for the mav to get the data")
    parser.add_argument("--baud-from", type=int, default=115200, help="baud rate, default: 115200")
    parser.add_argument("--baud-to", type=int, default=115200, help="baud rate, default: 115200")

    args = parser.parse_args()

    mav_from = mavutil.mavlink_connection(args.from_mav, baud=args.baud_from)
    mav_to = mavutil.mavlink_connection(args.to_mav, baud=args.baud_to)

    data = request_ekf.request_data(mav_from)

    for i in range(len(data)):
        send_ekf.send_data(mav_to, data[i], i)
