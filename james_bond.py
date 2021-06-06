import redis

FILE_PATH = 'limited_dictionary.txt'


def load_words_from_file(redis_client: redis.Redis):
    file = open(FILE_PATH)

    for word in file.readlines():
        redis_client.set(word.rstrip("\n").upper(), "")


def load_dictionary(redis_client: redis.Redis):
    print("Loading Dictionary...")
    load_words_from_file(redis_client)
    print("Dictionary Loaded!")


def is_valid_word(word: str, redis_client: redis.Redis) -> bool:
    return redis_client.exists(word)


def break_string_to_valid_words(string: str):
    input_size = len(string)
    if input_size == 0:
        return ''

    for start_index in range(input_size - 1, -1, -1):
        word = string[start_index:input_size]

        if is_valid_word(word, redis_client):
            broken_string_until_start_index = break_string_to_valid_words(string[0:start_index])
            if broken_string_until_start_index is not None:
                return broken_string_until_start_index + ' ' + word

    return None


if __name__ == '__main__':
    redis_client = redis.Redis(
        host='localhost',
        port='6379',
    )

    load_dictionary(redis_client)

    input_string = input("\nEnter Input:\n").strip()

    answer = break_string_to_valid_words(input_string)

    print(answer.strip()) if answer else print("The String is Invalid!")
