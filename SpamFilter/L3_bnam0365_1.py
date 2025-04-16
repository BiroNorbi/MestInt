from SpamFilter.L3_bnam0365_2 import SpamFilter, read_data


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
    print(f"______________________{placeholder}______________________")

    for alpha in alphas:
        spam_filter.set_alpha(alpha)
        accuracy = spam_filter.calculate_accuracy()
        print(f"Alpha: {alpha}, Accuracy: {accuracy:.4f}%")
