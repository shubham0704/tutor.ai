# import sys, os
# sys.path.append(os.path.expanduser('~') + '/models/syntaxnet/')
# import tree_gen
import spacy
import string
from nltk import Tree
# use spacy to ner and fill in the blank types
def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_


# def get_svo(text):
#   #subs = objs = verbs = None
#   subs = []
#   verbs = []
#   objs = []
#   parse_tree = tree_gen.get_tree(text)
#   print parse_tree
#   for token in parse_tree.token:
#     '''
#     if token.label == 'nsubj':
#       subs = token.word
#     elif token.label == 'root':
#       verbs = token.word
#     elif token.label == 'obj':
#       obj = token.word
#     else:
#       pass
#     '''
    
#     if "subj" in token.label:
#       subs.append(token.word)
#     elif token.label in ["root", "ex", "md"] or token.label.startswith("v"):
#       verbs.append(token.word)
#     elif "obj" in token.label or token.label.startswith("ob") or token.label=="nummod":
#       objs.append(token.word)
    
        
#   return (subs, verbs, objs)
nlp = spacy.load("en")
  
def get_svo(doc):

  subs = []
  verbs = []
  objs = []
  for tok in doc:
    if len(tok) < 3:
      continue
    if tok.dep_ == "nsubj":
      subs.append(str(tok))
    elif tok.tag_ == ["VBG", "VBD"] or tok.dep_ == "ROOT":
      verbs.append(str(tok))
    elif tok.dep_ in ["iobj", "dobj", "pobj"]:#and tok.tag_ in ["NNP", "CD", "NN"]
      objs.append(str(tok))

  return (subs, verbs, objs)    


def ngram_join(sent, nchunks):
  for chunk in nchunks:
    chunk = str(chunk)
    #print chunk
    chunk_tok = chunk.split()
    
    ng_join = "_".join(e for e in chunk_tok)
    # replace the entity in the string with ng_join
    sent = string.replace(sent, chunk, ng_join)
  return sent

def chain_capitalize(sent):
  tok_sent = [tok for tok in sent.split()]
  temp = []
  new_tok_sent = []
  flag = 0
  for i, tok in enumerate(tok_sent):
    
    if flag == 1:
      flag = 0
      continue
    if len(str(tok)) > 1:
      if tok[0].isupper() and tok[1].islower() or str(tok)=="of":
        temp.append(tok)
        if str(tok) == "of":
          flag = 1
          temp.append(tok_sent[i+1])


      else:
        
        if len(temp) > 0:
          new_tok = '_'.join(tok for tok in temp)
          new_tok_sent.append(new_tok)
        temp = []
        new_tok_sent.append(tok)

  # new_tok_sent = list(set(new_tok_sent))
  # return new_tok_sent
  # for tok in tok_sent:
  return ' '.join(tok for tok in new_tok_sent)




def preprocess(sent):
    sent = chain_capitalize(sent)
    doc = nlp(sent.decode())
    # print [(tok.text, tok.label_) for tok in doc.ents]
    sent = ngram_join(sent, list(doc.noun_chunks))
    #print sent
    print 'the noun chunks are', list(doc.noun_chunks)
    return [word for word in sent.split()], nlp(sent.decode())

if __name__ == '__main__':
  sent = "Babur defeated Ibrahim Hussain Lodi at the First Battle of Panipat in 1526 CE and founded the Mughal empire"
  #sent = "The Sun is the star at the center of the Solar System"
  nlp = spacy.load("en")
  # doc = nlp(sent.decode())
  # #print 'noun_chunks', list(doc.noun_chunks)
  # sent = ngram_join(sent, list(doc.ents))
  # #print sent
  # doc = nlp(sent.decode())
  # sent , doc = preprocess(sent)
  # print [(tok, tok.dep_, tok.tag_) for tok in doc]
   
  #[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
  # sent = chain_capitalize(sent)
  sent , doc = preprocess(sent)
  print [(tok, tok.dep_, tok.tag_) for tok in doc]
  [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
  
  # print sent

  alls = get_svo(doc)
  print alls
  # print sent
