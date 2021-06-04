from application.helpers import filter_messages

cursed_words = ['bajingan', 'asu', 'bangsat', 'kontol', 'memek', 'ngentot', 'ngewe', 'bencong', 'banci',
                'bego', 'goblok', 'idiot', 'sinting', 'tolol', 'budek', 'bolot', 'setan', 'keparat', 'bejad',
                'gembel', 'brengsek', 'fuck', 'bitch', 'asshole', 'ass', 'dick']

passed_sentence = "!tweeps Menurut kalian mending ambil gap year atau masuk kampus biasa dulu dan tahun depan coba lagi?"

best_case_not_passed = '!tweeps. Idiot kayak gini yang bikin resah warga! Kadang aneh aja kenapa orang-orang kayak gini dibiarin begitu aja'

worst_case_not_passed = '!teeps. Orang kayak gini meresahkan warga! Aneh banget orang-orang kayak gini dibiarin terus. Idiot'


def test_should_pass():

    result = filter_messages(passed_sentence, cursed_words)

    assert result


def test_should_not_pass():
    first = filter_messages(best_case_not_passed, cursed_words)

    second = filter_messages(worst_case_not_passed, cursed_words)

    assert not (first or second)
