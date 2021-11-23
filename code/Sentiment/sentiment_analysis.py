from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment",
                                                                        output_hidden_states = True)

model.eval() # get model into evaluation modus (out of training modus)

corpus = ["Hallo, wie gehts?", "Kiel ist super."] # list of strings to batch-tokenize

# batch tokenization
tokenized = tokenizer(corpus, padding=True, truncation=True, return_tensors="pt")
    
with torch.no_grad():
    model_output = model(**tokenized)

hidden = model_output.hidden_states

"""

Dimensions of hidden in given order: 
- Outputs of each of BERT’s 12 layers + input layer (13 tensors).
- Batches (sentences)
- Word / Tokens (Max. 512)
- Features (768 features) -> Vector we are looking for

https://medium.com/@dhartidhami/understanding-bert-word-embeddings-7dc4d2ea54ca

"""

embeddings = hidden[-1:][0] # only last layer as embedding

# save embedding for each unique word/token under its vocab-id in a dictionary
word_dir = {}
for text_idx, text in enumerate(corpus):
    for word_idx, token_id in enumerate(tokenizer.encode(text)):
        if word_idx == 512: 
            break # bert models only take a maxium of 512 tokens per segment/batch into account
        if token_id not in (101, 102): # not "CLS" or "SEP" (Bert specific special tokens)
            embedding = embeddings[text_idx][word_idx]
            if not token_id in word_dir:
                word_dir[token_id] = [embedding]
            else:
                word_dir[token_id].append(embedding)

## Demo for "Essen" 
"""
<corpus> variable has to be a list of german sentences for this to work
This Bert model is multilingual and detects the proper language automatically.

"""

food_encoded = tokenizer.encode("Das Essen ist lecker.")
town_encoded = tokenizer.encode("Essen ist eine schöne Stadt.")

tokenizer.decode(food_encoded[2]) # 'essen' -> model is uncased
