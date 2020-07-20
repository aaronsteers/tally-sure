"""`tally-sure.crypto` - Classes for cryptographically encrypting and signing tallies."""

import hashlib
from typing import List, Dict

from .banks import QuestionBank, TallyBank
from .uniques import Unique, uuid

# from .print import print_card

QUESTION_BANK_REPO = "[TK]"
TALLY_BANK_REPO = "[TK]"


QUESTION_BANK = QuestionBank(QUESTION_BANK_REPO)
TALLY_BANK = TallyBank(TALLY_BANK_REPO)
PERSONAL_SEED = uuid()

PRINT_TEMPLATE = """
Punch Card Name: {punch_card_name} ({punch_card_uuid})

{choices}
"""

CHOICES_TEMPLATE = """
{question}:
    (Question ID: {question_uuid})
{choice} ({choice_uuid})

"""


def get_locale_spec():
    """Returns a language/locale setting for localization purposes."""
    return "us-eng"


LOCALE = get_locale_spec()


class IncompletePunchCardException(Exception):
    pass


def hash_join(uuid1, uuid2, seed):
    m = hashlib.md5()
    m.update(f"{uuid1}{uuid2}{seed}")
    return m.hexdigest()


class PunchCardOption(Unique):
    """An option provided on a punch card."""

    def __init__(self, uuid: str = None):
        """Initialize."""
        super().__init__(uuid)


class PunchCardQuestion(Unique):
    """A punch-card multi-choice."""

    options: List[PunchCardOption]

    def __init__(self, uuid: str = None):
        super().__init__(uuid)
        QUESTION_BANK.get_options(self)

    def get_options(self):
        return QUESTION_BANK.get_options(self)


class PunchCard(Unique):
    """A unique Punch Card."""

    questions: List[PunchCardQuestion]
    choices: Dict[PunchCardQuestion, PunchCardOption]

    def __init__(self, uuid: str = None):
        """Initialize."""
        super().__init__(uuid)
        self.questions = QUESTION_BANK.get_questions(self)

    def set_choice(self, question: PunchCardQuestion, option: PunchCardOption):
        self.choices[question] = option

    def post_choices(self, force: bool = False):
        """Publish the choices.

        If force=True, ignore missing responses in the punchcard.
        Otherwise, raise IncompletePunchCardException if missing responses.
        """
        if not force:
            if len(self.questions - self.choices.keys()) > 0:
                raise IncompletePunchCardException()
        TALLY_BANK.post(punch_card_uuid=self.uuid, choices=self.choices)

    def print_card(self):
        """Print selections."""
        choices_text = "\n".join([CHOICES_TEMPLATE.format(x) for x in self.choices])
        card_text = PRINT_TEMPLATE.format(
            punch_card_name=self.name, punch_card_id=self.uuid, choices=choices_text
        )
        print(card_text)


class Tally(object):
    """A prepped vote tally, may or may not have published=True."""

    uuid: str
    punch_card: PunchCard

    def __init__(self, punch_card, question):
        """Initialize."""
        if uuid:
            self.uuid = uuid
