import aiml

	# The Kernel object is the public interface to
	# the AIML interpreter.
class AimlFunct:

	def __init__(self):
		self.kernel = aiml.Kernel()
		self.kernel.learn("./scripts/aiml_script/std-startup.xml")
		self.aiml_kernel = self.kernel.respond("load aiml b")

	def calling_aiml(self, user_text):
		
		aiml_response = self.kernel.respond(user_text)
		return aiml_response

