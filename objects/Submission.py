from utils.formatter import *
from dataclasses import dataclass
from datetime import datetime
from anytree import NodeMixin
import textwrap
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm


@dataclass
class BaseSubmission:
    """A single reddit submission"""

    id: str
    author: str
    partisan_score: np.ndarray  # np.array([score, score_std])
    title: str
    body: str
    url: str
    creation_date: datetime
    score: int
    subreddit: str
    permalink: str
    civility: float = -1.0  # -1 means undefined

    def __repr__(self):
        c = "red" if self.partisan_score[0] > 0 else "blue"
        return (
            f"{'▲' if self.score >= 0 else '▼'} {self.score} {italic(self.author)} "
            f"(Partisan score/std: {self.partisan_score[0]:.3f},{self.partisan_score[1]:.3f})\n"
            f"{color(blocked(self.title), c=c)}{chr(10) if self.body else ''}"
            f"{color(blocked(chr(10).join(textwrap.wrap(self.body, width=100))), c=c)}"
        )

    def __hash__(self):
        return hash(self.id)


class Submission(BaseSubmission, NodeMixin):  # add Node functionality
    def __init__(self, parent=None, children=None, *args, **kwargs):
        super(Submission, self).__init__(*args, **kwargs)
        self.parent = parent
        if children:
            self.children = children

    def __streamlit_repr__(self):
        """
        Returns a multi-line string optimized for streamlit markdown.
        Includes a colored partisan square and line-length adjustment for hidden links.
        """
        # determine square color
        norm = mpl.colors.Normalize(vmin=-0.2, vmax=0.2)
        cmap = cm.RdBu
        m = cm.ScalarMappable(norm=norm, cmap=cmap)
        c_hex = mpl.colors.to_hex(
            m.to_rgba(-self.partisan_score[0]), keep_alpha=False
        )  # color of score on blue-red scale

        # place line while showing hidden links
        body = self.body
        # body = re.sub(r"\[((.|\n)*?)\]\(((.|\n)*?)\)", r"\1 \3", body)  # make markup links normal text
        # body = "\n".join(textwrap.wrap(body, width=int(170-self.depth*2.6)))  # place new line breaks

        return (
            f"{'▲' if self.score >= 0 else '▼'} {self.score}&nbsp;&nbsp;&nbsp;[_{self.author}_]"
            f"(https://www.reddit.com/user/{self.author}/)&nbsp;&nbsp;&nbsp;<!-- METADATA -->"
            f"![{c_hex}](https://via.placeholder.com/20/{c_hex.lstrip('#')}/000000?text=+) "
            f"_Partisan score:_ {self.partisan_score[0]:.3f},&nbsp;&nbsp;&nbsp;"
            f"_Civility score:_ {self.civility:.3f},&nbsp;&nbsp;&nbsp;<!-- END-METADATA -->"
            f"_Date:_ {self.creation_date},&nbsp;&nbsp;&nbsp;[🔗Reddit](https://www.reddit.com{self.permalink})  \n"
            # uncomment if you want to limit the line length
            # f"{chr(10).join(textwrap.wrap(self.title, width=int(170-self.depth*2.6)))}{f'  {chr(10)}' if self.body else ''}"
            f"{self.title}{f'  {chr(10)}' if self.body else ''}"
            f"{body}"
        )
