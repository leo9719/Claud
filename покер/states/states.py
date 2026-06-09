"""FSM state groups for Poker Academy Bot."""

from aiogram.fsm.state import State, StatesGroup


class LanguageSelection(StatesGroup):
    choosing = State()


class TheoryFlow(StatesGroup):
    viewing_topic = State()


class TrainingFlow(StatesGroup):
    hands_eval = State()
    decisions = State()
    equity_drill = State()
    simulator = State()
    quiz_active = State()
    quiz_done = State()


class PokerTypeFlow(StatesGroup):
    viewing_variant = State()


class AffiliateFlow(StatesGroup):
    viewing_rooms = State()
