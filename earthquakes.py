"""
Author: Eliza Black

Credits: 
University of Oregon CIS 210 Project 6 Outline
https://www.kite.com/python/answers/how-to-create-dictionary-keys-from-variables-in-python

Description: Reading, organizing, selecting parts of, and graphing earthquake data in csv files
"""


import csv
from matplotlib import pyplot as plt
import matplotlib.pyplot


#  1. Load the earthquake data from a CSV file and store it in a list of dictionaries
def load_data(file_name: str) -> list:
    """
    Opens and reads the file whose filename is passed as an argument, creates a list of the data
    described in the following steps, and returns it.
    :param file_name: file used to create data list
    :return: eq_data: list containing dictionaries for each row of eq data

    >>> import pprint
    >>> pp = pprint.PrettyPrinter(indent=4)
    >>> eq_data = load_data('earthquakes-2020.csv')
    >>> pp.pprint(eq_data[0:2])
    [   {   'depth': '40.24',
            'depthError': '6.3',
            'dmin': '1.19',
            'gap': '74',
            'horizontalError': '9.4',
            'id': 'us70006t13',
            'latitude': '-5.3245',
            'locationSource': 'us',
            'longitude': '152.5514',
            'mag': '5.1',
            'magError': '0.044',
            'magNst': '171',
            'magSource': 'us',
            'magType': 'mb',
            'net': 'us',
            'nst': '',
            'place': '112 km SSE of Kokopo, Papua New Guinea',
            'rms': '0.79',
            'status': 'reviewed',
            'time': '2020-01-01T00:28:20.289Z',
            'type': 'earthquake',
            'updated': '2020-03-21T17:13:29.040Z'},
        {   'depth': '32.93',
            'depthError': '5.6',
            'dmin': '1.218',
            'gap': '45',
            'horizontalError': '9.9',
            'id': 'us700070sx',
            'latitude': '-5.3373',
            'locationSource': 'us',
            'longitude': '152.6003',
            'mag': '4.6',
            'magError': '0.096',
            'magNst': '32',
            'magSource': 'us',
            'magType': 'mb',
            'net': 'us',
            'nst': '',
            'place': '115 km SSE of Kokopo, Papua New Guinea',
            'rms': '1.08',
            'status': 'reviewed',
            'time': '2020-01-01T00:35:48.020Z',
            'type': 'earthquake',
            'updated': '2020-03-21T17:13:47.040Z'}]
    """
    eq_data = []  # initializing list to be returned
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            eq_data.append(row)  # each row appened to eq_data list
    return eq_data


# 2. Transform the earthquake data
def get_series(raw_data: list, col_name: str, col_type: type) -> list:
    """
    Takes the list created in 1 as the first argument, a column name, and a column type
    (e.g., int, float, str) and returns a single list of values in that column, converted to that type.
    :param raw_data: data from csv file
    :param col_name: name of specific data attribute function finds in file, e.g. magnitude
    :param col_type: type of the data for col_name, e.g. float
    :return: list of the data for col_name

    >>> q_data = load_data('earthquakes-2020.csv')
    >>> magnitude = get_series(load_data('earthquakes-2020.csv'), 'mag', float)
    >>> print(magnitude[:10])
    [5.1, 4.6, 4.5, 4.8, 4.6, 5.0, 5.4, 4.7, 4.6, 4.8]
    """
    data_column = []  # initializing list to be returned
    for row in raw_data:

        # Assigning the key in each dict key value pair (the
        # dictionary inside raw_data) to new variable specific_data
        specific_data = row[col_name]

        # Creating new variable that is specific_data value converted to col_type
        data_correct_type = col_type(specific_data)

        # Appending converted data values to data_column list
        # so the value is saved before new loop iteration occurs
        data_column.append(data_correct_type)

    return data_column


