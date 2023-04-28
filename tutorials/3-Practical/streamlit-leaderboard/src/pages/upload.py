import streamlit as st
from zipfile import ZipFile
from src.submissions.submissions_manager import SubmissionManager
from src.evaluation.evaluator import Evaluator
from src.config import SUBMISSIONS_DIR, EVALUATOR_CLASS, EVALUATOR_KWARGS,\
    ALLOWED_SUBMISSION_FILE_EXTENSION
from src.submissions.submission_sidebar import SubmissionSidebar

@st.cache_data()
def get_submission_manager():
    return SubmissionManager(SUBMISSIONS_DIR)

@st.cache_data()
def get_submission_sidebar(username: str) -> SubmissionSidebar:
    return SubmissionSidebar(username, get_submission_manager(),
                             submission_validator=get_evaluator().validate_submission,
                             submission_evaluator=get_evaluator().evaluate,
                             submission_file_extension=ALLOWED_SUBMISSION_FILE_EXTENSION,
                             )

@st.cache_data()
def get_evaluator() -> Evaluator:
    return EVALUATOR_CLASS(**EVALUATOR_KWARGS)


# initialize session_state
if 'username' not in st.session_state.keys():
    st.session_state['username'] = ''


get_submission_sidebar(st.session_state['username']).run_submission()
