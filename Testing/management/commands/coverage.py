#!/usr/bin/env python3
from typing import Any, List
import subprocess
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help: str = 'Run tests and return tests coverage analysis'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--app', type=str, help='The App to test')

    def handle(self, *args: Any, **kwargs: Any) -> None:
        print('Starts the tests coverage compute')
        cmds: List[str] = [
            'coverage run manage.py test',
            'coverage html',
        ]
        if 'app' in kwargs and kwargs['app'] is not None:
            cmds[0] += ' ' + kwargs['app']
        for cmd in cmds:
            print(cmd)
            subprocess.run(cmd.split(' '))
        print('Done')
