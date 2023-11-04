from experta import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections.abc import Mapping

condition_list = []
face_symptoms = []
symptom_map = {}
d_desc_map = {}
d_treatment_map = {}

def preprocess():
    global condition_list, face_symptoms, symptom_map, d_desc_map, d_treatment_map
    diseases = open("penyakit.txt")
    diseases_t = diseases.read()
    condition_list = diseases_t.split("\n")
    diseases.close()
    for disease in condition_list:
        disease_s_file = open("kondisi wajah/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        s_list = disease_s_data.split("\n")
        face_symptoms.append(s_list)
        symptom_map[tuple(s_list)] = disease  # Change to use tuple as the key
        disease_s_file.close()
        disease_s_file = open("deskripsi kondisi/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        d_desc_map[disease] = disease_s_data
        disease_s_file.close()
        disease_s_file = open("pengobatan/" + disease + ".txt")
        disease_s_data = disease_s_file.read()
        d_treatment_map[disease] = disease_s_data
        disease_s_file.close()

def identify_disease(*arguments):
    symptom_list = []
    for symptom in arguments:
        symptom_list.append(symptom)
    return symptom_map[tuple(symptom_list)]  # Change to use tuple for matching

def get_details(disease):
	return d_desc_map[disease]

def get_treatments(disease):
	return d_treatment_map[disease]

def if_not_matched(disease):
		print("")
		id_disease = disease
		disease_details = get_details(id_disease)
		treatments = get_treatments(id_disease)
		print("")
		print("Kemungkinan penyakit yang kamu miliki adalah %s\n" %(id_disease))

		plt.imshow(mpimg.imread("./img/" + id_disease + ".jpg"))
		plt.title(id_disease)
		plt.axis('off')
		plt.show()

		print("Sedikit deskripsi tentang penyakit yang diberikan :")
		print(disease_details+"\n")
		print("Pengobatan umum dan prosedur yang disarankan oleh dokter adalah :")
		print(treatments+"\n")

class Greetings(KnowledgeEngine):
	@DefFacts()
	def _initial_action(self):
		print("")
		print("Halo! Saya adalah SkinChecker, Saya akan mendiagnosa kondisi kulit wajah anda!")
		print("Oleh karena itu anda harus menjawab beberapa gejala yang anda alami")
		print("Apakah anda merasakan beberapa gejala dibawah ini(yes/no):")
		print("")
		yield Fact(action="find_disease")

	# Gejala
	@Rule(Fact(action='find_disease'), NOT(Fact(kulit_membengkak=W())),salience = 1)
	def symptom_0(self):
		self.declare(Fact(kulit_membengkak=input("Apakah anda mengalami pembengkakan kulit: ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(benjolan_di_kulit=W())),salience = 1)
	def symptom_1(self):
		self.declare(Fact(benjolan_di_kulit=input("Apakah anda mengalami benjolan di kulit: ")))

	# Analisis
	@Rule(Fact(action='find_disease'),Fact(kulit_membengkak="yes"),Fact(benjolan_di_kulit="yes"))
	def disease_0(self):
		self.declare(Fact(disease="Jerawat"))

	# Hasil diagnosa
	@Rule(Fact(action='find_disease'),Fact(disease=MATCH.disease),salience = -998)

	def disease(self, disease):
		print("")
		id_disease = disease
		disease_details = get_details(id_disease)
		treatments = get_treatments(id_disease)
		print("")
		print("Kemungkinan terbesar yang anda alami adalah %s\n" %(id_disease))

		plt.imshow(mpimg.imread("./img/" + id_disease + ".jpg"))
		plt.title(id_disease)
		plt.axis('off')
		plt.show()

		print("Berikut deskripsi singkat dari penyakit yang diberikan :")
		print(disease_details+"\n")
		print("Beberapa pengobatan yang disarankan :")
		print(treatments+"\n")

	@Rule(Fact(action='find_disease'),
		  Fact(kulit_membengkak=MATCH.kulit_membengkak),
		  Fact(benjolan_di_kulit=MATCH.benjolan_di_kulit),
		  NOT(Fact(disease=MATCH.disease)),salience = -999)

	def not_matched(self,kulit_membengkak, benjolan_di_kulit):
		print("\nTidak menemukan penyakit yang sangat pas dengan gejala yang anda alami")
		lis = [kulit_membengkak, benjolan_di_kulit]
		max_count = 0
		max_disease = ""
		for key,val in symptom_map.items():
			count = 0
			temp_list = eval(key)
			for j in range(0,len(lis)):
				if(temp_list[j] == lis[j] and lis[j] == "yes"):
					count = count + 1
			if count > max_count:
				max_count = count
				max_disease = val
		if_not_matched(max_disease)


if __name__ == "__main__":
	preprocess()
	engine = Greetings()
	while(1):
		engine.reset()  # Prepare the engine for the execution.
		engine.run()  # Run it!
		print("Ingin mencoba diagnosa dengan gejala yang lain?")
		if input() == "no":
			exit()
		#print(engine.facts)