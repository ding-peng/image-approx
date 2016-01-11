#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Peng Ding @ 2016-01-07 17:00:10


import random
import math
import operator
from PIL import Image, ImageDraw, ImageChops

from genetic import genetic, gene

TARGET_IMG_NAME = 'test.jpg'
POP_SIZE = 25
MUT_RATE = 0.05
GENERATIONS = 100000
CHILDREN_PER_GEN = 5
TRI_NUM = 100
BACKGROUND_COLOR = 'white'

TARGET = Image.open(TARGET_IMG_NAME).convert('RGB')
TARGET = TARGET.resize((500, 500))


class individual:

    def __init__(self, parent_1=None, parent_2=None):
        self.genes = []
        op = genetic()
        if parent_1 and parent_2:
            array = op.crossover3(parent_1, parent_2, TRI_NUM)
            self.generate_genes_from_array_with_mut(array, MUT_RATE)
        else:
            for i in xrange(TRI_NUM):
                self.genes.append(gene())
        self.im = self.get_current_img()
        self.fitness = self.get_fitness(TARGET)

    def get_current_img(self):
        im = Image.new('RGB', (500, 500), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(im, 'RGBA')
        for gene in self.genes:
            draw.polygon([gene.pos_1, gene.pos_2, gene.pos_3],
                         fill=(gene.color['r'], gene.color['g'],
                               gene.color['b'], gene.color['a']))
        del draw
        return im

    def save_current_img(self, f_name):
        self.im.save(f_name, 'PNG')

    def get_fitness(self, target):
        h = ImageChops.difference(target, self.im).histogram()
        return math.sqrt(reduce(operator.add,
                         map(lambda h, i: h*(i**2),
                             h, range(256)*3)) /
                            (float(target.size[0]) * target.size[1]))

    def get_array(self):
        array = []
        for g in self.genes:
            array.append(g.pos_1)
            array.append(g.pos_2)
            array.append(g.pos_3)
            array.append(g.color['r'])
            array.append(g.color['g'])
            array.append(g.color['b'])
        return array

    def generate_genes_from_array_with_mut(self, array, rate):
        new_array = zip(*[iter(array)]*6)
        self.genes = []
        for chunk in new_array:
            g = gene()
            if random.uniform(0, 1) > rate:
                g.pos_1 = chunk[0]
                g.pos_2 = chunk[1]
                g.pos_3 = chunk[2]
                g.color['r'] = chunk[3]
                g.color['g'] = chunk[4]
                g.color['b'] = chunk[5]
            self.genes.append(g)


def initalize(pop):
    for i in xrange(POP_SIZE*2):
        pop.append(individual())
    pop.sort(key=lambda x: x.fitness)
    pop = pop[:POP_SIZE]
    return pop


def evolove(pop):
    for i in xrange(GENERATIONS):

        children = []

        parent_choices = []
        w = 100
        for p in pop:
            parent_choices.append((p, w))
            if w > 0:
                w = w - 10
        pop_choices = [val for val, cnt in parent_choices for j in range(cnt)]

        for j in range(CHILDREN_PER_GEN):
            parent_1 = random.choice(pop_choices)
            parent_2 = random.choice(pop_choices)
            child = individual(parent_1, parent_2)
            children.append(child)

        pop += children
        pop.sort(key=lambda x: x.fitness)
        pop = pop[:POP_SIZE]

        if i % 10000 == 0 or i in [100, 200, 500, 1000, 5000]:
            pop[0].save_current_img(str(i)+'_b.png')
        if i % 10 == 0:
            avg = sum(map(lambda x: x.fitness, pop)) / 25
            print "Finish " + str(i), pop[0].fitness, avg
    return pop


if __name__ == '__main__':
    pop = []
    pop = initalize(pop)
    pop = evolove(pop)
    pop[0].save_current_img('best.png')
    print pop[0].fitness
