# -*- coding: utf-8 -*-

"""
Small utility to convert Portuguese CAOP features to other geospatial data formats

Feedback, ideas, bugs....whatever please contact info@geocrafter.eu

2017 Geocrafter - Geospatial Studio
"""

import argparse
from src.caop2geojson import CAOP2GeoJSON

__author__ = "Geocrafter - Geospatial Studio"
__email__ = "info@geocrafter.eu"
__date__ = "November 2017"
__version__ = "0.1.0"


def execute(args):
    caop = CAOP2GeoJSON()
    caop.src_file = args.source
    caop.src_epsg = args.s_srs
    caop.src_format = args.s_format
    caop.dest_file = args.output
    caop.dest_epsg = args.o_srs
    caop.dest_format = args.o_format
    caop.overwrite = args.overwrite

    source = caop.read()

    if len(args.query) == 0 and args.group == "":
        caop.export_all(source=source)
    # TODO: add query option
    else:
        caop.export_groupby(source=source, destination=args.group)


def main():
    utility = argparse.ArgumentParser(prog="caop2geojson",
                                      description="Tool for CAOP export to other geospatial formats",
                                      version=__version__)

    # Source definition
    utility.add_argument('--source', '-s', help='Path to source file for conversion')
    utility.add_argument('-s_srs', help='Source reference system (EPSG:3763)', default='EPSG:3763')
    utility.add_argument('-s_format', help='Source file format using OGR definition (ESRI Shapefile)',
                         default='ESRI Shapefile')
    # Target definition
    utility.add_argument('--output', '-o', help='Path to output the converted file')
    utility.add_argument('-o_srs', help='Output reference system (EPSG:4326)', default='EPSG:4326')
    utility.add_argument('-o_format', help='Output file format using OGR definition (GeoJSON)',
                         default='GeoJSON')
    # Query definition
    query = utility.add_argument_group('query')
    query.add_argument('--query', '-q', help="WIP: Query the source file for DICOFRE with a k:v list. "
                                             "(Example: ['DICOFRE:100301', 'DICOFRE:100301]' ", type=list,
                       default=[])
    query.add_argument('--group', '-g', help="Path to where to group individual parishes by district. "
                                             "(Example: /path/to/mycaop' ", action='store', default="")

    # Other Option
    options = utility.add_argument_group('options')
    options.add_argument('--overwrite', help='Overwrite existing files on export.', action='store_true',
                         default=False)

    return utility.parse_args()


if __name__ == "__main__":
    args = main()
    execute(args)