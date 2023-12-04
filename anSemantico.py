from transformers import pipeline

def analizador_semantico(texto):
    sentiment_analyzer = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    resultado = sentiment_analyzer(texto)[0]
    sentimiento = resultado['label']
    return sentimiento

texto_prueba = "Voy a follar bien rico"
sentimiento = analizador_semantico(texto_prueba)
