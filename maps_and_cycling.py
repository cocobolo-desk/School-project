import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import geo_classes as gc  # My project classes
mpl.use('TkAgg')


def read_json(filename):
    """Reads a json-file and returns the data as a nested dictionary."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
    except FileNotFoundError:
        print('The file does not exist.')
        return None
    except PermissionError:
        print('The user does not have permission to read the file.')
        return None
    except Exception as error:
        print(error)
        return None
    return data_dict


def create_instances(data_dict):
    """Creates a list of Path instances from a nested dictionary. A new
    instance of the class Path is created with coordinates, name and
    True/False whether it is bicycle-friendly."""
    list_instances = []
    for feature in data_dict['features']:
        if feature['geometry']['type'] == 'LineString' \
                and 'highway' in feature['properties'].keys():  # If it's a path

            is_bike_friendly = check_friendliness(feature)
            coordinates = feature['geometry']['coordinates']
            if 'name' in feature['properties'].keys():
                name = feature['properties']['name']
            else:
                name = 'Unknown'
            list_instances.append(gc.Path(coordinates, name, is_bike_friendly))
    return list_instances


def check_friendliness(feature):
    """Checks if a path is bike-friendly given a dictionary for a path."""
    for obj_property in feature['properties'].keys():
        if obj_property == 'bicycle':
            return True
        elif obj_property in ['cycleway', 'cycleway:left', 'cycleway:right', 'cycleway:both'] \
                and feature['properties'][obj_property] != 'no':
            return True
        elif obj_property == 'highway' \
                and feature['properties'][obj_property] == 'cycleway':
            return True
    return False


def get_pdf_name(filename):
    """Returns the name for the pdf given the filename for the samples."""
    filename_split = filename.split('.')
    if len(filename_split) != 2:
        raise NameError('The filename has multiple dots.')
    pdf_name = filename_split[0] + '.pdf'
    return pdf_name


def plot_paths(list_instances, pdf_name):
    """Plots the paths where red paths are bike-friendly and saves it in a pdf-file."""
    for path in list_instances:
        if not isinstance(path, gc.Path):
            continue
        x = []
        y = []
        for segment in path.points:
            x.append(segment.longitude)
            y.append(segment.latitude)

        if path.bicycle_friendly:
            plt.plot(x, y, color="red")
        else:
            plt.plot(x, y, color="black")
    plt.axis('off')
    plt.savefig(pdf_name)


def sum_path_lengths(list_instances):
    """Iterates through all Path instances, and adds their length to
    the total as well as the bicycle friendly length if bicycle-friendly."""
    total_length = 0
    bicycle_length = 0
    for path in list_instances:
        if not isinstance(path, gc.Path):
            continue
        total_length += gc.Path.path_length(path)
        if path.bicycle_friendly:
            bicycle_length += gc.Path.path_length(path)
    return total_length, bicycle_length


def print_lengths(total_length, bicycle_length):
    """Prints the calculated lengths and the share of bike-friendly lengths"""
    print(f'\nTotal street/road/path length: {round(total_length, 2)} km')
    print(f'Bicycle friendly length: {round(bicycle_length, 2)} km')
    print(f'Share: {round(100 * bicycle_length / total_length, 1)} %')


def main():
    data_dict = None
    while not data_dict:
        filename = input('Which file would you like to read? ')
        data_dict = read_json(filename)

    # Creates a list of Path instances
    list_instances = create_instances(data_dict)
    total_length, bicycle_length = sum_path_lengths(list_instances)
    print_lengths(total_length, bicycle_length)
    pdf_name = get_pdf_name(filename)
    plot_paths(list_instances, pdf_name)


if __name__ == '__main__':
    main()
