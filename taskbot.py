print("Bot starting...")

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# তোমার API Token
TOKEN = "8126823051:AAHyeJK1ACfn_eE2fOcVLwS89SIjHUk9q5I"

# Stages
PROOF1, PROOF2, PROOF3, PROOF4 = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules = """📌 কাজের নিয়মাবলী (ভালোভাবে পড়ে তারপর শুরু করুন)

1️⃣ কাজ যাচাইয়ের পর খুব দ্রুতই পেমেন্ট প্রদান করা হবে। 💸
2️⃣ শুধুমাত্র Firefox ব্রাউজার ব্যবহার করে মোবাইল থেকে Sign Up করুন।
3️⃣ ❌ Chrome বা অন্য কোনো ব্রাউজার ব্যবহার করে Sign Up করলে কাজ গ্রহণযোগ্য হবে না।
4️⃣ কাজ অবশ্যই মোবাইল ডিভাইস থেকে সম্পন্ন করতে হবে।
5️⃣ প্রতিটি লিংকে, প্রতি ডিভাইস থেকে শুধু একবারই Sign Up করবেন।

⚠️ গুরুত্বপূর্ণ:
👉 নিয়ম ভঙ্গ করলে কোনো অবস্থাতেই পেমেন্ট প্রদান করা হবে না।
👉 কাজ শুরু করার আগে নির্দেশনাগুলো ভালোভাবে পড়ে নিন।

লিংকটি কপি করুন 👉 https://t.co/CZNr999lyj

📞 যোগাযোগ: WhatsApp +8801326585409
"""
    await update.message.reply_text(rules)

async def submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Screenshot 1 দিন (Clear Browser Proof)")
    return PROOF1

async def proof1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["proof1"] = update.message.photo[-1].file_id
    await update.message.reply_text("✅ Screenshot 1 পাওয়া গেছে!\nএখন Screenshot 2 দিন (Link Paste Proof)")
    return PROOF2

async def proof2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["proof2"] = update.message.photo[-1].file_id
    await update.message.reply_text("✅ Screenshot 2 পাওয়া গেছে!\nএখন Screenshot 3 দিন (Form Fill Proof)")
    return PROOF3

async def proof3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["proof3"] = update.message.photo[-1].file_id
    await update.message.reply_text("✅ Screenshot 3 পাওয়া গেছে!\nএখন Screenshot 4 দিন (Profile Complete Proof)")
    return PROOF4

async def proof4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["proof4"] = update.message.photo[-1].file_id
    admin_id = 5825915140  # তোমার ID
    user = update.message.from_user
    await context.bot.send_message(chat_id=admin_id, text=f"🔔 নতুন কাজ জমা দিয়েছে: @{user.username} (ID: {user.id})")
    for i in range(1, 5):
        await context.bot.send_photo(chat_id=admin_id, photo=context.user_data[f"proof{i}"])
    await update.message.reply_text("✅ সব Screenshot জমা হয়েছে! 12-24 ঘণ্টার মধ্যে Payment পাবেন।")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Submission বাতিল হয়েছে।")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("submit", submit)],
        states={
            PROOF1: [MessageHandler(filters.PHOTO, proof1)],
            PROOF2: [MessageHandler(filters.PHOTO, proof2)],
            PROOF3: [MessageHandler(filters.PHOTO, proof3)],
            PROOF4: [MessageHandler(filters.PHOTO, proof4)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    print("Bot is connecting to Telegram...")

    app = Application.builder().token(TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, proof1))

    print("Bot is running...")
    app.run_polling()

