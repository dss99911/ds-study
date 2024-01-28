import plotly.offline as of
import plotly.graph_objs as go


# Generate traces to create Sankey diagrams
trace = go.Sankey(
    node = dict(
        pad = 15,
        thickness = 30,
        line = dict(color = "black", width = 1),
        label = labels[0]
    ),
    link = dict(
        source = source[0],
        target = target[0],
        value = value[0]
    ))


plot({
    "data": trace,
    "layout": go.Layout(
        title= diagram_title + "[" + base_date + "]"
    )
})