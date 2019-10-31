# Default pattern Tests
# Correct pattern: 2019/1/30（水）0:00


from text_verifier import TextVerifier

def test_success():
    err_list = []
    text_verifier = TextVerifier()

    err_list += text_verifier.verify_text('2016/2/29（月）23:59')
    err_list += text_verifier.verify_text('2016/3/1（火）23:59')
    err_list += text_verifier.verify_text('2019/10/15（火）0:00')
    
    assert len(err_list) == 0


def test_failed_date_format1():
    assert 1 == len(TextVerifier().verify_text('２０１６/2/29（月）23:59'))
def test_failed_date_format2():
    assert 1 == len(TextVerifier().verify_text('2016/２/29（月）23:59'))
def test_failed_date_format3():
    assert 1 == len(TextVerifier().verify_text('2016/2/２9（月）23:59'))
def test_failed_date_format4():
    assert 1 == len(TextVerifier().verify_text('2016/2/29(月)23:59'))
def test_failed_date_format5():
    assert 1 == len(TextVerifier().verify_text('2016/2/29（月）23：59'))
def test_failed_date_format6():
    assert 1 == len(TextVerifier().verify_text('2016/2/29 (月) 23：59'))

def test_failed_date_ng_list1():
    assert 1 == len(TextVerifier().verify_text('2/29（月）23:59'))
def test_failed_date_ng_list2():
    assert 1 == len(TextVerifier().verify_text('<br>2/29（月）23:59<br>'))

def test_failed_date_verify():
    assert 0 == len(TextVerifier().verify_text('2016/2/30（火）23:59'))
