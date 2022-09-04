import pickle

cv = pickle.load(open(f'./cv.pickle', 'rb'))
model = pickle.load(open(f'./spam-detection-model.sav', 'rb'))


############################
# Spam Detector
############################


def detect_spam(text: str) -> bool:
    text = text.replace('\n', ' ')

    vectorised_input = cv.transform([text]).toarray()
    result = model.predict(vectorised_input)

    return True if result == 'spam' else False
