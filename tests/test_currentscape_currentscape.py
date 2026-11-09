"""Test plot_currentscape end-to-end with small synthetic data."""

from unittest import mock

import matplotlib.pyplot as plt
import numpy as np
import pytest

from currentscape.currentscape import plot_currentscape
from currentscape.plotting import get_colormap


def synthetic_data():
    """Return small synthetic voltage, currents and time arrays."""
    time = np.linspace(0.0, 10.0, 11)
    voltage = np.linspace(-70.0, -40.0, 11)
    currents = np.array([np.sin(time), np.cos(time)])
    return voltage, currents, time


def pattern_config():
    """Return a config using patterns, like in the reported infinite-loop issue."""
    return {
        "current": {"names": ["curr1", "curr2"], "reorder": False},
        "output": {"savefig": False},
        "pattern": {"use": True, "patterns": ["", ".", "x"]},
    }


def test_plot_currentscape_empty_ions_data():
    """plot_currentscape with empty ions_data should return a figure, not hang."""
    voltage, currents, time = synthetic_data()

    fig = plot_currentscape(
        voltage, currents, pattern_config(), ions_data=[], time=time
    )

    assert fig is not None
    plt.close(fig)


def test_plot_currentscape_none_ions_data():
    """plot_currentscape with ions_data=None should return a figure."""
    voltage, currents, time = synthetic_data()

    fig = plot_currentscape(
        voltage, currents, pattern_config(), ions_data=None, time=time
    )

    assert fig is not None
    plt.close(fig)


@pytest.mark.parametrize("currents_data", [None, [], [[], []], np.empty((2, 0))])
def test_plot_currentscape_empty_currents_data(currents_data):
    """plot_currentscape with no currents should fail fast instead of hanging."""
    voltage, _, time = synthetic_data()

    with pytest.raises(ValueError, match="no current data"):
        plot_currentscape(voltage, currents_data, pattern_config(), time=time)


@pytest.mark.parametrize("ions_data", [[], [[], [], []], np.empty((3, 0))])
def test_plot_currentscape_empty_ions_are_not_counted(ions_data):
    """Empty ions should be treated as no ions, including for the colormap size."""
    voltage, currents, time = synthetic_data()

    with mock.patch(
        "currentscape.currentscape.get_colormap", wraps=get_colormap
    ) as colormap:
        fig = plot_currentscape(
            voltage, currents, pattern_config(), ions_data=ions_data, time=time
        )

    assert colormap.call_args.args[-1] is None
    plt.close(fig)


def test_plot_currentscape_disabled_empty_patterns():
    """An empty pattern list should stay valid when patterns are not used."""
    voltage, currents, time = synthetic_data()
    config = pattern_config()
    config["pattern"] = {"use": False, "patterns": []}

    fig = plot_currentscape(voltage, currents, config, time=time)

    assert fig is not None
    plt.close(fig)


def test_plot_currentscape_ions_with_patterns_use_time_axis():
    """Ion lines plotted with patterns should be placed on the time axis."""
    voltage, currents, _ = synthetic_data()
    time = np.linspace(100.0, 200.0, 11)
    config = pattern_config()
    config["ions"] = {"names": ["ion1"]}

    fig = plot_currentscape(
        voltage, currents, config, ions_data=[np.linspace(0.1, 1.0, 11)], time=time
    )

    assert np.array_equal(fig.axes[-1].get_lines()[0].get_xdata(), time)
    plt.close(fig)


@pytest.mark.parametrize("use_patterns", [True, False])
def test_plot_currentscape_all_zero_ions(use_patterns):
    """All-zero ion data has no scale but should not make the plot fail."""
    voltage, currents, time = synthetic_data()
    config = pattern_config()
    config["pattern"]["use"] = use_patterns
    config["ions"] = {"names": ["ion1"]}

    fig = plot_currentscape(
        voltage, currents, config, ions_data=[np.zeros(11)], time=time
    )

    assert fig is not None
    plt.close(fig)


def test_plot_currentscape_with_ions_and_patterns():
    """plot_currentscape with ion data and patterns plots ions with linestyles."""
    voltage, currents, time = synthetic_data()
    config = pattern_config()
    config["ions"] = {"names": ["ion1"]}

    fig = plot_currentscape(
        voltage, currents, config, ions_data=[np.linspace(0.1, 1.0, 11)], time=time
    )

    assert len(fig.axes) >= 6
    plt.close(fig)
