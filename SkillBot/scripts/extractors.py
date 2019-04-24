import re
# from scripts.otp_py import GenerateOTP

class Extractors:

    def __init__(self):
        pass


    def email_id(self, chat_text, context_data):
        search_rex = re.search(r"[\w\.-]+@[\w\.-]+", chat_text)
        if search_rex:
            context_data["context_attrs"]["email_id"] = search_rex.group()
        # otp = self.otp_obj.GenerateOTP
        return context_data

    def fname(self, chat_text, context_data):
        context_data["context_attrs"]["fname"] = chat_text
        return context_data

    def lname(self, chat_text, context_data):
        context_data["context_attrs"]["lname"] = chat_text
        return context_data

    def language_to_test(self, chat_text, context_data):
        laguages = ["python"]
        if chat_text.lower() in laguages:
            context_data["context_attrs"]["language_to_test"] = chat_text.lower()
        return context_data

    def level_of_your_language(self, chat_text, context_data):
        levels = ["begineer", "intermediate", "advanced"]
        if chat_text.lower() in levels:
            context_data["context_attrs"]["level_of_your_language"] = chat_text.lower()
        return context_data

    def mobile(self, chat_text, context_data):
        context_data["context_attrs"]["mobile"] = chat_text
        return context_data

    def otp(self, chat_text, context_data):
        # import pdb
        # pdb.set_trace()
        otp_data = context_data["context_attrs"]["otp_verification"]
        search_rex = re.search(otp_data, chat_text, flags=re.IGNORECASE)
        if search_rex:
            context_data["context_attrs"]["otp"] = search_rex.group()
            print("Please enter correct otp")
        return context_data

    # def programming_languages_known(self, chat_text, context_data):
    #     context_data["context_attrs"]["programming_languages_known"] = chat_text
    #     return context_data

    # def programming_languages_2learn(self, chat_text, context_data):
    #     context_data["context_attrs"]["moprogramming_languages_2learn"] = chat_text
    #     return context_data
