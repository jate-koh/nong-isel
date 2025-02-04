import datetime
import os
import json

from termcolor import colored
from constants import default_configs, default_path


def log(message, type, json_data=None, module=None):
    get_logger(module).log(message, type, json_data=json_data, record=True)


def get_logger(module=None):
    if module is None:
        return Logger(module=None)
    else:
        return Logger(module=module)


class Logger:
    def __init__(self, module=None):
        self.tz = datetime.timezone(datetime.timedelta(hours=default_configs()["gmt"]))
        self.path = os.path.join(
            os.getcwd(),
            default_path()["logs_dir"],
        )
        self.debug_path = os.path.join(
            os.getcwd(),
            default_path()["debugs_dir"],
        )
        if module is None:
            self.module = ""
        else:
            self.module = module

    def log(self, message, type, json_data=None, record=True):
        match type:
            case "info":
                self.info(message, json_data=json_data, record=record)
            case "warn":
                self.warn(message, json_data=json_data, record=record)
            case "error":
                self.error(message, json_data=json_data, record=record)
            case _:
                print(f"{datetime.datetime.now(tz=self.tz)} {type.upper()}: {message}")

    def format_time(self):
        return colored(
            datetime.datetime.now(tz=self.tz).strftime("%d-%m-%Y %H:%M:%S"), "dark_grey"
        )

    def format_module(self, module):
        if module is not None:
            return colored(f" [{module}]", "light_magenta")
        return ""

    def format_message(self, message):
        return colored(f" {message}", "light_grey")

    def format_object(self, json_data):
        return json.dumps(json_data, indent=2)

    def info(self, message, json_data=None, record=True):
        buff = self.format_time() + colored(" INFO", "light_blue", attrs=["bold"])
        if self.module is not None:
            buff += self.format_module(self.module)
        buff += self.format_message(message)
        if json_data is not None:
            # Newline
            buff += "\n" + self.format_object(json_data)
        print(buff)

        if record:
            self.write(message)
        if json_data is not None:
            self.write(json_data)

    def warn(self, message, json_data=None, record=True):
        buff = self.format_time() + colored(" WARN", "yellow", attrs=["bold"])
        if self.module is not None:
            buff += self.format_module(self.module)
        buff += self.format_message(message)
        if json_data is not None:
            buff += "\n" + self.format_object(json_data)
        print(buff)

        if record:
            self.write(message)
        if json_data is not None:
            self.write(json_data)

    def error(self, message, json_data=None, record=True):
        buff = self.format_time() + colored(" ERROR", "red", attrs=["bold"])
        if self.module is not None:
            buff += self.format_module(self.module)
        buff += self.format_message(message)
        if json_data is not None:
            buff += "\n" + self.format_object(json_data)
        print(buff)

        if record:
            self.write(message)
        if json_data is not None:
            self.write(json_data)

    def debug(self, message, json_data=None, record=True):
        buff = self.format_time() + colored(" DEBUG", "light_green", attrs=["bold"])
        if self.module is not None:
            buff += self.format_module(self.module)
        buff += self.format_message(message)
        if json_data is not None:
            buff += "\n" + self.format_object(json_data)
        print(buff)

        if record:
            self.write(message, debug_log=True)
        if json_data is not None:
            self.write(json_data, debug_log=True)

    def write(self, message, debug_log=False):
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                f.write("")
            f.close()
        if not os.path.exists(self.debug_path):
            with open(self.debug_path, "w", encoding="utf-8") as f:
                f.write("")
            f.close()

        if debug_log:
            with open(self.debug_path, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.datetime.now(tz=self.tz)}]; {message}\n")
            f.close()
            return

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now(tz=self.tz)}]; {message}\n")
        f.close()
