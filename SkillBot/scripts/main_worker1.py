
import traceback
import re
import redis
import json
import random
import math
import pymongo
from classifier.binary_classifier import BinaryClassifier
from scripts.aiml_script.start import AimlFunct
from socketIO_client import SocketIO
from copy import deepcopy
from scripts.extractors import Extractors
# from classifier.emo_clff import EmoClf



redis_host = "localhost"
redis_port = 6379
redis_password = ""

class MainWorker:

        def __init__(self):
                self.classifier_obj = BinaryClassifier()
                self.aiml_obj= AimlFunct()
                # self.emotion_obj = EmoClf()
                self.extractor_obj = Extractors()
                with open("./scripts/context_data.json", "r") as fp1:
                        self.context_template = json.load(fp1)
                with open("./scripts/counter.json", "r") as fp2:
                        self.counter = json.load(fp2)
                self.socket_conn = SocketIO("localhost:4201")
                self.mongo_conn = pymongo.MongoClient('mongodb://localhost:27017/')
                self.redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)


        def text_preprocessor(self, chat_text):
                chat_text = re.sub( r" +", " ", re.sub(r"[^a-z0-9]", " ", chat_text, flags=re.IGNORECASE)).lower()
                return chat_text

        def get_context_data(self, user_id):
                user_id = str(user_id)
                if self.redis_conn.exists(user_id):
                        context_data = json.loads(self.redis_conn.get(user_id))
                else:
                        context_data = deepcopy(self.context_template)
                        context_data["session_id"] = user_id
                        self.redis_conn.setex(user_id, 3600, json.dumps(context_data))
                return context_data

        def mongo_db_connct(self, context_data):
                updated = False
                mydb = self.mongo_conn["skill_bot"]
                mycol = mydb["user_details"]
                mydict = {
                        "fname":context_data["context_attrs"]["fname"],
                        "lname":context_data["context_attrs"]["lname"],
                        "email_id":context_data["context_attrs"]["email_id"],
                        "mobile":context_data["context_attrs"]["mobile"]
                        }

                if not mycol.find({"email_id": context_data["context_attrs"]["email_id"]}).count():
                        mycol.insert(mydict)
                        updated = True
                return updated

        def generate_otp(self, channel):
                if channel == "alexa":
                    string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                else:
                    string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

                otp = ""
                length = len(string)
                for i in range(4) :
                        otp += string[math.floor(random.random() * length)]

                return otp

        def counter_logic(self, chat_text, context_data):
                reply_text = ""
                if context_data["current_context"] in self.counter:
                        for param_dct in self.counter[context_data["current_context"]]:
                                tobe_asked = set(list(param_dct.keys()))-set(list(context_data["context_attrs"].keys()))
                                if tobe_asked:

                                        final_param = random.choice(list(tobe_asked))
                                        if final_param == "otp" and context_data["asked_parameter"] not in ["otp"]:
                                                otp_code = self.generate_otp(context_data["channel"])
                                                context_data["context_attrs"]["otp_verification"] = otp_code
                                                self.socket_conn.emit("send_email", otp_code, context_data["context_attrs"]["email_id"])
                                        elif final_param == "perform_demographic_test":
                                                reply_text = self.get_demographic_data(chat_text, context_data)

                                        context_data["asked_parameter"] = final_param
                                        if not reply_text:
                                                reply_text = random.choice(self.counter["responses"]).replace("<<[KEY]>>", final_param)
                                        break
                        else:
                                print("Completed!")
                                if context_data["current_context"] == "user_registration":
                                        context_data["loggedin"] = True
                                        updated = self.mongo_db_connct(context_data)
                                        if updated:
                                                print("Stored")
                                                reply_text = "Now we will direct you to profile page."
                                                context_data = self.context_switching(param_dct, context_data)
                                                reply_text = self.counter_logic(chat_text, context_data)
                                        else:
                                                context_data["context_attrs"]["email_id"] = ""
                                                reply_text = "Your information is not updated as your email id is already registered. Please provide valid email id."
                                else:
                                        import pdb
                                        #pdb.set_trace()
                                        context_data = self.context_switching(param_dct, context_data)

                                        if context_data["current_context"] in ["test_module"]:
                                                import pdb
                                                # #pdb.set_trace()

                                                mydb = self.mongo_conn["sanfoundry"]
                                                mycol = mydb["document_set"]
                                                user_level = context_data["context_attrs"]["level_of_your_language"]
                                                language_to_test = context_data["context_attrs"]["language_to_test"]
                                                if "all_questions" not in context_data["context_attrs"]:
                                                        all_recs = mycol.find({
                                                                        "language" : language_to_test,
                                                                        "level" : user_level
                                                                }).limit(3)
                                                        all_questions = []
                                                        mycol = mydb["question_set"]

                                                        for each in all_recs:
                                                                for each_q in each["questions"]:
                                                                        each_question = mycol.find({"q_id": int(each_q)})[0]
                                                                        del each_question["_id"]
                                                                        each_question["topic_name"] = each["topic"]
                                                                        all_questions.append(each_question)

                                                        context_data["context_attrs"]["all_questions"] = all_questions
                                                else:
                                                        all_questions = context_data["context_attrs"]["all_questions"]

                                                for question_to_ask      in all_questions:
                                                        if "user_answer" not in question_to_ask:
                                                                question_to_ask["user_answer"] = ""
                                                                reply_text = question_to_ask["question"] + "\n".join(question_to_ask["options"])
                                                                context_data["asked_parameter"] = context_data["current_context"]
                                                                break

                                                        elif "user_answer" in question_to_ask and not question_to_ask["user_answer"]:
                                                                question_to_ask["user_answer"] = chat_text
                                                else:
                                                        # reply_text = "Evaluatio to be process"
                                                        reply_text = self.result(all_questions, "level_test")
                                        else:

                                                reply_text, context_data = self.counter_logic(chat_text, context_data)

                return reply_text, context_data

        def socket_receiver(self, *args):

                try:
                        data_dct = args[0]
                        response_text  = ""
                        user_id = data_dct["identifier"]["user_id"]
                        email_id = data_dct["identifier"]["email_id"]
                        chat_text = data_dct["chat_req"]["chat_text"]
                        context_data = self.get_context_data(user_id)
                        context_data["channel"] = data_dct["channel"]
                        if email_id:
                            context_data["context_attrs"]["email_id"] = email_id
                        processed_chat_text = self.text_preprocessor(chat_text)
                        class_dct = self.classifier_obj.tester(processed_chat_text)

                        # if class_dct["label"] == "greeting" and class_dct["score"] > 0.40:
                        #         response_text  =  self.aiml_obj.calling_aiml(processed_chat_text)
                        # if not response_text or (class_dct["label"] == "general" and class_dct["score"] > 0.50):
                        #         response_text  = "TO BE PROCESSED"

                        response_text  =  self.aiml_obj.calling_aiml(processed_chat_text)

                        if not response_text:

                                # emotion_dct = self.emotion_obj.tester(processed_chat_text)
                                if context_data["asked_parameter"]:
                                        if context_data["asked_parameter"] in dir(self.extractor_obj):
                                                context_data = getattr( self.extractor_obj, context_data["asked_parameter"])(chat_text, context_data)


                                if not context_data["loggedin"]:
                                        context_data["current_context"] = "user_registration"
                                        response_text, context_data = self.counter_logic(chat_text, context_data)
                                elif context_data["loggedin"]:
                                        context_data["current_context"] = "user_info"
                                        response_text, context_data = self.counter_logic(chat_text, context_data)
                                else:
                                        response_text  = "TO BE PROCESSED"

                        data_dct["chat_res"]["reply_text"] = response_text

                except Exception as e:
                        print ("Exception in main ", e, traceback.format_exc())
                self.redis_conn.setex(str(user_id), 3600, json.dumps(context_data))
                self.socket_conn.emit("response_to_service", data_dct)


if __name__ == '__main__':
        obj = MainWorker()
        obj.socket_conn.on('message_req_worker', obj.socket_receiver)
        while True:
                obj.socket_conn.wait(seconds=1)
