# -*- coding: utf-8 -*-
import pytest
from source.parts.keras import KerasPilot, KerasLinear
from source.parts.keras import default_linear


def test_linear():
    kl = KerasLinear()
    assert kl.model is not None


def test_linear_with_model():
    kc = KerasLinear(default_linear())
    assert kc.model is not None

