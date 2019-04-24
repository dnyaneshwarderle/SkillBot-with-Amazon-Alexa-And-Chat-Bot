import math, random 
# from scripts.extractors import Extractors
class OtpGenerater:
	
	def generateOTP(self) : 
		string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		otp = "" 
		length = len(string) 
		for i in range(4) : 
			otp += string[math.floor(random.random() * length)] 
	
		return otp 
  
if __name__ == "__main__":
	obj = OtpGenerater()

	viewOTP = obj.generateOTP()
	print(viewOTP)

	# print("OTP: ", generateOTP()) 