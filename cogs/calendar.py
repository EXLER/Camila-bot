import discord
from discord.ext import commands
import aiosqlite3

from utils import log, validators


class Calendar(commands.Cog):
    """
    Schedule one-time or repeating events.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def schedule(self, ctx, title, group: discord.Role, *, date):
        """Schedule a new event.
        All members of given group will be mentioned in the reminder
        Date format: YYYY-MM-DD hh:mm"""
        if not validators.date_validator(date):
            await ctx.send(
                "❌ Incorrect date format or date is in the past. Please write the date in format: YYYY-MM-DD hh:mm"
            )
            return

        creator_id = ctx.author.id
        async with self.bot.db_holder.db.cursor() as cur:
            try:
                await cur.execute(
                    f'INSERT INTO events VALUES ("{creator_id}", "{title}", "{date}", "{group}")'
                )
                await self.bot.db_holder.db.commit()
                await ctx.send(
                    f"📅 Scheduled event `{title}` for group `{group}` on `{date}`"
                )
            except aiosqlite3.IntegrityError as e:
                log.error(f"Database error on `schedule` command: {e}")
                await ctx.send(
                    "Database error occured while using the `schedule` command."
                )

    @commands.command()
    async def deleteevent(self, ctx, title):
        """Delete an existing event.
           Can only be called by server admin or the event creator"""
        async with self.bot.db_holder.db.cursor() as cur:
            try:
                await cur.execute(
                    f'SELECT creator_id FROM events WHERE event_title="{title}"'
                )
                event = await cur.fetchone()
                if not event:
                    await ctx.send("No event with given title is in the database!")
                    return

                if (
                    ctx.author.id == event[0]
                    or ctx.author.guild_permissions.administrator
                ):
                    await cur.execute(f'DELETE FROM events WHERE event_title="{title}"')
                    await self.bot.db_holder.db.commit()
                    await ctx.send(f"🗑️ Deleted event `{title}`")
                else:
                    await ctx.send(
                        "Only the event creator or the administrator can delete events."
                    )
            except aiosqlite3.IntegrityError as e:
                log.error(f"Database error on `deleteevent` command: {e}")
                await ctx.send(
                    "Database error occured while using the `deleteevent` command."
                )

    @commands.command()
    async def allscheduled(self, ctx):
        """Display all scheduled events in the database"""
        async with self.bot.db_holder.db.cursor() as cur:
            try:
                await cur.execute(f"SELECT * FROM events")
                events = await cur.fetchall()
                if events:
                    msg = "📅 Currently scheduled events:\n"
                    for event in events:
                        creator = self.bot.get_user(event[0])
                        msg += f"`{event[1]}` for group `{event[3]}` on `{event[2]}`, created by: {creator}\n"
                else:
                    msg = "There are no currently scheduled events."

                await ctx.send(msg)
            except aiosqlite3.IntegrityError as e:
                log.error(f"Database error on `schedule` command: {e}")
                await ctx.send(
                    "Database error occured while using the `schedule` command."
                )

    @commands.command()
    async def today(self, ctx):
        """Display events scheduled for today"""
        async with self.bot.db_holder.db.cursor() as cur:
            try:
                await cur.execute(f"SELECT * FROM events")
                events = await cur.fetchall()
                if events:
                    msg = "📅 Today's scheduled events:\n"
                    for event in events:
                        if not validators.check_if_date_is_today(event[2]):
                            continue
                        creator = self.bot.get_user(event[0])
                        msg += f"`{event[1]}` for group `{event[3]}` on `{event[2]}`, created by: {creator}\n"
                else:
                    msg = "There are no currently scheduled events."

                await ctx.send(msg)
            except aiosqlite3.IntegrityError as e:
                log.error(f"Database error on `schedule` command: {e}")
                await ctx.send(
                    "Database error occured while using the `schedule` command."
                )

    @commands.command()
    async def week(self, ctx):
        """Display events scheduled for the next 7 days"""
        async with self.bot.db_holder.db.cursor() as cur:
            try:
                await cur.execute(f"SELECT * FROM events")
                events = await cur.fetchall()
                if events:
                    msg = "📅 Currently scheduled events:\n"
                    for event in events:
                        if not validators.check_if_date_is_this_week(event[2]):
                            continue
                        creator = self.bot.get_user(event[0])
                        msg += f"`{event[1]}` for group `{event[3]}` on `{event[2]}`, created by: {creator}\n"
                else:
                    msg = "There are no currently scheduled events."

                await ctx.send(msg)
            except aiosqlite3.IntegrityError as e:
                log.error(f"Database error on `schedule` command: {e}")
                await ctx.send(
                    "Database error occured while using the `schedule` command."
                )


def setup(bot):
    bot.add_cog(Calendar(bot))
