from dataclasses import dataclass
import numpy as np
from anytree import NodeMixin


@dataclass
class BaseSubreddit:
    """A single subreddit/community"""

    id: str
    name: str
    embedding: np.array
    embedding_std: np.array
    partisan_score: float
    partisan_score_std: float

    def __repr__(self):
        return f"Subreddit: {self.name}"


class Subreddit(BaseSubreddit, NodeMixin):  # add Node functionality
    def __init__(self, parent=None, children=None, *args, **kwargs):
        super(Subreddit, self).__init__(*args, **kwargs)
        self.parent = parent
        if children:
            self.children = children

    @staticmethod
    def __streamlit_repr__():
        """
        Returns an empty string in order to not get printed.
        """
        return ""
