import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import database as db
from handlers.affiliate import send_post_quiz_nudge
from keyboards.training import quiz_answer_keyboard, training_menu_keyboard
from localization.texts import t
from states.states import TrainingFlow

logger = logging.getLogger(__name__)
router = Router(name="training")

_QUIZ_QUESTIONS = [
    {
        "id": 0,
        "question": {
            "ru": "Какая комбинация старше?",
            "en": "Which hand ranks higher?",
        },
        "options": {
            "ru": ["Стрит", "Флэш", "Фулл-хаус", "Тройка"],
            "en": ["Straight", "Flush", "Full House", "Three of a Kind"],
        },
        "correct": 2,
        "explanation": {
            "ru": "Фулл-хаус (тройка + пара) бьёт стрит и флэш.",
            "en": "Full House (three + pair) beats straight and flush.",
        },
    },
    {
        "id": 1,
        "question": {
            "ru": "Что такое позиция в покере?",
            "en": "What does 'position' mean in poker?",
        },
        "options": {
            "ru": ["Место за столом", "Размер ставки", "Тип раздачи", "Вид покера"],
            "en": ["Your seat at the table", "Bet size", "Hand type", "Poker variant"],
        },
        "correct": 0,
        "explanation": {
            "ru": "Позиция — это ваше место за столом относительно блайндов.",
            "en": "Position refers to your seat relative to the blinds.",
        },
    },
]


@router.callback_query(F.data.startswith("train:"))
async def training_section(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    mode = callback.data.split(":", 1)[1]

    if mode == "quiz":
        await start_quiz(callback, state, lang)
    else:
        await callback.message.edit_text(
            text=t("coming_soon", lang),
            parse_mode="HTML",
            reply_markup=training_menu_keyboard(lang),
        )
        await callback.answer()


async def start_quiz(callback: CallbackQuery, state: FSMContext, lang: str) -> None:
    question = _QUIZ_QUESTIONS[0]
    options = question["options"].get(lang, question["options"]["en"])
    q_text = question["question"].get(lang, question["question"]["en"])

    await state.set_state(TrainingFlow.quiz_active)
    await state.update_data(quiz_index=0, score=0)

    await callback.message.edit_text(
        text=f"❓ <b>{q_text}</b>",
        parse_mode="HTML",
        reply_markup=quiz_answer_keyboard(options, question["id"], lang),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("quiz_answer:"), TrainingFlow.quiz_active)
async def quiz_answer(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    _, q_id_str, ans_str = callback.data.split(":")
    q_id, ans_idx = int(q_id_str), int(ans_str)

    data = await state.get_data()
    quiz_index: int = data.get("quiz_index", 0)
    score: int = data.get("score", 0)

    question = _QUIZ_QUESTIONS[q_id]
    is_correct = ans_idx == question["correct"]
    explanation = question["explanation"].get(lang, question["explanation"]["en"])

    if is_correct:
        score += 1
        result_text = f"✅ <b>Correct!</b>\n\n{explanation}"
    else:
        correct_opt = question["options"].get(lang)[question["correct"]]
        result_text = f"❌ <b>Wrong.</b> Correct: <b>{correct_opt}</b>\n\n{explanation}"

    next_index = quiz_index + 1

    if next_index < len(_QUIZ_QUESTIONS):
        await state.update_data(quiz_index=next_index, score=score)
        next_q = _QUIZ_QUESTIONS[next_index]
        next_options = next_q["options"].get(lang, next_q["options"]["en"])
        next_text = next_q["question"].get(lang, next_q["question"]["en"])

        await callback.message.edit_text(
            text=f"{result_text}\n\n❓ <b>{next_text}</b>",
            parse_mode="HTML",
            reply_markup=quiz_answer_keyboard(next_options, next_q["id"], lang),
        )
    else:
        max_score = len(_QUIZ_QUESTIONS)
        await state.set_state(TrainingFlow.quiz_done)
        await db.save_progress(
            callback.from_user.id,
            "quiz_general",
            score=score,
            max_score=max_score,
        )
        await callback.message.edit_text(text=result_text, parse_mode="HTML")
        await send_post_quiz_nudge(callback.message, lang, score, max_score)

    await callback.answer()
