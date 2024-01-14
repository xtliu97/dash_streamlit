from typing import Dict, List, Type
from collections import defaultdict

import streamlit as st


class _Singleton:
    _instances = None

    def __new__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super().__new__(cls)
        return cls._instances

    @classmethod
    def get(cls):
        return cls._instances


class SessionStateManager(_Singleton):
    def __init__(self):
        self._session_state = st.session_state

    def __getitem__(self, key):
        return self._session_state.get(key, None)

    def __setitem__(self, key, value):
        self._session_state[key] = value
