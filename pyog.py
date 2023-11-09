# -*- coding: utf-8 -*-
import json
import socket
import struct
import time

OG_FLAG_KEYS = {
    0: "shift_key",
    1: "ctrl_key",
    13: "show_turbo",
    14: "prefer_km",  # false means miles
    15: "prefer_bar",  # false means PSI
}

DL_FLAG_KEYS = {
    0: "shift_light",
    1: "full_beam",
    2: "handbrake",
    3: "pit_speed_limiter",
    4: "tc",
    5: "signal_left",
    6: "signal_right",
    7: "signal_any",
    8: "oil_warning",
    9: "battery_warning",
    10: "abs",
    11: "spare",
}


def create_socket(ip: str, port: int) -> socket.socket:
    """
    Creates a UDP server socket to connect to OutGauge

    Parameters
    ----------
    ip : str
        The IP Address to connect to (probably 127.0.0.1)
    port : int
        The port to connect on (probably 2222)

    Returns
    -------
    sock : socket.socket
        The socket to use for getting data
    """
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.bind((ip, port))

    return sock


def parse_flags(flag_data: int, flag_keys: dict[int, str]) -> dict[str, bool]:
    """
    Parses flags into their respective booleans

    Parameters
    ----------
    flag_data : int
        The flag data straight from unpacking the UDP data
    flag_keys : dict[int, str]
        The flag keys in a dict with the key as the index of the bit with the flag
        and the value being the key for that item in the resultant dict

    Returns
    -------
    result : dict[str, str]
        The dict for all of the information in this set of flags
    """
    result = dict()
    for key in flag_keys:
        # Getting the name of this flag from the dict
        result_key = flag_keys[key]

        if flag_data & (2**key):
            result[result_key] = True
        else:
            result[result_key] = False

    return result


def read_outgauge_data(sock: socket.socket, buffer_size: int = 256) -> dict:
    """
    Reads the data from the socket and returns a dict with all of the information
    from the OutGauge packet.
    See: https://documentation.beamng.com/modding/protocols/#outgauge-udp-protocol

    Parameters
    ----------
    sock : socket.socket
        The socket to read data off of
    buffer_size : int
        The size of the buffer to read from the socket

    Returns
    -------
    parsed_data : dict
        The data nicely formatted into a dict
    """
    raw_data = sock.recvfrom(buffer_size)
    data = struct.unpack("I4sHbbfffffffIIfff16s16sxxxx", raw_data[0])
    return {
        "time": data[0],
        "car": data[1].decode("utf-8"),
        "flags": parse_flags(data[2], OG_FLAG_KEYS),
        "gear": data[3],
        "plid": data[4],
        "speed": data[5],
        "rpm": data[6],
        "turbo": data[7],
        "eng_temp": data[8],
        "fuel": data[9],
        "oil_pressure": data[10],
        "oil_temp": data[11],
        "dash_lights": parse_flags(data[12], DL_FLAG_KEYS),
        "show_lights": parse_flags(data[13], DL_FLAG_KEYS),
        "throttle": data[14],
        "brake": data[15],
        "clutch": data[16],
        "display1": data[17].decode("utf-8"),
        "display2": data[18].decode("utf-8"),
    }


def read_motionsim_data(sock: socket.socket, buffer_size: int = 256) -> dict:
    """
    Reads the data from the socket and returns a dict with all of the information
    from the MotionSim packet.
    See: https://documentation.beamng.com/modding/protocols/#motionsim-udp-protocol

    Parameters
    ----------
    sock : socket.socket
        The socket to read data off of
    buffer_size : int
        The size of the buffer to read from the socket

    Returns
    -------
    parsed_data : dict
        The data nicely formatted into a dict
    """
    raw_data = sock.recvfrom(buffer_size)
    data = struct.unpack("4sfffffffffffffffffffff", raw_data[0][:88])
    return {
        "magic": data[0].decode("utf-8"),
        "pos_x": data[1],
        "pos_y": data[2],
        "pos_z": data[3],
        "vel_x": data[4],
        "vel_y": data[5],
        "vel_z": data[6],
        "acc_x": data[7],
        "acc_y": data[8],
        "acc_z": data[9],
        "up_vel_x": data[10],
        "up_vel_y": data[11],
        "up_vel_z": data[12],
        "roll_pos": data[13],
        "pitch_pos": data[14],
        "yaw_pos": data[15],
        "roll_rate": data[16],
        "pitch_rate": data[17],
        "yaw_rate": data[18],
        "roll_acc": data[19],
        "pitch_acc": data[20],
        "yaw_acc": data[21],
    }


def main():
    """
    Sample test program which will simply output data until you press Ctrl+C
    """
    IP = "127.0.0.1"
    PORT = 4444

    with create_socket(IP, PORT) as sock:
        while True:
            print(json.dumps(read_outgauge_data(sock)))


if __name__ == "__main__":
    main()