# 3. Summarize the earthquake data
def get_categories(data: list, print_table=True) -> dict:
    """
    Function that will group earthquake magnitudes in light, moderate, major, and strong,
    return data in a dictionary, and print frequency table
    :param data:
    :param print_table:
    :return: dictionary containing the frequencies of the different magnitude levels
    >>> get_categories(get_series(load_data('earthquakes-2020.csv'), 'mag', float))
    Light     : 5057
    Moderate  : 1312
    Major     :  112
    Strong    :    9
    {'light': 5057, 'moderate': 1312, 'major': 112, 'strong': 9}

    >>> get_categories(get_series(load_data('earthquakes-2020.csv'), 'mag', float), False)
    {'light': 5057, 'moderate': 1312, 'major': 112, 'strong': 9}
    """
    # Assigning each value in data (list) to a category based on the size of the number
    light = 0
    moderate = 0
    major = 0
    strong = 0
    for mag in data:
        mag = float(mag)
        if 4.5 <= mag <= 4.9:
            light += 1
        elif 5 <= mag <= 5.9:
            moderate += 1
        elif 6 <= mag <= 6.9:
            major += 1
        elif 7 <= mag:
            strong += 1

    #  Creating dictionary where the keys are 'light', 'moderate', 'major',
    #  and 'strong' and the values are the frequency of each key category
    mag_freq_dict = {}
    for freq in ['light', 'moderate', 'major', 'strong']:
        mag_freq_dict[freq] = eval(freq)

    # Table displaying category frequencies if print_table parameter = True
    if print_table:

        for key in mag_freq_dict:
            row_key = key.capitalize()
            row_val = mag_freq_dict[key]

            row_txt = "{:<9} : {:>4}".format(row_key, row_val)
            print(row_txt)

    return mag_freq_dict


# 4. Visualize data
def plot_bar(x: list, y: list, title: str) -> matplotlib.pyplot.Figure:
    """
    Visualize the differences in earthquakes between 2021 and 2020 in the four categories defined in the last part.
    :param x: list of keys used to label bars
    :param y: list of differences between the values of each key from from two different years of earthquake data
    :param title: the title of the bar graph
    :return: fig: resulting Figure object
    """

    fig = plt.Figure()
    plt.title(title)

    # Creating dictionary containing x and y axis values for bar graph
    # (keys = x axis, values = y axis)
    diff_dict = {}
    counter = 0
    for key in x:
        diff_dict[key] = y[counter]
        counter += 1

    keys = diff_dict.keys()
    values = diff_dict.values()

    plt.bar(keys, values)

    plt.savefig(f'barplot-{title}.png')

    plt.show(block=False)

    return fig


def plot_scatter(x: list, y: list, title: str) -> matplotlib.pyplot.Figure:
    """
    Creates a scatterplot with the provided x and y lists
    :param x: list of data for specific earthquake attribute, e.g. depth
    :param y: list of data for specific earthquake attribute, e.g. magnitude
    :param title: title of scatter plot
    :return: fig: resulting Figure object
    """
    fig = plt.Figure()
    plt.title(title)
    plt.scatter(x, y, s=10)

    plt.savefig(f'scatterplot-{title}.png')
    plt.show(block=False)

    return fig


# CREDIT: main function created by University of Oregon CIS department; not my work
def main():
    """
    Perform all required steps for this project by calling other functions.
    """

    # 2020 data
    eq_data = load_data('earthquakes-2020.csv')
    magnitudes = get_series(eq_data, 'mag', float)
    print("2020 Earthquakes:")
    categories20 = get_categories(magnitudes)

    # 2021 data
    eq_data = load_data('earthquakes-2021.csv')
    magnitudes = get_series(eq_data, 'mag', float)
    print("\n2021 Earthquakes:")
    categories21 = get_categories(magnitudes)

    # Creating list to be argument for plot_bar list contains differences between 2021 and 2020 magnitudes)
    diff21_20 = []
    for key in categories20.keys():
        diff21_20.append(categories21[key] - categories20[key])

    # Plotting bar graph and scatterplot
    plot_bar(categories21.keys(), diff21_20, '2021 - 2020 Earthquakes')
    depths = get_series(eq_data, 'depth', float)
    plot_scatter(depths, magnitudes, '2020 Depth vs Magnitude')


if __name__ == '__main__':
    main()



