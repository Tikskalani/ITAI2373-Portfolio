from src.data_processing.text_preprocessor import TextPreprocessor


def test_preprocess_removes_noise():
    p = TextPreprocessor()
    out = p.preprocess("The BANKS are running at http://x.com and a@b.com 12345 !!!")
    assert "http" not in out and "@" not in out
    assert all(ch.isalpha() or ch == " " for ch in out)
    assert "bank" in out
