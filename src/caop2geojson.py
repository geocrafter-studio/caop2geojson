# -*- coding: utf-8 -*-

"""
Small utility to convert Portuguese CAOP features to different formats

Feedback, ideas, bugs....whatever please contact:
info@geocrafter.eu

2017 Geocrafter - Geospatial Studio
"""

import fiona
from pyproj import Proj, transform
from os import path
from sys import stdout

from utils import mkgroupdir, progressbar, removefile


class CAOP2GeoJSON(object):
    def __init__(self):
        self.src_epsg = "EPSG:3763"  # PTTM06
        self.dest_epsg = "EPSG:4326"  # WGS84
        self.src_file = "caop.shp"  # source shapefile
        self.src_format = "ESRI Shapefile"
        self.dest_file = "caop.geojson"  # output file
        self.dest_format = "GeoJSON"  # output format
        self.src_proj = Proj(init=self.src_epsg)
        self.dest_proj = Proj(init=self.dest_epsg)
        self.overwrite = False
        self.ext = ''

    def read(self):
        return fiona.open(path=self.src_file, mode='r', driver=self.src_format, crs=self.src_epsg, encoding='latin1')

    def export_all(self, source):
        schema = source.schema.copy()
        pbar = progressbar(len(source))
        print "Starting to export %s feature(s)..." % pbar.total
        self.export_file(source=source, target=self.dest_file, schema=schema, pbar=pbar)
        pbar.close()
        stdout.flush()
        print "Successfully exported %s feature(s)!" % pbar.total

    def export_groupby(self, source, destination):
        schema = source.schema.copy()
        pbar = progressbar(len(source))
        print "Collection info for %s feature(s)..." % pbar.total
        if self.dest_format == 'GeoJSON':
            self.ext = '.geojson'
        dico = []
        dico_field = self.get_dico_field(schema=schema)
        for ft in source:
            if ft['properties'][dico_field] not in dico:
                d = ft['properties'][dico_field][0:2]
                f = ft['properties'][dico_field]
                mkgroupdir(destination, d)
                self.export_file(source=None, target=path.join(destination, d, f + self.ext), schema=schema,
                                 pbar=pbar, group=True, feature=ft, dicolist=dico, diconame=dico_field)
                dico.append(f)
        source.close()
        pbar.close()
        stdout.flush()
        print "Successfully exported %s feature(s)!" % pbar.total

    def export_file(self, source, target, schema, pbar, group=False, feature=None, dicolist=None, diconame=None):
        if self.overwrite:
            removefile(target)
        with fiona.open(path=target, mode='w', schema=schema, driver=self.dest_format,
                        crs=self.dest_epsg, encoding='UTF-8') as output:
            if group:
                source = self.read()
            for ft in source:
                if group:
                    if ft['properties'][diconame] not in dicolist:
                        if ft['properties'][diconame] == feature['properties'][diconame]:
                            tf = self.transform_feature(feature=ft, orig_proj=self.src_proj, dest_proj=self.dest_proj)
                            output.write(tf)
                            pbar.update()
                else:
                    tf = self.transform_feature(feature=ft, orig_proj=self.src_proj, dest_proj=self.dest_proj)
                    output.write(tf)
                    pbar.update()
            if group:
                source.close()

    @staticmethod
    def transform_feature(feature, orig_proj, dest_proj):
        out_lr = []
        for p in feature['geometry']['coordinates'][0]:
            orig_x, orig_y = p
            proj_x, proj_y = transform(orig_proj, dest_proj, orig_x, orig_y)
            out_lr.append((proj_x, proj_y))
        feature['geometry']['coordinates'] = [out_lr]
        return feature

    @staticmethod
    def get_dico_field(schema):
        try:
            schema['properties']['Dicofre']
            return 'Dicofre'
        except KeyError:
            return 'DICOFRE'
