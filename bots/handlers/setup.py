from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database import update_target_folder, update_gpt_request, get_gpt_request
from bots.telethon_service import analyze_folder
from bots.filters.isAdmin import IsAdmin
from geminiapi import generate_text

setup_router = Router()


class Form(StatesGroup):
    wait_for_folder_name = State()
    wait_for_survey_time = State()
    wait_for_gpt_request = State()


@setup_router.message(F.text == "Analyze now", IsAdmin())
async def analyze_now_command(message: types.Message):
    await message.answer("Starting analysis now...")
    user_id = message.from_user.id

    result = await analyze_folder(user_id)
    if not result or result.get("status") != "ok":
        await message.answer("No chats found in the selected folder or analysis failed.")
        return

    # Flatten a limited number of recent messages into context
    lines = []
    for chat_id, items in result.get("data", {}).items():
        if isinstance(items, dict) and items.get("error"):
            continue
        for msg in items or []:
            text = msg.get("text", "")
            date = msg.get("date", "")
            lines.append(f"[{chat_id} {date}] {text}")

    if not lines:
        await message.answer("No recent messages to analyze.")
        return

    context_text = "\n".join(lines)
    gpt_req = await get_gpt_request(user_id) or "Summarize the key topics discussed and actionable insights."
    prompt = f"{gpt_req}\n\nContext:\n{context_text}"

    try:
        resp = await generate_text(prompt, await get_gpt_request(user_id))
    except Exception as e:
        await message.answer(f"Gemini error: {e}")
        return

    if not isinstance(resp, str):
        resp = str(resp)

    # Respect Telegram message length limits
    max_len = 4000
    if len(resp) > max_len:
        resp = resp[: max_len - 20] + "\n... [truncated]"

    await message.answer(resp)


@setup_router.message(F.text == "Choose folder", IsAdmin())
async def setup_folder_command(message: types.Message, state: FSMContext):
    await state.set_state(Form.wait_for_folder_name)
    await message.answer("Enter the name of the folder to configure:")


@setup_router.message(Form.wait_for_folder_name, IsAdmin())
async def process_folder_name(message: types.Message, state: FSMContext):
    folder_name = message.text
    await update_target_folder(message.from_user.id, folder_name)
    await message.answer(f"The folder '{folder_name}' has been successfully selected for configuration.")
    await state.clear()


@setup_router.message(F.text == "Configure GPT Request", IsAdmin())
async def setup_gpt_request_command(message: types.Message, state: FSMContext):
    await state.set_state(Form.wait_for_gpt_request)
    await message.answer("Enter the new GPT request:")


@setup_router.message(Form.wait_for_gpt_request, IsAdmin())
async def process_gpt_request(message: types.Message, state: FSMContext):
    gpt_request = message.text
    await update_gpt_request(message.from_user.id, gpt_request)
    await message.answer("The GPT request has been successfully updated.")
    await state.clear()
