import os
import shutil
from datetime import datetime
import pytest

from turkey_eq_monitor.processing import retrieve_data, plot_map, _UTC

FILE_PATH = "tests/roti_01_17.h5"

C_LIMITS = {
    'ROTI': [0, 0.5,'TECu/min']
}


def test_retrieve_data():
    assert os.path.isfile(FILE_PATH)

    # Test retrieving data without specific times
    data = retrieve_data(FILE_PATH, "ROTI")
    assert isinstance(data, dict)
    assert len(data) > 0

    # Test retrieving data with specific times
    times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in [datetime(2023, 2, 6, 1, 17)]]
    data = retrieve_data(FILE_PATH, "ROTI", times)
    assert len(data[times[0]]) > 100


def test_plot_map():
    # Test plotting data
    times = [t.replace(tzinfo=t.tzinfo or _UTC) for t in [datetime(2023, 2, 6, 1, 17)]]
    data = retrieve_data(FILE_PATH, "ROTI", times)
    _data = {'ROTI': data}

    plot_map(
        plot_times=times,
        data=_data,
        type_d="ROTI",
        lon_limits=(25, 50),
        lat_limits=(25, 50),
        ncols=1,
        clims=C_LIMITS,
        savefig="",
        test_mod=True
    )

    # Test plotting data with saving figure
    savefig = "tests/result.png"
    plot_map(
        plot_times=times,
        data=_data,
        type_d="ROTI",
        lon_limits=(25, 50),
        lat_limits=(25, 50),
        ncols=1,
        clims=C_LIMITS,
        savefig=savefig
    )
    assert os.path.isfile(savefig)
    os.remove(savefig)
