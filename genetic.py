#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Peng Ding @ 2016-01-07 17:29:57


import random


class gene(object):
    """
    The gene class, which represent a triangle.

    Attributes:
        pos_1: The first vertex of the triangle.
        pos_2: The second vertex of the triangle.
        pos_2: The third vertex of the triangle.
        color: The GRBA value of the triangle.
    """
    def __init__(self):
        """
        Inits a gene with mutation operation.
        """
        self.mutate()

    def mutate(self):
        """
        Mutation operation. Change the values of a gene.
        """
        self.pos_1 = (random.randint(0, 500), random.randint(0, 500))
        self.pos_2 = (random.randint(0, 500), random.randint(0, 500))
        self.pos_3 = (random.randint(0, 500), random.randint(0, 500))
        self.color = {'r': random.randint(0, 255),
                      'g': random.randint(0, 255),
                      'b': random.randint(0, 255),
                      'a': 128}


class genetic(object):
    """
    The genetic operation utils class.
    """
    def crossover(self, parent_1, parent_2, rate):
        """
        Crossover method 1, one-point crossover. (legacy)
        Generate a child with a portion of complete genes from parent_1
        and another portion of complete genes from parent_2.

        Args:
            parent_1: a parent.
            parent_2: another parent.
            rate: the portion of genes that come from parent_1.

        Returns:
            new_genes: a list of new genes.
        """
        gene_num = len(parent_1.genes)
        mid = int(gene_num * rate)
        new_genes = parent_1.genes[:mid] + parent_2.genes[mid:]
        return new_genes

    def crossover2(self, parent_1, parent_2, tri_num):
        """
        Crossover method 2, uniform crossover. (legacy)
        Generate a child with some complete genes from parent_1
        and some complete genes from parent_2.

        Args:
            parent_1: a parent.
            parent_2: another parent.
            tri_num: number of triangles that form the result image.

        Returns:
            new_genes: a list of new genes.
        """
        new_genes = []
        for i in xrange(tri_num):
            if random.uniform(0, 1) < 0.5:
                new_genes.append(parent_1.genes[i])  # get gene from parent_1
            else:
                new_genes.append(parent_2.genes[i])  # get gene from parent_2
        return new_genes

    def crossover3(self, parent_1, parent_2, tri_num):
        """
        Crossover method 3, uniform crossover. (currently used)
        Transform the parent genes into array representation(DNA sequence).
        The child get a portion of DNA from parent_1, then from parent_2,
        then from parent_1 again, and so on.

        Args:
            parent_1: a parent.
            parent_2: another parent.
            tri_num: number of triangles that form the result image.

        Returns:
            new_genes: an array representation(DNA sequence) of the gene.
        """
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
        """
        Mutation Selector:
        Select some genes and let them mutate.

        Args:
            genes: the list of genes of an individual.
            rate: the mutation rate.
            tri_num: number of triangles that form the result image.

        Returns:
            genes: a list of mutated genes.
        """
        if random.uniform(0, 1) < rate:
            mut_genes = random.sample(range(tri_num), 5)
            for g in mut_genes:
                genes[g].mutate()
        return genes
