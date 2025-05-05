from SpamFilter.L3_bnam0365_2 import SpamFilter, read_data, SpamPrediction


def read_train_data_and_stop_words(train, stop_words_file):
    stop_words = set()

    with open(stop_words_file) as f:
        for line in f:
            stop_words.add(line.strip())

    spam_filter = SpamFilter(stop_words=stop_words)
    with open(train, 'r') as f:
        for l in f:
            line = l.strip()
            parts = line.split(".")
            data_label = parts[-2]
            if data_label == "ham":
                file_name = f"ham/{line}"
            else:
                file_name = f"spam/{line}"
            data = read_data(file_name, stop_words, data_label)

            spam_filter.add_data(data)

    return spam_filter


def test(filename, placeholder, spam_filter):
    alphas = [0.01, 0.1, 1]

    spam_filter.read_test_data(filename)
    spam_filter.train()
    spam_filter.calculate_probability()

    print(f"______________________{placeholder}______________________")

    for alpha in alphas:
        spam_filter.set_alpha(alpha)
        spam_filter.recalculate_vocabulary()
        confusion_matrix = spam_filter.calculate_accuracy()

        fn = confusion_matrix[SpamPrediction.FN]
        fp = confusion_matrix[SpamPrediction.FP]
        tn = confusion_matrix[SpamPrediction.TN]
        tp = confusion_matrix[SpamPrediction.TP]

        q = fp / fn
        all_sum = fp + fn + tn + tp
        accuracy = (tp + tn) / all_sum
        print(f"Alpha: {alpha}, Accuracy: {accuracy * 100:.4f}")
        if placeholder == "TEST RESULT":
            print(f"FP ratio: {(fp * 100) / all_sum:.4f}, FN ratio: {(fn * 100) / all_sum:.4f}, FP/FN ratio: {q:.4f}")
            print(f"""
                   Predicted
                  0       1
               +-------+-------+
    Actual  0 |  {tp:<5} |  {fn:<5} |
               +-------+-------+
            1 |  {fp:<5} |  {tn:<5} |
               +-------+-------+
    """)