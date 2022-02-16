# nlp4jo

![knowledge_graph](https://github.com/ujjwalk00/Entity_Recognition/blob/dev/assets/nlp4jo_logo.png)


## Description
Our manager at a consultancy agency has been overrun by an influx of projects that involve large volumes of financial news. He hands you piles and piles of documents and asks you to read each one and provide a summary of: 

**Who is implicated in this document? and what are their relationships?**

**How hard could that be? Not that hard, no ?** True. If you know, natural language processing that is. You realize that what your manager really wants, is a knowledge graph.

![knowledge_graph](https://d1.awsstatic.com/products/Neptune/knowledge_graph.b0e9408219d92f2ca3c7a05cccf9a5a72e34ddbd.png)


## Objectives

- Be able to preprocess data obtained from textual sources
- Be able to employ named entity recognition and relationship extraction using SpaCy
- Be able to visualize results
- Be able to present insights and findings to client
- Be able to store data using the graph database Neo4j
- Be able to write clean and documented code.


## Repo architecture

* README.md -> Explains the project and gives a report

* requirements.txt -> Shows information on what libraries and python version to install/use.

* main.py  -> Runs the streamlit application

* text_preprocessing -> Contains the code for the proprecessing stage of the project 

* entity_relation -> Contains the code for entity/relation extraction

* graph -> Contains the code for the graph creation

## Installation

- Clone this repository into your local environment with below command-

  `git clone https://github.com/ujjwalk00/Entity_Recognition.git`

- Create python virtual environment

- Install all the required library with below command

  `pip install -r requirements.txt`

## Usage

To run application with streamlit run main.py with below command.

  `streamlit run main.py`
Application withh open in browser automatically or you can also find application url in terminal like below

![terminal](assets/streamlit_run.png)

You can open url in browser and your application will load.

## Visualization examples

This knowledge graph shows us how the entities are related to eachother based on a single article:
![knowledge_graph](https://github.com/ujjwalk00/Entity_Recognition/blob/dev/assets/article_graph.png)

This knowledge graph shows us how the entities from different articles are related to a certain category:
![knowledge_graph](https://github.com/ujjwalk00/Entity_Recognition/blob/dev/assets/organisation_category_graph.png)


## Collaborators

Design and construction phase of the project was made by 3 collaborators.([Ujjwal Kandel](https://github.com/Ujjwalk00), [Reena Koshta](https://github.com/reenakoshta10), and [Maryam El B](https://github.com/agilepydev))


## Timeline

*January 2022*

- Duration: `2 weeks`
- Deadline: `20/01/2022 4:30 PM`
