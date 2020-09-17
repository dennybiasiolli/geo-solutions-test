# -*- coding: utf-8 -*-
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from geo.models import Coordinate


class Command(BaseCommand):
    help = """
Imports coordinates from CSV file

Use with
`python manage.py geo_import_coordinates_from_csv -f file_path`
"""

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, required=True,
                            help='path of csv file to import')
        parser.add_argument('--delete', action='store_true', required=False,
                            help='force overwrite of existent records')
        parser.add_argument('--delete-all', action='store_true', required=False,
                            help='force overwrite of all existent records')

    def handle(self, *args, **options):
        try:
            f = open(options['file'], encoding='utf-8')
            reader = csv.reader(f, delimiter=';')
        except:
            raise CommandError('Wrong "file" parameter')

        if options['delete_all']:
            Coordinate.objects.all().delete()

        headers = None
        for line in reader:
            if headers == None:
                headers = line
            else:
                if options['delete']:
                    Coordinate.objects.filter(id_orig=line[0]).delete()
                print(line)
                c = Coordinate(
                    id_orig=int(line[0]),
                    x=float(line[1]),
                    y=float(line[2]),
                )
                try:
                    c.save()
                except IntegrityError:
                    raise CommandError((
                        'Coordinate with id_orig {0} already exists.\n'
                        '\t- use --delete to remove imported coordinates\n'
                        '\t- use --delete-all to remove all coordinates before import'
                    ).format(c.id_orig))
        self.stdout.write('Coordinates import completed')
        f.close()
