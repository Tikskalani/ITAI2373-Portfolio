def test_all_core_imports():
    from src.data_processing.text_preprocessor import TextPreprocessor
    from src.data_processing.feature_extractor import FeatureExtractor
    from src.data_processing.data_validator import DataValidator
    from src.analysis.classifier import NewsClassifier
    from src.analysis.sentiment_analyzer import SentimentAnalyzer
    from src.analysis.ner_extractor import NERExtractor
    from src.analysis.topic_modeler import TopicModeler
    from src.newsbot import NewsBot
    assert NewsBot is not None
