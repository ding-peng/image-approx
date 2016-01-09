#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Peng Ding @ 2016-01-07 17:29:57


import random


class gene:

    def __init__(self):
        self.mutate()

    def mutate(self):
        self.pos_1 = (random.randint(0, 500), random.randint(0, 500))
        self.pos_2 = (random.randint(0, 500), random.randint(0, 500))
        self.pos_3 = (random.randint(0, 500), random.randint(0, 500))
        self.color = {'r': random.randint(0, 255),
                      'g': random.randint(0, 255),
                      'b': random.randint(0, 255),
                      'a': 128}


class genetic:

    def crossover(self, parent_1, parent_2, rate):
        gene_num = len(parent_1.genes)
        mid = int(gene_num * rate)
        new_genes = parent_1.genes[:mid] + parent_2.genes[mid:]
        return new_genes

    def crossover2(self, parent_1, parent_2, tri_num):
        new_genes = []
        for i in xrange(tri_num):
            if random.uniform(0, 1) < 0.5:
                new_genes.append(parent_1.genes[i])
            else:
                new_genes.append(parent_2.genes[i])
        return new_genes

    def crossover3(self, parent_1, parent_2, tri_num):
        array1 = parent_1.get_array()
        array2 = parent_2.get_array()
        new_array = []
        flag = -1
        last_pos = 0
        pos = random.randint(0, 50)
        while last_pos < tri_num * 6:
            if flag > 0:
                new_array += array1[last_pos:pos]
            else:
                new_array += array2[last_pos:pos]
            flag *= -1
            last_pos = pos
            pos = random.randint(last_pos, last_pos+50)
        return new_array

    def mutate(self, genes, rate, tri_num):
        if random.uniform(0, 1) < rate:
            mut_genes = random.sample(range(tri_num), 5)
            for g in mut_genes:
                genes[g].mutate()
        return genes
