"""Test the integrity of the spider data being retrieved."""

import logging

import pytest

from rlgpy.api import RocketLeagueGarage


logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_items_not_empty():
    items = RocketLeagueGarage.get_items(cache_enabled=True)
    assert len(items) > 0


@pytest.mark.integration
def test_trades_not_empty():
    trades = RocketLeagueGarage.get_trades()
    assert len(trades) > 0


@pytest.mark.integration
def test_achievements():
    achievements = RocketLeagueGarage.get_achievements()
    assert len(achievements) > 0
