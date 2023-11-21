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
	@Rule(Fact(action='find_disease'), NOT(Fact(tidak_banyak_mengeluarkan_minyak=W())),salience = 1)
	def symptom_0(self):
		self.declare(Fact(tidak_banyak_mengeluarkan_minyak=input("Apakah kulit wajah anda tidak banyak mengeluarkan minyak: ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(kulit_wajah_mudah_berjerawat=W())),salience = 1)
	def symptom_1(self):
		self.declare(Fact(kulit_wajah_mudah_berjerawat=input("Apakah kulit wajah anda mudah berjerawat: ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(pori_wajah_terlihat=W())),salience = 1)
	def symptom_2(self):
		self.declare(Fact(pori_wajah_terlihat=input("Apakah kulit wajah anda pori-porinya terlihat: ")))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(sering_mengalami_gatal=W())),salience = 1)
	def symptom_3(self):
		self.declare(Fact(sering_mengalami_gatal=input("Apakah kulit wajah anda sering mengalami gatal: ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(lembut=W())),salience = 1)
	def symptom_4(self):
		self.declare(Fact(lembut=input("Apakah kulit wajah anda lembut dan halus: ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(bagian_pipi_kering=W())),salience = 1)
	def symptom_5(self):
		self.declare(Fact(bagian_pipi_kering=input("Apakah kulit wajah anda pada bagian pipi kering: ")))

	# Analisis
	@Rule(Fact(action='find_disease'),Fact(tidak_banyak_mengeluarkan_minyak="yes"),Fact(kulit_wajah_mudah_berjerawat="no"), Fact(pori_wajah_terlihat="no"), Fact(sering_mengalami_gatal="no"),Fact(lembut="yes"), Fact(bagian_pipi_kering="no"))
	def disease_0(self):
		self.declare(Fact(disease="normal"))
	@Rule(Fact(action='find_disease'),Fact(tidak_banyak_mengeluarkan_minyak="no"),Fact(kulit_wajah_mudah_berjerawat="yes"), Fact(pori_wajah_terlihat="yes"),Fact(sering_mengalami_gatal="no"),Fact(lembut="no"), Fact(bagian_pipi_kering="no"))
	def disease_1(self):
		self.declare(Fact(disease="Berminyak"))
	@Rule(Fact(action='find_disease'),Fact(tidak_banyak_mengeluarkan_minyak="yes"),Fact(kulit_wajah_mudah_berjerawat="no"), Fact(pori_wajah_terlihat="no"), Fact(sering_mengalami_gatal="no"),Fact(lembut="no"), Fact(bagian_pipi_kering="no"))
	def disease_3(self):
		self.declare(Fact(disease="kering"))
	@Rule(Fact(action='find_disease'),Fact(tidak_banyak_mengeluarkan_minyak="yes"),Fact(kulit_wajah_mudah_berjerawat="no"), Fact(pori_wajah_terlihat="yes"),Fact(sering_mengalami_gatal="yes"),Fact(lembut="no"), Fact(bagian_pipi_kering="no"))
	def disease_4(self):
		self.declare(Fact(disease="sensitive"))
	@Rule(Fact(action='find_disease'),Fact(tidak_banyak_mengeluarkan_minyak="yes"),Fact(kulit_wajah_mudah_berjerawat="yes"), Fact(pori_wajah_terlihat="no"), Fact(sering_mengalami_gatal="no"),Fact(lembut="no"), Fact(bagian_pipi_kering="yes"))
	def disease_5(self):
		self.declare(Fact(disease="kombinasi"))


	# Hasil diagnosa
	@Rule(Fact(action='find_disease'),Fact(disease=MATCH.disease),salience = -998)

	def disease(self, disease):
		print("")
		id_disease = disease
		disease_details = get_details(id_disease)
		treatments = get_treatments(id_disease)
		print("")
		print("Kemungkinan terbesar kondisi yang anda alami adalah %s\n" %(id_disease))

		plt.imshow(mpimg.imread("./img/" + id_disease + ".jpg"))
		plt.title(id_disease)
		plt.axis('off')
		plt.show()

		print("Berikut deskripsi singkat dari kondisi anda:")
		print(disease_details+"\n")
		print("Beberapa pengobatan yang disarankan:")
		print(treatments+"\n")

	@Rule(Fact(action='find_disease'),
		  Fact(tidak_banyak_mengeluarkan_minyak=MATCH.tidak_banyak_mengeluarkan_minyak),
		  Fact(kulit_wajah_mudah_berjerawat=MATCH.kulit_wajah_mudah_berjerawat),
		  Fact(pori_wajah_terlihat=MATCH.pori_wajah_terlihat),
		  Fact(sering_mengalami_gatal=MATCH.sering_mengalami_gatal),
		  Fact(lembut=MATCH.lembut),
		  Fact(bagian_pipi_kering=MATCH.bagian_pipi_kering),
		  NOT(Fact(disease=MATCH.disease)),salience = -999)

	def if_not_matched(self):
		print("Tidak ditemukan kondisi kulit yang cocok dengan wajah anda.\n")

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