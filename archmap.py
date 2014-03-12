#!/usr/bin/env python3

from urllib.request import urlopen
from geojson import Feature, Point, FeatureCollection, dumps
from geojsonio import to_geojsonio


def get_users():
    """This funtion parses users from the ArchWiki and writes it to users.txt"""

    # Open and decode the ArchWiki page containing the list of users.
    wiki = urlopen("https://wiki.archlinux.org/index.php/ArchMap/List")

    wiki_source = wiki.read().decode()

    # Grab the user data between the second set of <pre> tags.
    wiki_text_start = wiki_source.find('<pre>', wiki_source.find('<pre>') + 1) + 6
    wiki_text_end = wiki_source.find('</pre>', wiki_source.find('</pre>') + 1) - 1
    wiki_text = wiki_source[wiki_text_start:wiki_text_end]

    # Write the user data (wiki_text) to users.txt and close the file.
    wiki_output = open(output_file_users, 'w')
    wiki_output.write(wiki_text)
    wiki_output.close()


def make_geojson(geojsonio):
    """This function reads users.txt and outputs output.geojson"""

    # Open files and initialize a list for the geojson features.
    users = open(output_file_users, 'r')
    output = open(output_file_geojson, 'w')

    geo_output = []

    # Loop over the lines in users.txt and assign each element a variable.
    for line in users:
        elements = line.split('"')

        coords = elements[0].strip(' ')
        coords = coords.split(',')
        latitude = float(coords[0])
        longitude = float(coords[1])
        name = elements[1].strip()
        comment = elements[2].strip()
        comment = comment[2:]

        # Generate a geojson point feature for the entry and add it to geo_output.
        point = Point((longitude, latitude))
        feature = Feature(geometry=point, properties={"Comment": comment, "Name": name})

        geo_output.append(feature)

    # Pass the feature collection to geo_output_str.
    geo_output_str = (dumps(FeatureCollection(geo_output)))

    if geojsonio is True:
        # Send the geojson to geojson.io via a GitHub gist.
        to_geojsonio(geo_output_str)

    else:
        # Make geo_output_str look pretty.
        geo_output_str = geo_output_str.replace('"features": [', '"features": [\n')
        geo_output_str = geo_output_str.replace('}}, ', '}},\n')
        geo_output_str = geo_output_str.replace('}}]', '}}\n]')

    # Write geo_output_str to output.geojson.
    output.write(geo_output_str)

    # Close users.txt and output.geojson.
    users.close()
    output.close()


# If the script is being run and not imported, get_users() and make_geojson().
if __name__ == "__main__":
    from argparse import ArgumentParser
    from configparser import ConfigParser

    # Define and parse arguments.
    parser = ArgumentParser()
    parser.add_argument("--config", metavar="FILE",
                        help="Use an alternative configuration file instead of /etc/archmp.conf")
    parser.add_argument("--geojsonio", action="store_true",
                        help="Send the geojson to http://geojson.io for processing")
    args = parser.parse_args()

    # Test if arguments have been called, then conditionally set variables.
    if args.config:
        config_file = args.config
    else:
        config_file = '/etc/archmap.conf'

    if args.geojsonio:
        geojsonio = True
    else:
        geojsonio = False

    config = ConfigParser()
    config.read(config_file)
    output_file_geojson = config['files']['geojson']
    output_file_users = config['files']['users']

    get_users()
    make_geojson(geojsonio)
