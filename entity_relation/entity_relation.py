from re import A
from tokenize import String
import pandas as pd
from spacy.matcher import Matcher


def find_rel(doc, nlp):
    subject = []
    target = []
    relation = []
    entities = set()
    for token in doc:
        if token.dep_ == "ccomp" or token.dep_ == "ROOT" or token.pos_ == "VERB":
            if token.text in ["said", "say"] and token.text in relation:
                continue
            sub = find_sub(token)
            if token.i == len(doc)-1:
              break
            if token.nbor().dep_ in ["agent", "prep"]:
                rel = " ".join([token.text, token.nbor().text])
                obj = find_obj(token.nbor(), doc)
            else:
                rel = token.text
                obj = find_obj(token, doc)

            if sub is None:
                continue
            sub = get_full_word(sub, doc)
            if obj is None:
                continue
            subject.append(sub)
            target.append(str(obj))
            relation.append(rel)
            entities.add(sub)
            entities.add(obj)

    location_rel = find_rel_location(doc, nlp)
    for rel in location_rel:
        subject.append(rel[0])
        relation.append(rel[1])
        target.append(rel[2])
        entities.add(rel[0])
        entities.add(rel[2])
    input_df = pd.DataFrame({"source": subject, "relation": relation, "target": target})
    # print(input_df)
    input_df.to_csv("assets/input-data-for-graph.csv", index=False)
    entity_df = pd.DataFrame(
        {
            "id": range(1, len(entities) + 1),
            "entity": [
                *entities,
            ],
        }
    )
    entity_df.to_csv("assets/entities-for_graph.csv", index=False)
    return input_df


def find_sub(pred):
    if len(list(pred.lefts)) > 0:
        for token in pred.lefts:
            if token.dep_ in ["nsubj", "nsubjpass"]:
                return token
    else:
        if pred.i > 1:
            if pred.nbor(-1).dep_ != "punct":
                return pred.nbor(-1)
            else:
                return pred.nbor(-2)


def find_obj(pred, article):
    obj_dep = ["dobj", "pobj", "iobj", "obj", "obl"]
    obj = None
    # print("pred=",pred)
    for token in pred.rights:
        if token.dep_ != "punct" and token.dep_ in obj_dep:
            # print("obj",token)
            obj = token
            break
    if obj == None:
        for token in pred.rights:
            if token.dep_ != "punct":
                if token.dep_ == "ccomp":
                    obj = find_sub(token)
                    break
                else:
                    # for right in token.rights:
                    right = token
                    if right.dep_ == "xcomp":
                        obj = find_obj(right, article)
                        break
                    else:
                        if right.pos_ != "ADP":
                            obj = right
                            break
                        else:
                            obj = find_obj(right, article)
                            break

    if obj == None:
        for token in pred.lefts:
            if token.dep_ == "ccomp":
                obj = find_sub(token)
    if obj != None and type(obj) != str:
        obj = get_full_word(obj, article)
        # print("full word",obj)

    return obj


def get_full_word(token, article):
    entities = [ent for ent in article.ents]
    for words in entities:
        if token.i in range(words.start, words.end):
            return words.text
        elif token.text == article[words.start].text:
            return words.text
    nouns = [ent for ent in article.noun_chunks]
    for words in nouns:
        if token in words:
            return words.text
    return token.text


def find_rel_location(article, nlp):
    matcher = Matcher(nlp.vocab)
    rel_list = []
    pattern = [
        {"ENT_TYPE": "ORG"},
        {"POS": {"IN": ["ADP", "PUNCT"]}},
        {"POS": "DET", "OP": "?"},
        {"ENT_TYPE": "GPE"},
    ]
    matcher.add("located", [pattern])
    matches = matcher(article)
    for match_id, start, end in matches:
        span = article[start:end]

        rel_list.append(
            [
                get_full_word(span[0], article),
                "located in",
                get_full_word(span[-1], article),
            ]
        )
    return rel_list
