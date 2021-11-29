import spacy
import benepar



## Extract clauses
def text2clauses(text, nlp):
    sents = nlp(text).sents
    clauses = []
    for sent in sents:
        clauses += extract_main(sent)
    return clauses

def extract_main(sent):
    """
    recursive magic

    returns a list of main clauses (or the original input)
    """
    cleaned = [child for child in sent._.children if child._.labels]

    main_clauses = [child for child in cleaned if ('S' in child._.labels
                        or 'CS' in child._.labels) and 'NP' not in child._.labels]
    
    result = []
    if  main_clauses:
        np_idc = [idx for idx, is_np in enumerate([True if 'NP' in child._.labels else False for child in cleaned]) if is_np]
        for idx, clause in enumerate(main_clauses):
            if idx+1 not in np_idc:
                result += extract_main(clause)
            else:
                result += [", ".join(map(str, (clause, list(cleaned)[idx+1])))]
        return result
    else:
        return [str(sent)]

nlp = spacy.load('de_core_news_sm')
nlp.add_pipe("benepar", config={"model": "benepar_de2"})

examp = "Das ist schön, aber das ist doof. Schönes Wetter hier und Kiel ist auch toll. Blabla."

clauses = text2clauses(examp, nlp) 