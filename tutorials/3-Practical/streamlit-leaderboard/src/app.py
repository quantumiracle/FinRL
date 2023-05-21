import sys, pathlib

import streamlit as st

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.login.login import Login
from src.login.username_password_manager import UsernamePasswordManagerArgon2
from src.submissions.submissions_manager import SubmissionManager
from src.config import SUBMISSIONS_DIR, EVALUATOR_CLASS, EVALUATOR_KWARGS, PASSWORDS_DB_FILE, ARGON2_KWARGS, \
    MAX_NUM_USERS, ALLOW_FIRST_LOGIN, DEV_MODE
from src.evaluation.evaluator import Evaluator
from src.display.leaderboard import Leaderboard
from src.display.personal_progress import PersonalProgress
from src.common.css_utils import set_block_container_width
from src.common.utils import show_all_pages, clear_all_but_first_page


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

DEFAULT_PAGE = 'app.py'


def get_login() -> Login:
    password_manager = UsernamePasswordManagerArgon2(PASSWORDS_DB_FILE, **ARGON2_KWARGS)
    return Login(password_manager, MAX_NUM_USERS)

@st.cache_data()
def get_submission_manager():
    return SubmissionManager(SUBMISSIONS_DIR)


@st.cache_data()
def get_evaluator() -> Evaluator:
    return EVALUATOR_CLASS(**EVALUATOR_KWARGS)


@st.cache_data()
def get_leaderboard() -> Leaderboard:
    return Leaderboard(get_submission_manager(), get_evaluator())


# @st.cache_data()
# def get_personal_progress(username: str) -> PersonalProgress:
#     return PersonalProgress(get_submission_manager().get_participant(username), get_evaluator())


# @st.cache_data()
# def get_users_without_admin():
#     return [user for user in get_submission_manager().participants.keys() if user != ADMIN_USERNAME]


# def admin_display_personal_progress():
#     selected_user = st.sidebar.selectbox('Select user to view',
#                                          get_users_without_admin())
#     if selected_user is not None:
#         get_personal_progress(selected_user).show_progress(progress_placeholder)


clear_all_but_first_page(DEFAULT_PAGE)

login = get_login()
login.init(allow_first_login=ALLOW_FIRST_LOGIN)
leaderboard_placeholder = st.empty()
progress_placeholder = st.empty()

# initialize session_state
if 'username' not in st.session_state.keys():
    st.session_state['username'] = ''


if DEV_MODE or (login.run_and_return_if_access_is_allowed() and not login.has_user_signed_out()):
    if DEV_MODE:
        st.sidebar.warning("DEV MODE")

    show_all_pages(DEFAULT_PAGE)

    username = login.get_username()
    get_leaderboard().display_leaderboard(username, leaderboard_placeholder)
    # if get_submission_manager().participant_exists(username) and username != ADMIN_USERNAME:
    #     get_personal_progress(username).show_progress(progress_placeholder)
    # if username == ADMIN_USERNAME:
    #     admin_display_personal_progress()
else:
    get_leaderboard().display_leaderboard('', leaderboard_placeholder)
    clear_all_but_first_page(DEFAULT_PAGE)