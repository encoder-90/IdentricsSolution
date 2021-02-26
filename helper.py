import pandas as pd
import requests


# Transform csv data into dataframe
def load_data():
    df_co_mention_count = pd.read_csv("data/co_mention_count.csv", index_col=[0])
    df_mono_mention_count = pd.read_csv("data/mono_mentions_count.csv", index_col=[0])
    df_rank_mentions_count = pd.read_csv("data/rank_mentions_count.csv", index_col=[0])
    df_co_mentions_names = pd.read_csv("data/co_mentions_names.csv", index_col=[0])
    df_name_sen_num = pd.read_csv("data/df_name_sen_num.csv", index_col=[0])

    return df_co_mention_count, df_mono_mention_count, df_rank_mentions_count, df_co_mentions_names, df_name_sen_num


# Loaded automatically once helper is imported bu the api.py file
df_co_mention_count, df_mono_mention_count, df_rank_mentions_count, df_co_mentions_names, df_name_sen_num = load_data()


def check_name_exists(name):
    character_names = list(df_name_sen_num.name.values)
    if name in character_names:
        return True
    return False


def get_rank(name):
    list_mentions = []
    df_ranks_filtered = df_rank_mentions_count.loc[df_rank_mentions_count["name"] == name, "rank"]
    if df_ranks_filtered.empty:
        return list_mentions
    list_mentions = list(df_ranks_filtered)[0]
    return list_mentions


def get_mentions_count(name):
    list_mentions = []
    df_mentions_filtered = df_rank_mentions_count.loc[df_rank_mentions_count["name"] == name, "counts"]
    if df_mentions_filtered.empty:
        return list_mentions
    list_mentions = list(df_mentions_filtered)[0]
    return list_mentions


def get_mono_mentions_count(name):
    list_mentions = []
    df_mono_mentions_filtered = df_mono_mention_count.loc[df_mono_mention_count["name"] == name, "counts"]
    if df_mono_mentions_filtered.empty:
        return list_mentions
    list_mentions = list(df_mono_mentions_filtered)[0]
    return list_mentions


def get_co_mentions_count(name):
    list_mentions = []
    df_co_mentions_filtered = df_co_mention_count.loc[df_co_mention_count["name"] == name, "counts"]
    if df_co_mentions_filtered.empty:
        return list_mentions
    list_mentions = list(df_co_mentions_filtered)[0]
    return list_mentions


def get_character_info(name):
    rank = get_rank(name)
    # Map rank to correct value as in the dataframe 
    # episode characters are defined as rank 0
    if rank == 0: rank = 3

    mentions_count = get_mentions_count(name)
    mono_mentions_count = get_mono_mentions_count(name)
    co_mention_count = get_co_mentions_count(name)
    co_mentions_names = get_co_mentions_names(name)

    character_dict = {
        "name": name,
        "rank": rank,
        "mentions_count": mentions_count,
        "mono_mentions_count": mono_mentions_count,
        "co_mention_count": co_mention_count,
        "co_mentions_names": co_mentions_names
    }
    return character_dict


def get_co_mentions_names(name):
    # Group dataframe by sentence number
    gk_sen = df_co_mentions_names.groupby("sentence_num")

    list_sen = []
    for index, row in df_co_mentions_names.iterrows():
        if row["name"] == name:
            list_sen.append(row["sentence_num"])
    
    names_list = []
    for i in list_sen:
        names_list.append(list(gk_sen.get_group(i).name.values))
    
    clean_list = []
    for sen_list in names_list:
        for i in sen_list:
            if i != name:
                clean_list.append(i)
    
    return list(set(clean_list))


def get_main_characters():
    df_main_characters = df_rank_mentions_count.loc[df_rank_mentions_count["rank"] == 1]

    main_characters_names = list(df_main_characters.name.values)
    main_characters_list = []

    for character_name in main_characters_names:
        main_characters_list.append(get_character_info(character_name))

    return main_characters_list


def get_support_characters():
    df_second_char = df_rank_mentions_count.copy()
    df_second_char = df_second_char.loc[df_second_char["rank"] == 2]
    df_second_char = df_second_char.head(10)

    support_characters_names = list(df_second_char.name.values)
    support_characters_list = []

    for character_name in support_characters_names:
        support_characters_list.append(get_character_info(character_name))
    
    return support_characters_list


def get_episode_characters():
    df_rank3_char = df_rank_mentions_count.copy()
    df_rank3_char = df_rank3_char.loc[df_rank3_char["rank"] == 0]
    df_rank3_char = df_rank3_char.reset_index(drop=True)
    df_ten_elements = df_rank3_char.sample(n=10)

    episode_characters_names = list(df_ten_elements.name.values)
    episode_characters_list = []

    for character_name in episode_characters_names:
        episode_characters_list.append(get_character_info(character_name))

    return episode_characters_list


def get_character_mentions(name=None):
    list_sen_num = []
    if name is None:
        df_main_characters = df_rank_mentions_count.loc[df_rank_mentions_count["rank"] == 1]
        main_characters_names = list(df_main_characters.name.values)
        for character in main_characters_names:
            for index, row in df_name_sen_num.iterrows():
                if row["name"] == character:
                    list_sen_num.append(row["sentence_num"])
        return list_sen_num

    for index, row in df_name_sen_num.iterrows():
        if row["name"] == name:
            list_sen_num.append(row["sentence_num"])
    return list_sen_num


def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))


def get_characters_co_mentions(name_a, name_b):
    list_sen_one = []
    for index, row in df_co_mentions_names.iterrows():
        if row['name'] == name_a:
            list_sen_one.append(row['sentence_num'])
    
    list_sen_two = []
    for index, row in df_co_mentions_names.iterrows():
        if row['name'] == name_b:
            list_sen_two.append(row['sentence_num'])
    
    list_common_sentences = intersection(list_sen_one, list_sen_two)
    return list_common_sentences


def get_book_info_from_ISBN(isbn_number):
    """
    Gets book information using provided isbn_number
    Information retrieved from public Google API
    """
    info_dict = {}
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn_number
    response = requests.get(url)
    data = response.json()

    if data["totalItems"] == 0:
       return info_dict
    
    title = data["items"][0]["volumeInfo"]["title"]
    authors = data["items"][0]["volumeInfo"]["authors"]
    summary = data["items"][0]["searchInfo"]["textSnippet"]
    page_count = data["items"][0]["volumeInfo"]["pageCount"]
    categories = data["items"][0]["volumeInfo"]["categories"]
    language = data["items"][0]["volumeInfo"]["language"]

    info_dict = {
        "title": title,
        "authors": authors,
        "summary": summary,
        "categories": categories,
        "page_count": page_count,
        "language": language
    }
    return info_dict
