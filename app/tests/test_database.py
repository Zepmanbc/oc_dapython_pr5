#! /usr/bin/env python3

"""Tests For database."""

import pytest

from app.database.database import Database


class Test_database():
    """Test."""

    def setup(self):
        """Set up Pytest method."""
        pass

    def teardown(self):
        """Teardown test method."""
        pass

    def test_one(self):
        """test."""
        db = Database()
        assert 1