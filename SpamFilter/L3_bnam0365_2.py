import enum
import logging
from math import log

logging.basicConfig(
    filename='spam_filter.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)

class SpamPrediction(enum.Enum):
    TN = "ham-ham"
    FN = "ham-spam"
    FP = "spam-ham"
    TP = "spam-spam"

def read_data(filename, stopwords, label):
    data = []
    occurrence = {}
    encodings_to_try = ["utf-8", "cp1252", "iso-8859-1"]
    for enc in encodings_to_try:
        try:
            with open(filename, encoding=enc) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            logging.warning(f"Could not decode {filename} with {enc}, trying next...")
    else:
        logging.error(f"Failed to decode {filename} with known encodings.")
        return
    invalid_characters = ['subject:', '.', ',', ';', '!', '?', '"', '\'', ':', '-', '_', '(', ')', '[', ']', '{', '}',
                          '<', '>', '\\', '/']
    for line in lines:
        parts = line.strip().split(' ')

        for p in parts:
            part = p.lower()
            if part not in stopwords and part not in invalid_characters:
                data.append(part)
                if part not in occurrence:
                    occurrence[part] = 1
                else:
                    occurrence[part] += 1

    return Data(data, label, occurrence)


class SpamFilter:
    def __init__(self, stop_words, alpha=0.1):
        self.data = []
        self.stop_words = stop_words
        self.ham_probability = 0
        self.spam_probability = 0
        self.vocabulary = {}
        self.alpha = alpha
        self.test = []
        self.lambda_val = 0.00000001
        self.number_of_ham = 0
        self.number_of_spam = 0

    def set_alpha(self, alpha):
        self.alpha = alpha

    def add_data(self, data):
        self.data.append(data)

    def calculate_probability(self):
        total = len(self.data)
        spam = 0
        ham = 0

        for d in self.data:
            if d.data_label == "spam":
                spam += 1
            else:
                ham += 1
        self.ham_probability = ham / total
        self.spam_probability = spam / total

    def train(self):
        number_of_spam = 0
        number_of_ham = 0

        for d in self.data:
            for w in d.data:
                if w not in self.vocabulary:
                    self.vocabulary[w] = [0, 0, 0, 0]

                if d.data_label == "ham":
                    self.vocabulary[w][0] += 1
                    number_of_ham += 1
                else:
                    self.vocabulary[w][1] += 1
                    number_of_spam += 1
        self.number_of_ham = number_of_ham
        self.number_of_spam = number_of_spam
        self.recalculate_vocabulary()

    def recalculate_vocabulary(self):
        card_v = len(self.vocabulary)

        for k, v in self.vocabulary.items():
            ham_count = v[0]
            spam_count = v[1]
            self.vocabulary[k][2] = (ham_count + self.alpha) / (self.number_of_ham + card_v * self.alpha)
            self.vocabulary[k][3] = (spam_count + self.alpha) / (self.number_of_spam + card_v * self.alpha)

    def read_test_data(self, filename):
        with open(filename, 'r') as f:
            for l in f:
                line = l.strip()
                parts = line.split(".")
                data_label = parts[-2]
                if data_label == "ham":
                    file_name = f"ham/{line}"
                else:
                    file_name = f"spam/{line}"
                data = read_data(file_name, self.stop_words, data_label)

                self.test.append(data)

    def filter(self, test_data):
        l = log(self.spam_probability) - log(self.ham_probability)
        occurrence = test_data.occurrence
        for t in test_data.data:
            if t in self.vocabulary:
                l += occurrence[t] * (log(max(self.vocabulary[t][3], self.lambda_val)) - log(
                    max(self.vocabulary[t][2], self.lambda_val)))
            # else:
            #     l += occurrence[t] * (log(self.lambda_val) - log(self.lambda_val))
        return l

    def calculate_accuracy(self):
        confusion_matrix = {
            SpamPrediction.TN: 0,
            SpamPrediction.FN: 0,
            SpamPrediction.FP: 0,
            SpamPrediction.TP: 0
        }

        for t in self.test:
            value = self.filter(t)

            if value >= 0:
                predicted_label = "spam"
            else:
                predicted_label = "ham"

            if predicted_label == "spam" and t.data_label == "spam":
                confusion_matrix[SpamPrediction.TP] += 1
            elif predicted_label == "ham" and t.data_label == "ham":
                confusion_matrix[SpamPrediction.TN] += 1
            elif predicted_label == "spam" and t.data_label == "ham":
                confusion_matrix[SpamPrediction.FP] += 1
            elif predicted_label == "ham" and t.data_label == "spam":
                confusion_matrix[SpamPrediction.FN] += 1

        return confusion_matrix

class Data:
    def __init__(self, data, label, occurrence):
        self.data = data
        self.data_label = label
        self.occurrence = occurrence

    def __repr__(self):
        return f"Data({self.data_label}, {self.data})"
