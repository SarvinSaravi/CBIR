from elasticsearch import Elasticsearch

# from reports.save_in_files import save_in_csv

timeout_ms = 60000


# this is a function that used inside of other main functions
def remove_duplicates(phrase):
    words = phrase.split()
    unique_words = []

    for word in words:
        if word not in unique_words:
            unique_words.append(word)

    return ' '.join(unique_words)


def elastic_indexing_with_titles(title_list, data_list, k, focus_index, shard_number=2, replica_number=0):
    # preparation mappings
    str_lst = [st.rstrip() for st in data_list]
    K = k
    data = {
        'title': {'type': 'keyword'}
    }
    index_counting_list = list(reversed(range(1, K + 1)))

    for i in index_counting_list:
        key = 'pos' + str(i)
        data[key] = {'type': 'keyword'}

    mappings = {
        'properties': data
    }

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200")

    # Define index name and settings/mappings
    index_name = focus_index
    settings = {
        'number_of_shards': shard_number,
        'number_of_replicas': replica_number
    }

    # Create index with defined settings/mappings
    es.indices.create(index=index_name, mappings=mappings, settings=settings)

    # inject data to index
    tmp_id = 1
    for st in str_lst:
        mid_list = st.split(' ')
        # mid_list.reverse()
        data['title'] = title_list[tmp_id - 1]
        for i, x in zip(index_counting_list, mid_list):
            key = 'pos' + str(i)
            data[key] = x

        es.index(index=index_name, id=str(tmp_id), document=data)
        tmp_id += 1


def elastic_indexing_idea3(title_list, data_list, focus_index, shard_number, replica_number):
    # preparation mappings
    str_lst = [st.rstrip() for st in data_list]

    mappings = {
        'properties': {
            'title': {'type': 'keyword'},
            'text_code': {'type': 'text'}
        }
    }

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

    # Define index name and settings/mappings
    index_name = focus_index
    settings = {
        'number_of_shards': shard_number,
        'number_of_replicas': replica_number
    }

    # Create index with defined settings/mappings
    es.indices.create(index=index_name, mappings=mappings, settings=settings)

    # inject data to index
    tmp_id = 1
    for text_code, title in zip(str_lst, title_list):
        data = {
            'title': title,
            'text_code': text_code
        }
        es.index(index=index_name, id=str(tmp_id), document=data)
        tmp_id += 1


def elastic_indexing_idea1(title_list, data_list, focus_index, shard_number, replica_number):
    # preparation mappings
    mappings = {
        'properties': {
            'title': {'type': 'keyword'},
            'text_code': {'type': 'text'}
        }
    }

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

    # Define index name and settings/mappings
    index_name = focus_index
    settings = {
        'number_of_shards': shard_number,
        'number_of_replicas': replica_number
    }

    # Create index with defined settings/mappings
    es.indices.create(index=index_name, mappings=mappings, settings=settings)

    # prepare data for indexing
    string_list = [remove_duplicates(st.rstrip()) for st in data_list]

    # inject data to index
    tmp_id = 1
    for text_code, title in zip(string_list, title_list):
        data = {
            'title': title,
            'text_code': text_code
        }
        es.index(index=index_name, id=str(tmp_id), document=data)
        tmp_id += 1


def elastic_indexing_idea4(title_list, data_list, focus_index, shard_number, replica_number):
    # remove duplicates in all strings
    string_list = [remove_duplicates(st.rstrip()) for st in data_list]
    K = string_list[0].count('T')
    prefix_step = 20
    prefix_number = int(K / prefix_step) + 1 if (K % prefix_step != 0) else int(K / prefix_step)
    print("| prefix step | = " + str(prefix_step))

    # preparation mappings
    data = {
        'title': {'type': 'keyword'}
    }

    for i in range(1, prefix_number + 1):
        key = 'prefix' + str(i)
        data[key] = {'type': 'keyword', 'fields': {'disjoint': {'type': 'text'}}}

    mappings = {
        'properties': data
    }

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

    # Define index name and settings/mappings
    index_name = focus_index
    settings = {
        'number_of_shards': shard_number,
        'number_of_replicas': replica_number
    }

    # Create index with defined settings/mappings
    es.indices.create(index=index_name, mappings=mappings, settings=settings)

    # inject data to index
    tmp_id = 1
    for text_code, title in zip(string_list, title_list):
        data['title'] = title

        split_code_text = text_code.split(' ')

        for i, prefix in enumerate(data.keys()):
            if prefix != 'title':
                data[prefix] = ' '.join(split_code_text[0:prefix_step * i])

        es.index(index=index_name, id=str(tmp_id), document=data)
        tmp_id += 1


