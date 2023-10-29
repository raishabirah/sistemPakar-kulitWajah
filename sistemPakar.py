condition_list = []
condition_symptoms = []

# def preprocess():
#     global condition_list, condition_symptoms
#     condition = open("kondisi_wajah.txt")
#     condition_t = condition.read()
    

# def indentify_condition():
#     symptom_list = []

class Greetings(KnowledgeEngine):
	def _initial_action(self):
		print("")
		print("Halo! Saya adalah Do-bot, Saya akan mendiagnosa kondisi kulit wajah anda!")
		print("Oleh karena itu anda harus menjawab beberapa gejala yang anda alami")
		print("Apakah anda merasakan beberapa gejala dibawah ini(yes/no):")
		print("")

# if __name__ == "__main__":
#     preprocess()