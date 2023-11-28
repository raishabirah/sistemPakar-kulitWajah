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
		print("Halo! Saya adalah SkinChecker, Saya akan melakukan diagnosa kondisi kulit wajah anda!")
		print("Oleh karena itu anda harus menjawab beberapa pertanyaan mengenai gejala yang anda alami")
		print("Apakah anda merasakan beberapa gejala dibawah ini(yes/no):")
		print("")
		yield Fact(action="find_disease")

	# Gejala
	@Rule(Fact(action='find_disease'), NOT(Fact(kulit_berminyak=W())),salience = 1)
	def symptom_0(self):
		self.declare(Fact(kulit_berminyak=input("Apakah kulit wajah anda mengeluarkan banyak minyak? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(mudah_berjerawat=W())),salience = 1)
	def symptom_1(self):
		self.declare(Fact(mudah_berjerawat=input("Apakah kulit wajah anda mudah berjerawat? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(pori_terlihat=W())),salience = 1)
	def symptom_2(self):
		self.declare(Fact(pori_terlihat=input("Apakah kulit wajah anda pori-porinya terlihat? ")))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(gatal=W())),salience = 1)
	def symptom_3(self):
		self.declare(Fact(gatal=input("Apakah kulit wajah anda sering mengalami gatal? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(merah=W())),salience = 1)
	def symptom_4(self):
		self.declare(Fact(merah=input("Apakah kulit wajah anda sering merah-merah? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(tzone_berminyak=W())),salience = 1)
	def symptom_5(self):
		self.declare(Fact(tzone_berminyak=input("Apakah dagu, hidung, dan dahi anda mengeluarkan minyak? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(kencang=W())),salience = 1)
	def symptom_6(self):
		self.declare(Fact(kencang=input("Apakah kulit wajah anda terasa kencang atau tertarik? ")))
	
	@Rule(Fact(action='find_disease'), NOT(Fact(kulit_terkelupas=W())),salience = 1)
	def symptom_7(self):
		self.declare(Fact(kulit_terkelupas=input("Apakah kulit wajah anda terkelupas? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(lembut=W())),salience = 1)
	def symptom_8(self):
		self.declare(Fact(lembut=input("Apakah kulit wajah anda lembut dan halus? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(kusam_tekstur=W())),salience = 1)
	def symptom_9(self):
		self.declare(Fact(kusam_tekstur=input("Apakah kulit wajah anda kusam dan bertekstur? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(lembab=W())),salience = 1)
	def symptom_10(self):
		self.declare(Fact(lembab=input("Apakah kulit wajah anda terasa lembab? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(pipi_kering=W())),salience = 1)
	def symptom_11(self):
		self.declare(Fact(pipi_kering=input("Apakah kulit wajah anda pada bagian pipi kering? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(sensitif_debu=W())),salience = 1)
	def symptom_12(self):
		self.declare(Fact(sensitif_debu=input("Apakah kulit wajah anda sensitif terhadap debu? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(kering=W())),salience = 1)
	def symptom_13(self):
		self.declare(Fact(kering=input("Apakah kulit wajah anda terasa kering? ")))

	@Rule(Fact(action='find_disease'), NOT(Fact(lengket=W())),salience = 1)
	def symptom_14(self):
		self.declare(Fact(lengket=input("Apakah kulit wajah anda terasa lengket? ")))

	# Analisis
	@Rule(Fact(action='find_disease'),Fact(kulit_berminyak="no"), Fact(mudah_berjerawat="no"), Fact(pori_terlihat="no"), Fact(gatal="no"), Fact(merah="no"), Fact(tzone_berminyak="no"), Fact(kencang="no"), Fact(kulit_terkelupas="no"), Fact(lembut="yes"), Fact(kusam_tekstur="no"), Fact(lembab="yes"), Fact(pipi_kering="no"), Fact(sensitif_debu="no"), Fact(kering="no"), Fact(lengket="no"))
	def disease_0(self):
		self.declare(Fact(disease="normal"))
	@Rule(Fact(action='find_disease'),Fact(kulit_berminyak="yes"), Fact(mudah_berjerawat="yes"), Fact(pori_terlihat="yes"),Fact(gatal="no"), Fact(merah="no"), Fact(tzone_berminyak="no"), Fact(kencang="no"), Fact(kulit_terkelupas="no"), Fact(lembut="no"), Fact(kusam_tekstur="no"), Fact(lembab="no"), Fact(pipi_kering="no"), Fact(sensitif_debu="no"), Fact(kering="no"), Fact(lengket="yes"))
	def disease_1(self):
		self.declare(Fact(disease="berminyak"))
	@Rule(Fact(action='find_disease'),Fact(kulit_berminyak="no"), Fact(mudah_berjerawat="no"), Fact(pori_terlihat="no"), Fact(gatal="yes"), Fact(merah="yes"), Fact(tzone_berminyak="no"), Fact(kencang="yes"), Fact(kulit_terkelupas="yes"), Fact(lembut="no"), Fact(kusam_tekstur="yes"), Fact(lembab="no"), Fact(pipi_kering="no"), Fact(sensitif_debu="no"), Fact(kering="yes"), Fact(lengket="no"))
	def disease_3(self):
		self.declare(Fact(disease="kering"))
	@Rule(Fact(action='find_disease'),Fact(kulit_berminyak="no"), Fact(mudah_berjerawat="no"), Fact(pori_terlihat="yes"),Fact(gatal="yes"), Fact(merah="yes"), Fact(tzone_berminyak="no"), Fact(kencang="yes"), Fact(kulit_terkelupas="no"), Fact(lembut="no"), Fact(kusam_tekstur="no"), Fact(lembab="no"), Fact(pipi_kering="no"), Fact(sensitif_debu="no"), Fact(kering="no"), Fact(lengket="no"))
	def disease_4(self):
		self.declare(Fact(disease="sensitive"))
	@Rule(Fact(action='find_disease'),Fact(kulit_berminyak="no"), Fact(mudah_berjerawat="yes"), Fact(pori_terlihat="no"), Fact(gatal="no"),Fact(merah="no"), Fact(tzone_berminyak="yes"), Fact(kencang="no"), Fact(kulit_terkelupas="no"), Fact(lembut="no"), Fact(kusam_tekstur="no"), Fact(lembab="no"), Fact(pipi_kering="yes"), Fact(sensitif_debu="yes"), Fact(kering="no"), Fact(lengket="no"))
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

		print("Sedikit deskripsi mengenai kondisi wajah anda:")
		print(disease_details+"\n")
		print("Beberapa perawatan kulit yang disarankan:")
		print(treatments+"\n")

	@Rule(Fact(action='find_disease'),
		  Fact(kulit_berminyak=MATCH.kulit_berminyak),
		  Fact(mudah_berjerawat=MATCH.mudah_berjerawat),
		  Fact(pori_terlihat=MATCH.pori_terlihat),
		  Fact(gatal=MATCH.gatal),
		  Fact(merah=MATCH.merah),
		  Fact(tzone_berminyak=MATCH.tzone_berminyak),
		  Fact(kencang=MATCH.kencang),
		  Fact(kulit_terkelupas=MATCH.kulit_terkelupas),
		  Fact(lembut=MATCH.lembut),
		  Fact(kusam_tekstur=MATCH.kusam_tekstur),
		  Fact(lembab=MATCH.lembab),
		  Fact(pipi_kering=MATCH.pipi_kering),
		  Fact(sensitif_debu=MATCH.sensitif_debu),
		  Fact(kering=MATCH.kering),
		  Fact(lengket=MATCH.lengket),
		  NOT(Fact(disease=MATCH.disease)),salience = -999)

	def if_not_matched(self):
		print("Tidak ditemukan kondisi kulit yang cocok dengan wajah anda.\n")

if __name__ == "__main__":
	preprocess()
	engine = Greetings()
	while(1):
		engine.reset()  # Prepare the engine for the execution.
		engine.run()  # Run it!
		print("Apakah anda ngin mencoba diagnosa dengan gejala yang lain?")
		if input() == "no":
			exit()
		#print(engine.facts)