def elastic_indexing_with_partitioning(title_list, partition_data_list, focus_index, shard_number, replica_number):
    # preparation mappings
    partition_count = len(partition_data_list)
    img_count = len(partition_data_list[0])
    data = {
        'title': {'type': 'keyword'}
    }
    for i in range(1, partition_count + 1):
        data['part' + str(i)] = {'type': 'text'}

    mappings = {
        'properties': data
    }

    # Connect to 'http://localhost:9200'
    es = Elasticsearch("http://localhost:9200", timeout=timeout_ms)

    # Define index name and settings/mappings
    index_name = focus_index
    settings = {
        'number_of_shards': shard_number,
        'number_of_replicas': replica_number
    }

    # Create index with defined settings/mappings
    es.indices.create(index=index_name, mappings=mappings, settings=settings)

    # inject data to index
    for doc_index in range(img_count):
        doc_strings = [part[doc_index] for part in partition_data_list]
        data['title'] = title_list[doc_index]
        for x, part_str in enumerate(doc_strings):
            data['part' + str(x + 1)] = part_str

        es.index(index=index_name, id=str(doc_index + 1), document=data)


# the main function for redirecting to others
def elastic_indexing(title_list, data_list, focus_index, indexing_method, shard_number=2, replica_number=0):
    if indexing_method == 'same_exact_phrase_with_separator':
        print(" > The method selected for indexing is : ", indexing_method)
        return elastic_indexing_idea3(title_list, data_list, focus_index, shard_number, replica_number)
    elif indexing_method == 'fuzzy_search':
        print(" > The method selected for indexing is : ", indexing_method)
        return elastic_indexing_idea3(title_list, data_list, focus_index, shard_number, replica_number)
    elif indexing_method == 'remove_frequency':
        print(" > The method selected for indexing is : ", indexing_method)
        return elastic_indexing_idea1(title_list, data_list, focus_index, shard_number, replica_number)
    elif indexing_method == 'prefix_search':
        print(" > The method selected for indexing is : ", indexing_method)
        return elastic_indexing_idea4(title_list, data_list, focus_index, shard_number, replica_number)
    elif indexing_method == 'partitioning':
        print(" > The method selected for indexing is : ", indexing_method)
        return elastic_indexing_with_partitioning(title_list, data_list, focus_index, shard_number, replica_number)
    else:
        print(" >>> Please clarify the indexing method <<< ")
    return


# test-cases
# str_list = [
#     'T11 T11 T11 T11 T11 T11 T4 T4 T4 T4 T4 T2 T2 T2 T2 T7 T7 T7 T3 T3 T1     ',
#     'T11 T11 T11 T11 T11 T11 T8 T8 T8 T8 T8 T7 T7 T7 T7 T5 T5 T5 T1 T1 T2     ',
#     'T5 T5 T5 T5 T5 T5 T10 T10 T10 T10 T10 T8 T8 T8 T8 T7 T7 T7 T9 T9 T6     '
# ]
# t_list = ['img1.jpg', 'img2.jpg', 'img3.jpg']
# elastic_indexing_idea4(t_list, str_list, 'test4idea1', shard_number=2, replica_number=0)
# part_list = [
#     ['SSSS', 'TTTT', 'AA', 'QQQQ', 'ZZZ'],
#     ['GGG', 'UUUUUUUUU', 'BBBB', 'KKKKKK', 'MMMM'],
#     ['LLLL', 'TTTT', 'BBBB', 'KKKK', 'VV']
# ]
# elastic_indexing_with_partitioning(t_list, part_list, 'test4U', shard_number=1, replica_number=0)
