from typing import List, Callable

import streamlit as st

"""
Component
    - StreamlitComponentHandler
    - BaseLayout
"""


class _Component:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def _render(self):
        raise NotImplementedError

    def render(self):
        self._render()


class StreamlitComponent(_Component):
    def __init__(self, streamlit_func: Callable, *args, **kwargs):
        # TODO: add type hint
        self.streamlit_func = streamlit_func
        self.args = args
        self.kwargs = kwargs

    def _render(self):
        self.streamlit_func(*self.args, **self.kwargs)


class _VerticalRenderer(_Component):
    """Accepts a list of components and render them from top to bottom"""

    def __init__(self, *components: List[_Component]):
        self._check_input_validity(components)
        self._components = components

    def _render(self):
        for component in self._components:
            component.render()

    def _check_input_validity(self, components: List[_Component]):
        for component in components:
            assert isinstance(
                component, _Component
            ), f"component {component} should be an instance of _Component"

    @property
    def n_items(self):
        return len(self._components)


class _HorizontalRenderer(_VerticalRenderer):
    def __init__(self, *components, ratio: List[int] = None):
        super().__init__(*components)
        self._ratio = ratio
        self.__ratio_validity_check()

    def __ratio_validity_check(self):
        if self._ratio:
            assert self.n_items == len(
                self._ratio
            ), f"ratio length {len(self._ratio)} should be equal to number of items {self.n_items}"

    def _render(self):
        rows = st.columns(self._ratio) if self._ratio else st.columns(self.n_items)
        for component, row in zip(self._components, rows):
            with row:
                component.render()


class Column(_VerticalRenderer):
    pass


class Row(_HorizontalRenderer):
    pass


class Layout(_VerticalRenderer):
    # call at initializing instance
    def __init__(self, *components: List[_Component]):
        super().__init__(*components)
        self.render()
