import pytest

import numpy as np

from .vector import EmbeddingInfo, VectorIndices

TESTIDX = 'testidx'

TEST_EMBEDDING_SIZE = 2048


def _create_random_vectors():
    vectors = []
    for i in range(10):
        vectors.append(
            np.random.random(TEST_EMBEDDING_SIZE).astype(np.float32)
        )
    return vectors


def cosine(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


@pytest.fixture
def vector_index():
    indices = VectorIndices()

    return indices.get(TESTIDX)


def test_initindex(vector_index):
    vector_index.create_index(embedding_size=TEST_EMBEDDING_SIZE)


def test_putvector(vector_index):
    vectors = _create_random_vectors()

    for i in range(10):
        data = vectors[i]
        vector_index.put(EmbeddingInfo(
            key=TESTIDX + ':' + str(i),
            tag='text-'+str(i),
            text='example random text',
            ntokens=3,
            embedding=data),
        )

    # test get textid
    textid = vector_index.get_tag(1)
    assert textid == 'text-1', \
        'ValueError: expecting text-1, getting ' + textid

    # test get embedding
    for i in range(10):
        embedding = vector_index.get_embedding(TESTIDX + ':' + str(i))

        assert np.array_equal(embedding, vectors[i]), \
            f'Error, getting unexpected embedding value at index {i}'


def test_searchvector(vector_index):
    search_vector = np.random.random(TEST_EMBEDDING_SIZE).astype(np.float32)

    results = vector_index.search(search_vector, max=10)
    scores = []

    assert len(results) != 0, 'No search results'

    for r in results:
        embedding = vector_index.get_embedding(r['key'])
        score = cosine(search_vector, embedding)
        scores.append(score)

    # cosine embedding is sorted by highest score, with max sorted as top
    assert scores == sorted(scores, reverse=True), 'Search result not sorted'


def test_cleanup(vector_index):
    vector_index.drop_index()
