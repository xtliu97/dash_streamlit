import streamlit as st
import dash_streamlit as dst

dst.set_wide_layout()


dst.Layout(
    dst.Row(
        dst.StreamlitComponent(st.header, "dash_streamlit"),
        dst.StreamlitComponent(st.text, dst.__version__),
    )
)


dst.Layout(
    dst.Row(
        dst.Column(
            dst.StreamlitComponent(st.header, "Column 1"),
            dst.StreamlitComponent(st.write, "width=1"),
        ),
        dst.Column(
            dst.StreamlitComponent(st.header, "Column 2"),
            dst.StreamlitComponent(st.write, "width=3"),
        ),
        dst.Column(
            dst.StreamlitComponent(st.header, "Column 3"),
            dst.StreamlitComponent(st.write, "width=2"),
        ),
        ratio=[1, 3, 2],
    )
)
