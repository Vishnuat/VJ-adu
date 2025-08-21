

import datetime
from pyrogram import Client, filters
from database.users_chats_db import db

@Client.on_message(filters.command("trending"))
async def trending_command(client, message):
    """
    Handles the /trending command to show a list of top 10 trending movies for the day.
    """
    try:
        # Get the current date
        today = datetime.date.today().strftime("%d %B %Y")

        # Start building the response message
        response_text = f"🎬 **Trending Movies - {today}**\n\n"

        # Get trending movies from the database
        trending_movies = await db.get_trending_movies()
        trending_list = [movie async for movie in trending_movies]

        if not trending_list:
            response_text += "No trending movies found for today."
        else:
            # Loop through the movie data and format it
            for i, movie in enumerate(trending_list, 1):
                title = movie["query"]
                count = movie["count"]
                response_text += f"**{i}. {title}** - Searched {count} times\n"

        # Send the response
        await message.reply_text(response_text)
    except Exception as e:
        await message.reply_text("Sorry, something went wrong while fetching trending movies.")
        print(f"Error in /trending command: {e}")
