from os.path import dirname, abspath, join


def get_results_path(f_name, model_name='m14', ext='csv'):
    """Helper function to navigate to the results folder."""

    # src folder
    parent_dir = dirname(dirname(abspath(__file__)))
    # relative path
    rel_path = "results/" + model_name + "/"
    # full path
    return join(parent_dir, rel_path, f_name + '.' + ext)


def preprocess_binary_results(x, y):
    """Preprocess the data so that there is no overlapping dots in the step
    plot."""

    new_x = []
    new_y = []

    n = len(x)

    # enumerate all original data points
    for i, _y in enumerate(y):

        # always include the end points
        if (i == 0) or (i == n - 1):
            new_x.append(x[i])
            new_y.append(_y)

        # identify points whose next points change values
        elif _y != y[i + 1]:

            # add point with current y and next x (so that the jump is vertical)
            new_x.append(x[i + 1])
            new_y.append(_y)

            # add point with nex y and next x
            new_x.append(x[i + 1])
            new_y.append(y[i + 1])

        # neglect redundant points
        else:
            pass

    return new_x, new_y


def generate_rec_data(x, y):
    """Generate list of tuples to prepare for broken_barh. Helper function of
    plot_modes.

    Input format:
    - x: [1, 2, 3, ...] (identical difference)
    - y: [0, 1, 1, ...] (only 0 and 1)

    Output format:
    - [(23, 5), (30, 10), ...]
    - Within each tuple,
        - 1st element: starting point of 1
        - 2nd element: ending point of 1
    """

    rec_list = []

    # make sure x, y are list
    x, y = list(x), list(y)

    n = len(x)
    start_idx = None

    # enumerate all original data points
    for i, _y in enumerate(y):

        # identify starting points
        # 1. starting point, i = 0
        # 2. previous point = 0, current point = 1
        if ((i == 0) and (_y == 1)) or (y[i - 1] == 0 and _y == 1):
            start_idx = i

        # identify ending point
        elif y[i - 1] == 1 and _y == 0:

            # i - 1 is the ending point
            # + 1 so that both endpoints are included
            width = x[i - 1 + 1] - x[start_idx]

            # add rectangle tuple
            rec_list.append((x[start_idx], width))
            # reset starting point
            start_idx = None

        else:
            pass

    # check if the ending piece is always 1
    if y[-1] == 1 and start_idx is not None:
        width = x[-1] - x[start_idx - 1]
        rec_list.append((x[start_idx], width))

    return rec_list