import pickle
import random
from objects import Comment

SAMPLE_SIZE = 100

root = pickle.load(open('data/demo_tree_filtered.pickle', 'rb'))

# draw random comments as samples
descendants = [x for x in root.descendants if isinstance(x, Comment)]
samples = random.sample(descendants, SAMPLE_SIZE)

# add first parent (or None)
samples = [(x, x.parent) for x in samples]

# add second parent (or None)
samples = [(*x, x[1].parent) if x[1] is not None else (*x, None) for x in samples]

# transform mini-threads into markdown strings
markdown = ['\n'.join(list(map(lambda x: x.__streamlit_repr__(), thread))) for thread in samples]

print(markdown[0])
