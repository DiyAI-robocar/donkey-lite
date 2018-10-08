import sys
import os
import socket
import shutil
import argparse

import pytest

import source as dk
from source.management.tub import TubManager


TEMPLATES_PATH = "./templates/"


def make_dir(path):
    real_path = os.path.expanduser(path)
    print('making dir ', real_path)
    if not os.path.exists(real_path):
        os.makedirs(real_path)
    return real_path


def load_config(config_path):

    """
    load a config from the given path
    """
    conf = os.path.expanduser(config_path)

    if not os.path.exists(conf):
        print("No config file at location: %s. Add --config to specify\
                location or run from dir containing config.py." % conf)
        return None

    try:
        cfg = dk.load_config(conf)
    except:
        print("Exception while loading config from", conf)
        return None

    return cfg


class BaseCommand():
    pass


class CreateCar(BaseCommand):

    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(prog='createcar', usage='%(prog)s [options]')
        parser.add_argument('--path', default=None, help='path where to create car folder')

        parsed_args = parser.parse_args(args)
        return parsed_args

    def run(self, args):
        args = self.parse_args(args)
        self.create_car(path=args.path)

    @staticmethod
    def create_car(path='~/mycar'):
        """
        This script sets up the folder struction for donkey to work.
        It must run without donkey installed so that people installing with
        docker can build the folder structure for docker to mount to.
        """

        print("Creating car folder: {}".format(path))
        path = make_dir(path)

        print("Creating data & model folders.")
        folders = ['models', 'data', 'logs']
        folder_paths = [os.path.join(path, f) for f in folders]
        for fp in folder_paths:
            make_dir(fp)

        #add car application and config files if they don't exist
        app_template_path = os.path.join(TEMPLATES_PATH, 'donkey2.py')
        config_template_path = os.path.join(TEMPLATES_PATH, 'config_defaults.py')
        car_app_path = os.path.join(path, 'manage.py')
        car_config_path = os.path.join(path, 'config.py')

        if os.path.exists(car_app_path):
            print('Car app already exists. Delete it and rerun createcar to replace.')
        else:
            print("Copying car application template: {}".format("donkey2"))
            shutil.copyfile(app_template_path, car_app_path)

        if os.path.exists(car_config_path):
            print('Car config already exists. Delete it and rerun createcar to replace.')
        else:
            print("Copying car config defaults. Adjust these before starting your car.")
            shutil.copyfile(config_template_path, car_config_path)

        print("Donkey setup complete.")


class FindCar(BaseCommand):

    @staticmethod
    def parse_args(args):
        pass

    @staticmethod
    def run(args):
        print('Looking up your computer IP address...')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        print('Your IP address: %s ' %s.getsockname()[0])
        s.close()

        print("Finding your car's IP address...")
        cmd = "sudo nmap -sP " + ip + "/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'"
        print("Your car's ip address is:" )
        os.system(cmd)


class CalibrateCar(BaseCommand):

    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(prog='calibrate', usage='%(prog)s [options]')
        parser.add_argument('--channel', help='The channel youd like to calibrate [0-15]')
        parsed_args = parser.parse_args(args)
        return parsed_args

    def run(self, args):
        from source.parts.actuator import PCA9685

        args = self.parse_args(args)
        channel = int(args.channel)
        c = PCA9685(channel)

        for i in range(10):
            pmw = int(input('Enter a PWM setting to test(0-1500)'))
            c.run(pmw)


class RunTests(BaseCommand):

    @staticmethod
    def parse_args(args):
        parser = argparse.ArgumentParser(prog='runtests', usage='%(prog)s [options]')
        parser.add_argument('--location', help='path to tests or path to file')
        parsed_args = parser.parse_args(args)
        return parsed_args

    def run(self, args):
        """
        run all tests
        """
        args = self.parse_args(args)
        pytest.main(['-x', args.location])


def execute_from_command_line():
    """
    This is the function linked to the "donkey" terminal command.
    """
    commands = {
        'createcar': CreateCar,
        'findcar': FindCar,
        'calibrate': CalibrateCar,
        'tubclean': TubManager,
        'runtests': RunTests,
    }

    args = sys.argv[:]
    command_text = args[1]

    if command_text in commands.keys():
        command = commands[command_text]
        c = command()
        c.run(args[2:])
    else:
        dk.util.proc.eprint('Usage: The available commands are:')
        dk.util.proc.eprint(list(commands.keys()))


if __name__ == "__main__":
    execute_from_command_line()
