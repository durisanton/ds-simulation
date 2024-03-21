import base64
import io
import urllib

from matplotlib.figure import Figure


class Utils:

    @staticmethod
    def get_image(fig: Figure) -> str:
        # convert graph into string buffer and then we convert 64 bit code into image
        buf = io.BytesIO()
        fig.set_size_inches(w=15, h=8)
        fig.savefig(fname=buf, format='png', dpi=150)
        buf.seek(0)
        string = base64.b64encode(buf.read())
        return urllib.parse.quote(string)
