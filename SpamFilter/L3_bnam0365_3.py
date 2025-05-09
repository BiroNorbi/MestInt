from SpamFilter.L3_bnam0365_1 import read_train_data_and_stop_words, test


def test_accuracy():
    spam_filter = read_train_data_and_stop_words("train.txt", "stopwords.txt")
    spam_filter.calculate_probability()
    spam_filter.train()
    spam_filter.recalculate_vocabulary()

    test("test.txt", "TEST RESULT", spam_filter)
    test("train.txt", "TRAIN RESULT", spam_filter)

def test_cross_validation():
    print("______________________CROSS VALIDATION______________________")
    spam_filter = read_train_data_and_stop_words("train.txt", "stopwords.txt")
    spam_filter.calculate_probability()
    spam_filter.train()
    spam_filter.recalculate_vocabulary()

    _ = spam_filter.cross_validation(interval=10)

def test_semi_supervised_learning():
    spam_filter = read_train_data_and_stop_words("train.txt", "stopwords.txt")
    spam_filter.calculate_probability()
    spam_filter.train()
    spam_filter.recalculate_vocabulary()

    test("test.txt", "TEST RESULT BEFORE SEMI SUPERVISED LEARNING", spam_filter)

    spam_filter.semi_supervised_learning()

    test("test.txt", "TEST RESULT AFTER SEMI SUPERVISED LEARNING", spam_filter)

def main(accuracy=True, cross_validation=True, semi_supervised_learning=True):
    if accuracy:
        test_accuracy()
    if cross_validation:
        test_cross_validation()
    if semi_supervised_learning:
        test_semi_supervised_learning()



if __name__ == "__main__":
    main(
        accuracy=True,
        cross_validation=True,
        semi_supervised_learning=True,
    )
