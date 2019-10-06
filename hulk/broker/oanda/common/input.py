from __future__ import print_function

import getpass
import sys

try:
    input_func = raw_input  # python 2
except NameError:
    input_func = input  # python 3


def get_string(prompt, default=None):
    prompt = "{}{}: ".format(
        prompt,
        "" if default is None else " [{}]".format(default)
    )

    value = None

    while value is None or len(value) == 0:
        try:
            value = input_func(prompt) or default
        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except:
            pass

    return value


def get_password(prompt):
    while True:
        try:
            password = getpass.getpass("{}: ".format(prompt))
            if len(password) > 0:
                return password
        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except:
            pass


def get_yn(prompt, default=True):
    choice = None

    choices = "[yn]"

    if default is True:
        choices = choices.replace("y", "Y")
    elif default is False:
        choices = choices.replace("n", "N")

    prompt = "{} {}: ".format(
        prompt,
        choices
    )

    while choice is None:
        try:
            s = input_func(prompt)

            if len(s) == 0 and default is not None:
                return default

            if len(s) > 1:
                continue

            s = s.lower()

            if s == "y":
                return True

            if s == "n":
                return False

        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except:
            pass


def get_from_list(choices, title, prompt, default=0):
    choice = None

    prompt = "{}{}: ".format(
        prompt,
        "" if default is None else " [{}]".format(default)
    )

    if title is not None:
        print(title)

    for i, c in enumerate(choices):
        print("[{}] {}".format(i, c))

    while choice is None:
        try:
            s = input_func(prompt) or default

            i = int(s)

            if 0 <= i < len(choices):
                choice = choices[i]
        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except:
            pass

    return choice
