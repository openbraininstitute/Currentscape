"""Test legends helpers."""

from types import SimpleNamespace

from currentscape.legends import _legend_handles


def test_legend_handles_new_and_old_matplotlib_attribute():
    """Both legend_handles (mpl>=3.7) and legendHandles (mpl<3.9) are supported."""
    assert _legend_handles(SimpleNamespace(legend_handles=[1])) == [1]
    assert _legend_handles(SimpleNamespace(legendHandles=[2])) == [2]
