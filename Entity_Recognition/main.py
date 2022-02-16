import spacy


from entity_relation.entity_relation import *
from text_preprocessing.Text_Preprocessing import *


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
from entity_relation import *


nlp = spacy.load("en_core_web_sm")


# Create a page dropdown
page = st.selectbox("Select Category", [
                    "Article based Graph", "Categorical Graph"])


if page == "Article based Graph":

    sentence = st.text_input("Input your sentence here:")
    if sentence:
        sentence = normalize_docs_text(sentence)
        article = nlp(sentence)

        input_df = find_rel(article, nlp)

        nodes = []
        edges = []

        len_df = len(input_df)

        for i in range(len_df):

            nodes.append(

                Node(id=input_df.iloc[i, 0],
                     label=input_df.iloc[i, 0],
                     size=1000,
                     labelPosition='right',
                     color='green',
                     )
            )

            nodes.append(
                Node(id=input_df.iloc[i, 2],
                     label=input_df.iloc[i, 2],
                     size=1000,
                     labelPosition='left',
                     color='green'
                     )


            )

            edges.append(
                Edge(
                    source=input_df.iloc[i, 0],
                    label=input_df.iloc[i, 1],
                    target=input_df.iloc[i, 2],
                    type="STRAIGHT",
                    strokeWidth=1.5,
                )
            )

        config = Config(width=1200,
                        height=700,
                        directed=True,
                        node={'labelProperty': 'label'},
                        link={'labelProperty': 'label', 'renderLabel': True},
                        collapsible=False)

        return_value = agraph(nodes=nodes, edges=edges, config=config)

        st.dataframe(input_df)


if page == "Categorical Graph":

    df = pd.read_excel("assets//" + "preprocessed_text.xlsx")

    option = st.selectbox(
        "What category do you want to test?", df.categories.unique())
    option_clean = option.replace("['", "").replace("']", "")

    st.write("You selected:", option_clean)

    data = df[df.categories == (option)]["text"]
    entity_set = []
    for entity in data:
        article = nlp(entity)
        for ne in article.ents:
            if ne.label_ == "ORG":
                entity_set.append(ne.text)
    input_df = pd.DataFrame(
        {
            "source": entity_set,
            "relation": ["has article related to"] * len(entity_set),
            "target": option_clean,
        }
    ).drop_duplicates()

    nodes_list = []
    edges_list = []
    nodes_list.append(
        {"id": option_clean, "label": option_clean, "shape": "dot", "size": 10}
    )
    len_df = len(input_df)
    if len_df >= 21:
        for i in range(21):
            nodes_list.append(
                {
                    "id": input_df.iloc[i, 0],
                    "label": input_df.iloc[i, 0],
                    "shape": "dot",
                    "size": 10,
                }
            )
            edges_list.append(
                {
                    "from": input_df.iloc[i, 0],
                    "relation": input_df.iloc[i, 1],
                    "to": option_clean,
                    "weight": 1,
                }
            )
    else:
        for i in range(len_df):
            nodes_list.append(
                {
                    "id": input_df.iloc[i, 0],
                    "label": input_df.iloc[i, 0],
                    "shape": "dot",
                    "size": 10,
                }
            )
            edges_list.append(
                {
                    "from": input_df.iloc[i, 0],
                    "relation": input_df.iloc[i, 1],
                    "to": option_clean,
                    "weight": 1,
                }
            )

    html_str = (
        """
    <html>
    <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>
    <center>
    </center>

    <!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
    <script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->

    <style type="text/css">

            #mynetwork {
                width: 100%;
                height: 700px;
                background-color: #ffffff;
                border: 1px solid lightgray;
                position: relative;
                float: left;
            }

            #config {
                float: left;
                width: 1000px;
                height: 600px;
            }

    </style>

    </head>

    <body>
    <div id = "mynetwork"></div>


    <div id = "config"></div>

    <script type="text/javascript">

        // initialize global variables.
        var edges;
        var nodes;
        var network;
        var container;
        var options, data;

        // This method is responsible for drawing the graph, returns the drawn network
        function drawGraph() {
            var container = document.getElementById('mynetwork');

            // parsing and collecting nodes and edges from the python
            nodes = new vis.DataSet("""
        + str(nodes_list)
        + """);
            edges = new vis.DataSet("""
        + str(edges_list)
        + """);

            // adding nodes and edges to the graph
            data = {nodes: nodes, edges: edges};

            var options = {
        "configure": {
            "enabled": true,
            "filter": [
                "physics"
            ]
        },
        "edges": {
            "color": {
                "inherit": true
            },
            "smooth": {
                "enabled": false,
                "type": "continuous"
            }
        },
        "interaction": {
            "dragNodes": true,
            "hideEdgesOnDrag": false,
            "hideNodesOnDrag": false
        },
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "fit": true,
                "iterations": 1000,
                "onlyDynamicEdges": false,
                "updateInterval": 50
            }
        }
    };

            // if this network requires displaying the configure window,
            // put it in its div
          //  options.configure["container"] = document.getElementById("config");

            network = new vis.Network(container, data, options);

            return network;

        }

        drawGraph();

    </script>
    </body>
    </html>
        """
    )

    components.html(html_str, height=1200, width=700)

    st.dataframe(input_df)
