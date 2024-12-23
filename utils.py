import os


def read_message_txt(dict: bool = False):
    if os.path.exists("message_id.txt"):
        with open("message_id.txt", "r") as f:
            string = f.read()
            f.close()
        if dict:
            if not string:
                return {
                    "message_id": None,
                    "channel_id": None,
                    "current_role_num": None,
                }
            return {
                "message_id": [
                    int(string.split("\n")[0].split(",")[i])
                    for i in range(len(string.split("\n")[0].split(",")))
                ],
                "channel_id": int(string.split("\n")[1]),
                "current_role_num": int(string.split("\n")[2]),
            }
        else:
            if not string:
                return (None, None, None)
            return (
                [
                    int(string.split("\n")[0].split(",")[i])
                    for i in range(len(string.split("\n")[0].split(",")))
                ],
                int(string.split("\n")[1]),
                int(string.split("\n")[2]),
            )
    else:
        return (None, None, None)
