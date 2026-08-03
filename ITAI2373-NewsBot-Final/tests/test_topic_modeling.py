from src.analysis.topic_modeler import TopicModeler


def test_topic_modeler_shapes():
    docs = ["bank market share profit money economy"] * 8 + \
           ["team goal player match win league"] * 8 + \
           ["film award actor movie star music"] * 8
    tm = TopicModeler(n_topics=3, max_features=60)
    W = tm.fit_transform(docs)
    assert W.shape == (24, 3)
    assert len(tm.get_topic_words(0, 5)) == 5
