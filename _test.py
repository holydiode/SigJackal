import pytest
from main import SIGPackJackaler, FileHandler


def test_geting_default_handler():
    jac = SIGPackJackaler("temp")
    assert type(jac.get_handler("")) == FileHandler