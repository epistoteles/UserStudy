import pickle
import random
from objects import Subreddit, Submission, Comment
import pandas as pd


SAMPLE_SIZE = 100


root = pickle.load(open("data/demo_tree.pickle", "rb"))

# draw random comments as samples
descendants = [x for x in root.descendants if isinstance(x, Comment)]
samples = random.sample(descendants, SAMPLE_SIZE)

# save comment ids
ids = [x.id for x in samples]

# add first parent (or None)
samples = [(x, x.parent) if not isinstance(x.parent, Subreddit) else (x, None) for x in samples]

# add second parent (or None)
samples = [
    (*x, x[1].parent) if x[1] is not None and not isinstance(x[1].parent, Subreddit) else (*x, None)
    for x in samples
]

# transform mini-threads into markdown strings
markdown = [
    list(
        map(
            lambda x: x.body
            if isinstance(x, Comment)
            else f"{x.title}  \n{x.body}"
            if isinstance(x, Submission) and x.body != ""
            else f"{x.title}"
            if isinstance(x, Submission)
            else "",
            thread,
        )
    )
    for thread in samples
]

# format strings as indented quotes and join
markdown = ["  \n".join([f"> {c3}", f">> {c2}", f">>> {c1}"]) for c1, c2, c3 in markdown]

# create dataframe with ids and comments
result = pd.DataFrame({"id": ids, "comment_markdown": markdown})

# save as csv that can be uploaded to Google Sheets
result.to_csv("sample.csv", index=False)
