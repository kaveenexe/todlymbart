# Dictionary for common terms to be translated manually (bilingual lexicon)
custom_lexicon = {
    "Todly": "Todly",
    "fruits": "පලතුරු",
    "vegetables": "එළවළු",
    "whole grains": "ධාන්ය වර්ග",
    "lean proteins": "ලීන් ප්‍රෝටීන්",
    "dairy products": "කිරි නිෂ්පාදන",
    "calcium": "කැල්සියම්",
    "Breast milk": "මව්කිරි",
    "legumes": "රනිල කුලයට අයත් බෝග",
    "lean meat": "සිහින් මස්",
    "dense": "ඝනත්වයකින් යුක්ත",
    "nuts": "ඇට වර්ග",
    "avocados":"අලිගැට පේර",
    "balanced diet": "සමබර ආහාර වේලක්",
    "dietitian": "පෝෂණවේදියෙක්",
    "comfort": "සුවපහසුව",
    "interaction": "අන්තර්ක්රියා",
    "support": "සහාය",
    "physical": "ශාරීරික",
    "lethargic": "උදාසීන",
    "healthy weight": "සෞඛ්ය සම්පන්න බර",
    "charts": "ප්රස්ථාර",
    "Interactive play": "අන්තර් ක්රියාකාරී ක්රීඩා",
    "storytelling": "කතන්දර කීම",
    "e.g.": "උදා."
}

def apply_custom_lexicon(text):
    for english_term, sinhala_translation in custom_lexicon.items():
        text = text.replace(english_term, sinhala_translation)
    return text
