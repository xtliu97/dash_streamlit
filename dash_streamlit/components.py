from typing import List, Callable

import inspect
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


import jinja2

subtemplate = jinja2.Template(
    """
class {{ class_name }}(_Component):
    def __init__(self, {{type_annotation_with_default}}):
        # get parameters
        {% for name in parameters %}self._{{name}} = {{name}}
        {% endfor %}
        
    def _render(self):
        st.{{class_name}}(
            {% for name in parameters %}{{name}}=self._{{name}}, 
            {% endfor %}
        )
"""
)


def render(st_func: Callable):
    classname = st_func.__name__
    parameters = []
    type_annotations = []
    default_values = []
    for name, parameter in inspect.signature(st_func).parameters.items():
        parameters.append(name)
        type_annotations.append(parameter.annotation)
        default_values.append(parameter.default)

    type_annotation = []
    for name, type_ in zip(parameters, type_annotations):
        type_annotation.append(f'{name}: "{type_}"')

        # if type_ == str:
        #     type_annotation.append(f"{name}: str")
        # else:
        #     type_annotation.append(f'{name}: "{type_.__name__}"')

    type_annotation = ", ".join(type_annotation)

    input_with_default = []
    for name, type_, value in zip(parameters, type_annotations, default_values):
        if value == inspect.Parameter.empty:
            input_with_default.append(f"{name}")
        else:
            input_with_default.append(f'{name}="{value}"')
        # if type_.__name__ == "Literal":
        #     input_with_default.append(f'{name}="{value}"')
        # elif value != inspect.Parameter.empty:
        #     input_with_default.append(f"{name}={value}")
        # else:
        #     input_with_default.append(name)

    if input_with_default and input_with_default[-1] == "kwargs":
        input_with_default[-1] = "**kwargs"

    input_with_default = ", ".join(input_with_default)

    if len(parameters) == 0:
        parameters = ["self"]

    return subtemplate.render(
        class_name=classname,
        type_annotation=type_annotation,
        type_annotation_with_default=input_with_default,
        parameters=parameters,
    )


exec(render(st.button))


"""
altair_chart = _main.altair_chart
area_chart = _main.area_chart
audio = _main.audio
balloons = _main.balloons
bar_chart = _main.bar_chart
bokeh_chart = _main.bokeh_chart
button = _main.button
caption = _main.caption
camera_input = _main.camera_input
chat_message = _main.chat_message
chat_input = _main.chat_input
checkbox = _main.checkbox
code = _main.code
columns = _main.columns
tabs = _main.tabs
container = _main.container
dataframe = _main.dataframe
data_editor = _main.data_editor
date_input = _main.date_input
divider = _main.divider
download_button = _main.download_button
expander = _main.expander
pydeck_chart = _main.pydeck_chart
empty = _main.empty
error = _main.error
exception = _main.exception
file_uploader = _main.file_uploader
form = _main.form
form_submit_button = _main.form_submit_button
graphviz_chart = _main.graphviz_chart
header = _main.header
help = _main.help
image = _main.image
info = _main.info
json = _main.json
latex = _main.latex
line_chart = _main.line_chart
link_button = _main.link_button
map = _main.map
markdown = _main.markdown
metric = _main.metric
multiselect = _main.multiselect
number_input = _main.number_input
plotly_chart = _main.plotly_chart
progress = _main.progress
pyplot = _main.pyplot
radio = _main.radio
scatter_chart = _main.scatter_chart
selectbox = _main.selectbox
select_slider = _main.select_slider
slider = _main.slider
snow = _main.snow
subheader = _main.subheader
success = _main.success
table = _main.table
text = _main.text
text_area = _main.text_area
text_input = _main.text_input
toggle = _main.toggle
time_input = _main.time_input
title = _main.title
vega_lite_chart = _main.vega_lite_chart
video = _main.video
warning = _main.warning
write = _main.write
color_picker = _main.color_picker
status = _main.status
"""


#  st.altair_chart ...
all_components = [
    st.altair_chart,
    st.area_chart,
    st.audio,
    st.balloons,
    st.bar_chart,
    st.button,
    st.checkbox,
    st.code,
    st.color_picker,
    st.columns,
    st.container,
    st.dataframe,
    st.date_input,
    st.download_button,
    st.empty,
    st.error,
    st.exception,
    st.file_uploader,
    st.form,
    st.form_submit_button,
    st.header,
    st.help,
    st.image,
    st.info,
    st.json,
    st.latex,
    st.line_chart,
    st.markdown,
    st.metric,
    st.multiselect,
    st.number_input,
    st.pyplot,
    st.progress,
    st.pydeck_chart,
    st.radio,
    st.select_slider,
    st.selectbox,
    st.slider,
    st.subheader,
    st.success,
    st.table,
    st.text,
    st.text_area,
    st.text_input,
    st.time_input,
    st.title,
    st.vega_lite_chart,
    st.video,
    st.warning,
    st.write,
]

codes = []

for component in all_components:
    codes.append(render(component))

import os

with open(os.path.join(os.path.dirname(__file__), "compiled.py"), "w") as f:
    f.write("\n".join(codes))
