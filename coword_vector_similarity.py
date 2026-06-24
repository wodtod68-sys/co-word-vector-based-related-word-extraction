#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import math # sqrt

###############################################################################
def cosine_similarity(t_vector, c_vector):

    # 두 벡터의 내적 (공통 공기어에 대해서만 계산)
    if len(t_vector) > len(c_vector):
        t_vector, c_vector = c_vector, t_vector

    dot = 0.0
    for word, weight in t_vector.items():
        if word in c_vector:
            dot += weight * c_vector[word]

    # 각 벡터의 크기(norm)
    norm_t = math.sqrt(sum(v * v for v in t_vector.values()))
    norm_c = math.sqrt(sum(v * v for v in c_vector.values()))

    if norm_t == 0.0 or norm_c == 0.0:
        return 0.0

    return dot / (norm_t * norm_c)

###############################################################################
def most_similar_words(word_vectors, target, topN=10):

    result = {}

    # 대상어가 사전에 없으면 빈 결과 반환
    if target not in word_vectors:
        return []

    t_vector = word_vectors[target]

    # 관련어 후보 = 대상어의 공기어들 + 공기어들의 공기어들
    candidates = set()
    for coword in t_vector:
        candidates.add(coword)
        if coword in word_vectors:
            for cocoword in word_vectors[coword]:
                candidates.add(cocoword)

    for candidate in candidates:

        # 후보가 대상어와 같으면 제외
        if candidate == target:
            continue

        # 후보가 대상어에 포함되면 제외 (예: 개인정보/정보, 교육부장관/장관)
        if candidate in target:
            continue

        if candidate not in word_vectors:
            continue

        sim = cosine_similarity(t_vector, word_vectors[candidate])

        # 코사인 유사도가 0.001보다 큰 경우만 저장
        if sim > 0.001:
            result[candidate] = sim

    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:topN]

###############################################################################
def print_words(words):
    for word, score in words:
        print(f"{word}\t{score:.3f}")

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file(pickle)", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1],"rb") as fin:
        word_vectors = pickle.load(fin)

    while True:

        print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)

        try:
            query = input()

        except EOFError:
            print('프로그램을 종료합니다.', file=sys.stderr)
            break

        # result : list of tuples, sorted by cosine similarity
        result = most_similar_words(word_vectors, query, topN=30)

        if result:
            print_words(result)
        else:
            print('\n결과가 없습니다.')
