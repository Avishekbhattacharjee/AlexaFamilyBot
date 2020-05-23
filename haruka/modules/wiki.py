__help__ = """
 - /wiki text: Returns search from wikipedia for the input text
"""
__mod_name__ = "Wikipedia"
WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki, pass_args=True)
dispatcher.add_handler(WIKI_HANDLER)
