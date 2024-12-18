class SlugGenerator():
    def __init__(self):
        self.translit = {'а':'a', 'б':'b', 'в':'b', 'г':'g', 
        'д':'d', 'е':'e', 'ё':'e', 'ж':'j', 'з':'z', 
        'и':'i', 'й':'y', 'к':'k', 'л':'l', 'м':'m', 'н':'n', 
        'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u',
        'ф':'f', 'х':'h', 'ц':'ts', 'ч':'ch', 'ш':'sh', 'щ':'sh', 
        's':'yi', 'э':'a', 'ю':'u', 'я':'ya'}
    def __call__(self, title, id):
        slug = ''
        for sym in title.lower():
            slug += self.translit.get(sym, '')
        return slug + '-' + str(id)