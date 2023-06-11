import json
from pathlib import Path
from PIL import Image
import logging
from streamlit.source_util import _on_pages_changed, get_pages
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx

def remove_illegal_filename_characters(input_string: str) -> str:
    return "".join(x if (x.isalnum() or x in "._- ") else '_' for x in input_string).strip()


def is_legal_filename(filename: str) -> bool:
    return remove_illegal_filename_characters(filename) == filename

# ---
# Logging 

def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_ip = get_remote_ip()
        return super().filter(record)

def init_logging():
    # Make sure to instanciate the logger only once
    # otherwise, it will create a StreamHandler at every run
    # and duplicate the messages

    # create a custom logger
    logger = logging.getLogger("foobar")
    if logger.handlers:  # logger is already setup, don't setup again
        return
    logger.propagate = False
    logger.setLevel(logging.INFO)
    # in the formatter, use the variable "user_ip"
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s [user_ip=%(user_ip)s] - %(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.addFilter(ContextFilter())
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# ---
# This set of functions allows to show no pages before login

def get_all_pages(default_page: str) -> dict:
    default_pages = get_pages(default_page)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


def clear_all_but_first_page(default_page: str):
    current_pages = get_pages(default_page)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages(default_page)

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()

def show_all_pages(default_page: str):
    current_pages = get_pages(default_page)

    saved_pages = get_all_pages(default_page)

    missing_keys = set(saved_pages.keys()) - set(current_pages.keys())

    # Replace all the missing pages
    for key in missing_keys:
        current_pages[key] = saved_pages[key]

    _on_pages_changed.send()


# ---
# utility functions

def files_exist(files: list(), list2check: list()):
    # cleanup the list of files
    list2check = [l for l in list2check if ('__MACOSX' not in l)]

    for f in files:
        matching = [s for s in list2check if (f in s)]
        if len(matching) != 1:
            print(f'missing file {f}')
            print(f'file list = {list2check}')
            return False
    return True

#image load method
def loadImg(image: Path):
    img = Image.open(image)
    return img
