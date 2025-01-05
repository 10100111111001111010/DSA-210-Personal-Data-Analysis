# URL and web-related terms
WEB_TERMS = {
    'com', 'www', 'http', 'https', 'youtube', 'youtu', 'watch', 'video',
    'shorts', 'channel', 'playlist', 'subscribe'
}

# Language particles and regional terms
LANGUAGE_PARTICLES = {
    'v', 're', 'as', 'de', 'da', 'en', 'bu', 'ne', 'ile', 'mi',
    'la', 'ii', 'öyle', 've'
}

# Numbers and counters
NUMERICAL = {
    '000', 'k', 'm', 'bir', 'one', 'first'
}

# Articles and basic words
BASIC_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
    'to', 'for', 'of', 'with', 'by', 'from'
}

# Pronouns and possessives
PRONOUNS = {
    'i', 'me', 'my', 'mine', 'myself',
    'you', 'your', 'yours', 'yourself',
    'he', 'him', 'his', 'himself',
    'she', 'her', 'herself',
    'it', 'its',
    'we', 'us', 'our',
    'they', 'them', 'their'
}

# Verbs and helpers
VERBS = {
    'am', 'is', 'it', 'are', 'was', 'were', 'be', 'being',
    'have', 'has', 'had', 'having',
    'do', 'does', 'did',
    'will', 'can', 'should', 'could', 'would',
    'get', 'got', 'gotten', 'getting', 'gets',
    'go', 'goes', 'went', 'gone', 'going',
    'make', 'made', 'come', 'look', 'see', 'watch', 'know'
}

# Time-related terms
TIME_TERMS = {
    'day', 'week', 'month', 'year', 'time', 'daily', 'weekly',
    'now', 'then', 'before', 'after', 'while', 'during', 'until',
    'minutes', 'years', 'last', 'ever'
}

# Descriptive words
DESCRIPTORS = {
    'new', 'old', 'good', 'better', 'best', 'perfect',
    'bad', 'worse', 'worst',
    'big', 'small', 'large', 'little', 'long', 'short',
    'real', 'great', 'well', 'black', 'awesome', 'amazing'
}

# Quantities and comparisons
QUANTITIES = {
    'most', 'some', 'any', 'all', 'both', 'each', 'every',
    'other', 'another', 'own', 'same', 'such', 'more', 'less',
    'many', 'few', 'several', 'much'
}

# Question and relation words
FUNCTION_WORDS = {
    'how', 'what', 'why', 'who', 'where', 'when', 'which',
    'that', 'this', 'these', 'if', 'about', 'than', 'way',
    'here', 'there', 'like'
}

# Common modifiers
MODIFIERS = {
    'so', 'too', 'very', 'enough', 'just', 'only', 'even',
    'also', 'still', 'already', 'yet', 'almost',
    'always', 'never', 'often', 'sometimes', 'rarely'
}

# Media-related terms
MEDIA_TERMS = {
    'episode', 'ep', 'short', 'ft', 'feat', 'vs',
    'part', 'official', 'full'
}

# Directional and spatial terms
SPATIAL = {
    'up', 'down', 'over', 'under', 'above', 'below',
    'between', 'among', 'through', 'into', 'out', 'off',
    'back'
}

# Other common words
OTHER = {
    'not', 'no', 'yes', 'maybe', 'perhaps', 'either', 'neither',
    'none', 'let', 'really'
}

# Combine all sets into one comprehensive set of exclude words
EXCLUDE_WORDS = (
        WEB_TERMS | LANGUAGE_PARTICLES | NUMERICAL | BASIC_WORDS |
        PRONOUNS | VERBS | TIME_TERMS | DESCRIPTORS | QUANTITIES |
        FUNCTION_WORDS | MODIFIERS | MEDIA_TERMS | SPATIAL | OTHER
)


def get_exclude_words():
    return EXCLUDE_WORDS


def should_exclude(word):
    return word.lower() in EXCLUDE_WORDS