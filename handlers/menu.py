from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import SessionLocal, Account
from engine.reporter import MassReportEngine

router = Router()
db = SessionLocal()
engine = MassReportEngine(db)

@router.message(commands=['start'])
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Login", callback_data="login")
    builder.button(text="🎯 Target", callback_data="target")
    builder.button(text="📊 Active", callback_data="active")
    builder.button(text="🚀 Report", callback_data="report_start")
    builder.adjust(2, 2)
    await message.answer("<b>DeepHat Engine</b>\nSelect Menu:", parse_mode="HTML", reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data == "active")
async def callback_active(callback: types.CallbackQuery):
    count = db.query(Account).filter(Account.is_active == 1).count()
    await callback.message.answer(f"✅ <b='Active'>Accounts:</b> {count}", parse_mode="HTML")

@router.callback_query(lambda c: c.data == "report_start")
async def callback_attack(callback: types.CallbackQuery):
    await callback.message.answer("🚀 Attack Started!")
    asyncio.create_task(engine.attack("target_id_here", "user", "spam"))
