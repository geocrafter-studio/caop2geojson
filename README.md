# CAOP exporter (caop2geojson)

Small Python utility for exporting Portuguese [CAOP]('http://www.dgterritorio.pt/cartografia_e_geodesia/cartografia/carta_administrativa_oficial_de_portugal__caop_/caop_em_vigor/').

## Install
Setup a virtual environment and install dependencies

`pip install -r app-requirements.txt`

## Usage

### Export into single file

`python execute.py --source /path/to/my/caop.shp --output /path/to/my/caop.geojson`

### Export a freguesia (parish) per file

`python execute.py --source /path/to/my/caop.shp --group /path/to/my/group_root`

**Important**: In this mode, individual freguesias are grouped by district code folders. (Portuguese administrative code DICOFRE)

### Options

```
usage: caop2geojson [-h] [-v] [--source SOURCE] [-s_srs S_SRS]
                    [-s_format S_FORMAT] [--output OUTPUT] [-o_srs O_SRS]
                    [-o_format O_FORMAT] [--query QUERY] [--group GROUP]
                    [--overwrite]
```

```
optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --source SOURCE, -s SOURCE
                        Path to source file for conversion
  -s_srs S_SRS          Source reference system (EPSG:3763)
  -s_format S_FORMAT    Source file format using OGR definition (ESRI
                        Shapefile)
  --output OUTPUT, -o OUTPUT
                        Path to output the converted file
  -o_srs O_SRS          Output reference system (EPSG:4326)
  -o_format O_FORMAT    Output file format using OGR definition (GeoJSON)

query:
  --query QUERY, -q QUERY
                        WIP: Query the source file for DICOFRE with a k:v
                        list. (Example: ['DICOFRE:100301', 'DICOFRE:180101]'
  --group GROUP, -g GROUP
                        Path to where to group individual parishes by
                        district. (Example: /path/to/mycaop'

options:
  --overwrite           Overwrite existing files on export.
```

## Contact

If you need further assistance please contact [info[at]geocrafter.eu](info@geocrafter.eu)

## License

caop2geojson is Free and Open Source sofware and is licensed under the Simplified BSD License.