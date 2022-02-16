import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")


def get_ORG_category_relation(category: str):
    data = df[df.categories == ("[" + category + "]")]["text"]
    entity_set = []

    for entity in data:
        article = nlp(entity)
        for ne in article.ents:
            if ne.label_ == "ORG":
                entity_set.append(ne.text)
                print(ne.text, ne.label_)

    input_df = pd.DataFrame(
        {
            "source": entity_set,
            "relation": ["has article related to"] * len(entity_set),
            "target": ["Ship"] * len(entity_set),
        }
    )
    input_df = input_df.drop_duplicates()
    input_df.to_csv("../assets/input-data-for-graph.csv", index=False)


df = pd.read_excel("../assets/preprocessed_text.xlsx")
get_ORG_category_relation("ship")
