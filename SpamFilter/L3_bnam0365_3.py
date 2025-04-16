from SpamFilter.L3_bnam0365_1 import read_train_data_and_stop_words, test


def main():
    spam_filter = read_train_data_and_stop_words("train.txt", "stopwords.txt")
    spam_filter.calculate_probability()
    spam_filter.create_vocabulary()
    test("test.txt", "TEST RESULT", spam_filter)
    test("train.txt", "TRAIN RESULT", spam_filter)


if __name__ == "__main__":
    main()
