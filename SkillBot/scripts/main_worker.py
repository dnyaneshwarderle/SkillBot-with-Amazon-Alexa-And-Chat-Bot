
import traceback
import re
import redis
import json
import random
import math
import pymongo
from classifier.binary_classifier1 import BinaryClassifier
# from classifier.testing_classifier import TestingClassifier
from scripts.aiml_script.start import AimlFunct
from socketIO_client import SocketIO
from copy import deepcopy
from scripts.extractors import Extractors
import pdb
# from classifier.emo_clff import EmoClf



redis_host = "localhost"
redis_port = 6379
redis_password = ""

class MainWorker:

        def __init__(self):
                self.classifier_obj = BinaryClassifier()
                # self.classifier_testing_obj = TestingClassifier()
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
                mydb = self.mongo_conn["skill_bot1"]
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

        def generate_otp(self):
                if channel == "alexa":
                    string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                else:
                    string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                otp = ""
                length = len(string)
                for i in range(4) :
                        otp += string[math.floor(random.random() * length)]

                return otp

        def context_switching(self, param_dct, context_data):
                if param_dct.values() and "switch_context" in list(param_dct.values())[0]:
                        context_data["current_context"] = list(param_dct.values())[0]["switch_context"]
                return context_data

        def get_demographic_data(self, chat_text, context_data):
                import pdb
                # pdb.set_trace()
                language_to_test = context_data["context_attrs"]["language_to_test"]
                if "all_demographic_questions" not in context_data["context_attrs"]:
                        mydb = self.mongo_conn["sanfoundry"]
                        mycol = mydb["demographics"]
                        all_recs = mycol.find({
                                        "language" : language_to_test
                                })

                        all_questions = []


                        for each_q in all_recs:
                                del each_q["_id"]
                                all_questions.append(each_q)

                        context_data["context_attrs"]["all_demographic_questions"] = all_questions
                else:
                        all_questions = context_data["context_attrs"]["all_demographic_questions"]

                for question_to_ask  in all_questions:
                        if "user_answer" not in question_to_ask:
                                question_to_ask["user_answer"] = ""
                                reply_text = question_to_ask["question"] + "\n".join(question_to_ask["options"])
                                context_data["asked_parameter"] = context_data["current_context"]
                                break

                        elif "user_answer" in question_to_ask and not question_to_ask["user_answer"]:
                                question_to_ask["user_answer"] = chat_text
                else:
                        # reply_text = "Evaluatio to be process"
                        reply_text = self.result(all_questions,"demographic", context_data)
                        context_data["asked_parameter"] = ""
                # else:
                #          reply_text = self.counter_logic(chat_text, context_data)

                return reply_text, context_data

        def perform_test(self, context_data):
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
                        reply_text = self.result(all_questions, "level_test", context_data)
                        context_data["current_context"] = ""

                return reply_text, context_data


        def counter_logic(self, chat_text, context_data,email_id):
                reply_text = ""
                print("====",email_id)
                if context_data["current_context"] in self.counter:
                        for param_dct in self.counter[context_data["current_context"]]:
                                tobe_asked = set(list(param_dct.keys()))-set(list(context_data["context_attrs"].keys()))
                                if tobe_asked:

                                        final_param = random.choice(list(tobe_asked))
                                        if final_param not in context_data["attrs_count"]:
                                                context_data["attrs_count"][final_param] = 0

                                        context_data["attrs_count"][final_param] +=1
                                        context_data["asked_parameter"] = final_param
                                        if final_param == "otp" and context_data["asked_parameter"] not in ["otp"]:
                                                otp_code = self.generate_otp(context_data["channel"])
                                                context_data["context_attrs"]["otp_verification"] = otp_code
                                                self.socket_conn.emit("send_email", otp_code, context_data["context_attrs"]["email_id"])
                                        elif final_param == "perform_demographic_test":
                                                reply_text, context_data = self.get_demographic_data(chat_text, context_data)


                                        if not reply_text:
                                                reply_text = random.choice(self.counter["responses"]).replace("<<[KEY]>>", final_param)
                                        break
                        else:
                                print("Completed!")
                                if context_data["current_context"] == "user_login":
                                        mydb = self.mongo_conn["skill_bot"]
                                        mycol = mydb["user_details"]
                                        print("====",email_id)
                                        context_data["context_attrs"]["email_id"]=email_id
                                        all_email = mycol.find({"email_id" : email_id})

                                        if not all_email.count() and context_data["attrs_count"]["email_id"] == 1:
                                                context_data["attrs_count"]["email_id"]+=1
                                                reply_text = "Either your email id {} is wrong or not updated in my database. Please provide me your correct email id.".format(context_data["context_attrs"]["email_id"])
                                                del context_data["context_attrs"]["email_id"]
                                        elif not all_email.count() :
                                                context_data["current_context"] = "user_registration"
                                                reply_text, context_data = self.counter_logic(chat_text, context_data,email_id)
                                        elif all_email.count():
                                                context_data["loggedin"] = True
                                                reply_text = "Welcome again {}".format(all_email[0]["fname"])

                                elif context_data["current_context"] == "user_registration":
                                        context_data["loggedin"] = True
                                        updated = self.mongo_db_connct(context_data)
                                        if updated:
                                                print("Stored")
                                                reply_text = "Now we will direct you to profile page."
                                                context_data = self.context_switching(param_dct, context_data)
                                                reply_text, context_data = self.counter_logic(chat_text, context_data)
                                else:
                                        context_data = self.context_switching(param_dct, context_data)

                                        if context_data["current_context"] in ["test_module"]:
                                                import pdb
                                                # #pdb.set_trace()
                                                reply_text, context_data = self.perform_test(context_data)
                                        else:
                                                reply_text, context_data = self.counter_logic(chat_text, context_data,email_id)

                return reply_text, context_data

        def result(self, all_questions, type_of_process, context_data):
                import pdb
                # pdb.set_trace()
                list_of_wrong_q = []
                question_list = []
                all_demographics = []
                global check
                reply_text = ""
                cntr = 0
                line = "your score is :"

                for each_question in all_questions:
                        if each_question["user_answer"] == "a":
                                check = 0
                        elif each_question["user_answer"] == "b":
                                check = 1
                        elif each_question["user_answer"] == "c":
                                check = 2
                        elif each_question["user_answer"] == "d":
                                check = 3
                        else:
                                check = "NOT_FOUND"

                        if type_of_process == "level_test":
                                if check == each_question["answer"]["index"]:
                                        cntr += 1
                                elif check !=  each_question["answer"]["index"]:
                                        # print("--->",each_question)
                                        list_of_wrong_q.append(each_question["q_id"])
                                        # print(list_of_wrong_q)
                                        # mycol = mydb["document_set"]

                        elif type_of_process == "demographic":
                                if check != "NOT_FOUND":
                                        weight = each_question["weightage"][check]
                                        all_demographics.append(weight)

                if type_of_process == "level_test":
                        reply_text = line + str(cntr)
                elif type_of_process == "demographic":
                        final_score = sum(all_demographics)/len(all_demographics)

                        if final_score >= 2 and final_score < 4:
                                context_data["context_attrs"]["level_of_your_language"] = "begineer"
                                reply_text = "It seems your are new to {}".format(each_question["language"])
                        elif final_score >=4 and final_score < 6:
                                context_data["context_attrs"]["level_of_your_language"] = "intermediate"
                                rattrs_counteply_text = "I am happy that you are already aware of {}".format(each_question["language"])
                        elif final_score >=6 and final_score <=8:
                                context_data["context_attrs"]["level_of_your_language"] = "advanced"
                                reply_text = "Excellent! Lets play with your intelligence.{}".format(each_question["language"])
                        else:
                                context_data["context_attrs"]["level_of_your_language"] = "begineer"
                                reply_text = "It seems your are new to {}".format(each_question["language"])
                        reply_text+= " What do you want Test or Learn. Type 'I want to learn' or 'I want to take a test'"

                # mydb = self.mongo_conn["sanfoundry"]
                # mycol = mydb["document_set"]
                # all_rec = mycol.find()
                # for each_rec in all_rec:
                #         question_list.append(each_rec["questions"])
                #         # for each_id in question_list:
                #         #         print(each_id)
                # for each_list in question_list:
                #         for each_id in each_list:
                #                 for each_wrong in list_of_wrong_q:
                #                         if each_id == each_wrong:
                #                                 print("wronnnnnggggg", each_wrong)


                # # for each_wron_q in list_of_wrong_q:
                # #         if each_wron_q == mycol.find()
                # print("wong list",list_of_wrong_q)
                # print("result",cntr)
                return reply_text, context_data

        def socket_receiver(self, *args):

                try:
                        import pdb
                        # pdb.set_trace()
                        class_dct = {}
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


                        if context_data["asked_parameter"] in ["test_module"]:
                                if chat_text in ["a", "b", "c", "d"]:
                                        response_text, context_data = self.counter_logic(chat_text, context_data,email_id)

                        # emotion_dct = self.emotion_obj.tester(processed_chat_text)
                        if context_data["asked_parameter"]:
                                if context_data["asked_parameter"] in dir(self.extractor_obj):
                                        context_data = getattr( self.extractor_obj, context_data["asked_parameter"])(chat_text, context_data)

                        if not response_text:
                                if not context_data["asked_parameter"]:
                                        class_dct = self.classifier_obj.tester(processed_chat_text)
                                        if class_dct["label"] == "greeting" and class_dct["score"] > 0.40:
                                                response_text  =  self.aiml_obj.calling_aiml(processed_chat_text)
                                else:
                                         class_dct = {}
                                if not response_text:
                                        if not context_data["loggedin"]:
                                                context_data["current_context"] = "user_login"
                                                response_text, context_data = self.counter_logic(chat_text, context_data,email_id)
                                        elif context_data["loggedin"]:
                                                if not class_dct:
                                                        response_text, context_data = self.counter_logic(chat_text, context_data,email_id)
                                                elif class_dct["label"] == "general" and class_dct["score"] > 0.50:
                                                        response_text  = "TO BE PROCESSED"
                                                elif class_dct["label"] == "learn" and class_dct["score"] > 0.50:
                                                        pass
                                                elif class_dct["label"] == "test" and class_dct["score"] > 0.50:
                                                        context_data["current_context"] = "learn_module"
                                                        reply_text, context_data = self.perform_test(context_data)



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

        # while True:
        #         data_dct = {
        #                 "name" : {
        #                         "first_name": "",
        #                         "middle_name": "",
        #                         "last_name": "",
        #                         "mob": ""
        #                 },
        #                 "identifier":{
        #                         "user_id": "",
        #                         "session_id": "",
        #                         "location": "",
        #                         "channel_id": "",
        #                         "group_id": "",
        #                         "team_id": "",
        #                         "email_id":"",
        #                         "user_specified_id":{

        #                         "userdata": ""
        #                         }
        #                 },
        #                 "time":{
        #                         "time_zone": ""
        #                 },
        #                 "chat_req": {
        #                         "message_id": "3",
        #                         "chat_text": input("Q: "),
        #                         "chat_type": "message",
        #                         "chat_timestamp": ""
        #                 },
        #                 "chat_res":{
        #                         "reply_id": "",
        #                         "reply_text": "",
        #                         "reply_timestamp": "",
        #                         "additional_param":{
        #                         },
        #                         "reply_action": ""
        #                 },
        #                 "channel": ""
        #         }
        #         out = obj.main(data_dct)
        #         print ("Response: ", out["chat_res"]["reply_text"])
