import random

ingredients = ["mango", "pistachio", "berry", "chocolate", "strawberry", "raspberry", "blueberry", "blackberry", "currant", "cranberry", "black mulberry", "fig", "peach", "hazelnut", "cherry", "banana", "apricot", "kiwi", "coconut", "pineapple", "plum", "juniper berry", "lemon", "pear", "almond", "cashew", "sesame"]

adjectives = ["sweet", "sour", "fresh", "crispy", "delicate", "fluffy", "silky", "delicious", "delightful", "nutty", "red", "blue", "yellow", "white", "pink", "orange", "green", "tasty", "refreshing", "angelic", "beautiful", "candied", "blissful", "caramelized", "chocolaty", "classic", "comforting", "crisp", "crispy", "crunchy", "dainty", "elegant", "enjoyable", "enticing", "tempting", "alluring", "exceptional", "exquisite", "fruity", "garnished", "handmade", "heavenly", "homemade", "honeyed", "inspiring", "irresistible", "lavish", "light", "luscious", "magical", "nectarous", "pure", "savoury", "sensational", "special", "sublime", "traditional", "double", "triple", "velvety", "warm", "yummy", "milky", "celestial", "enchanted", "exclusive", "famous", "fancy", "fantastic", "gentle", "glamorous", "overwhelming", "precious", "pretty", "radiant", "romantic", "shining", "simple", "smooth", "tender", "warm", "playful", "cheeky"]

nouns = ["surprise", "dream", "miracle", "fantasy", "secret", "ambrosia", "fusion", "symphony", "treat", "abbundance", "adventure", "spring", "summer", "autumn", "winter", "blessing", "bliss", "blossom", "flower", "ribbon", "bonus", "boost", "celebration", "charm", "choice", "chuckle", "comfort", "star", "confidant", "delight", "desert", "flavor", "fountain", "garden", "generosity", "gift", "grin", "harmony", "heaven", "inspiration", "invitation", "journey", "kiss", "magic", "marvel", "wonder", "paradise", "passion", "perfection", "pleasure", "prize", "reward", "rose", "sensation", "sentiment", "serenity", "smile", "spark", "spell", "synergy", "taste", "warmth", "wisdom"]

def random_sweets(count: int = 1, seed = None):
    random.seed(seed, version=2)
    results = []
    for index in range(count):
        name_type = random.randint(0,10)
        if name_type < 4:
            ingredient_index = random.randrange(0, len(ingredients))
            noun_index = random.randrange(0, len(nouns))
            results.append(ingredients[ingredient_index] + " " + nouns[noun_index])
        else:
            common_nouns = ingredients + nouns
            noun_index = random.randrange(0, len(common_nouns))
            adjective_index = random.randrange(0, len(adjectives))
            results.append(adjectives[adjective_index] + " " + common_nouns[noun_index])
    return results
    
    
first_sweets = random_sweets()
print(first_sweets)

second_sweets = random_sweets(10, 42)
print(second_sweets)

third_sweets = random_sweets(30, "Some special name")
print(third_sweets)