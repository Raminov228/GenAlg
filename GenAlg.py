import random

#кол-во коэффицентов
len_a = 10

#кол-во особей в первой популяции
n0 = 1000

#сколько процентов будет умирать
dp = 0.5

#сколько процентов найдет себе пару
pp = 1

#сколько процентов мутирует
mp = 0

#класс особей
class Man():
    #особь - вектор x = [x1, x2, x3, x4....]
    def __init__(self, x):
        self.x = x

    #делаем детей просто складывая решения (самый оптимальный вариант)
    def get_children(self, man2):
        l = int(len(self.x) / 2)
        x = [self.x[i] + man2.x[i]  for i in range(len(self.x))]
        return [Man(x)]

    def __str__(self):
        return ', '.join([str(i) for i in self.x])

    def __len__(self):
        return len(self.x)


#Класс окружающей среды. Она определяет процент смертности, процент рождаемости и процент мутации
#Но самое важное - это фитнесс функция (т.е. она хранит значения коэффицентов a = [a1, a2, a3 ... an])
class Envrmnt():
    def __init__(self, a, death_per, parent_per, mutation_per):
        self.a = a
        self.d_p = death_per
        self.p_p = parent_per
        self.m_p = mutation_per

    #фитнесс функция - просто показывает насколько близко решение к правильному
    def f(self, man):
        return -abs(sum([self.a[i]*man.x[i] for i in range(len(self.a))]))

#Класс популяции
class Population():
    #принимаем список особей [Man1, Man2, ....]
    def __init__(self, pop, env):
        self.pop = pop
        self.env = env

    # умирает d_p процентов самых слабых
    def dead(self):
        self.pop.sort(key=lambda man: self.env.f(man))
        self.pop = self.pop[int(len(self.pop)*self.env.d_p):]

    # p_p процентов особей находят пару и выкекивают дитя
    def borning(self):
        amount_par = int(len(self) * self.env.p_p)
        parents = [(random.randint(0, len(self) - 1), random.randint(0, len(self) - 1)) for _ in range(amount_par)]
        children = []
        for pair in parents:
            children += self.pop[pair[0]].get_children(self.pop[pair[1]])
        self.pop += children

    # мутирует m_p процентов особей (плохо сделано)
    def mutate(self):
        mutate_men = (random.randint(0, len(self) - 1) for _ in range(int(len(self)*self.env.m_p)))
        for i in mutate_men:
            self.pop[i].x[random.randint(0, len(self.pop[0]) - 1)] = random.randint(-100000, 100000)

    def get_best(self):
        return self.pop[0]

    def __str__(self):
        return '\n'.join([str(i) for i in self.pop])

    def __getitem__(self, key):
        return self.pop[key]

    def __len__(self):
        return len(self.pop)

# функция создания рандомной последовательности
def get_random(l):
    x = [random.randint(-100000, 100000) for _ in range(l)]
    return x

# создаем окружающую среду
a = get_random(len_a) #cюда можно вставить свои коэффиценты, но надо не забыть поменять len_a
Env = Envrmnt(a, dp, pp, mp)

#создаем популяцию
H = Population([Man(get_random(len_a)) for _ in range(n0)], Env)

a_min = -10000000
x_min = []

i = 0
while i < 10000 and a_min != 0:
    H.borning()
    H.mutate()
    H.dead()
    a = Env.f(H.get_best())
    if a > a_min:
        print(a)
        a_min = a
        x_min = H.get_best()
    i += 1


print('end')
print('a1, a2... an', Env.a)
print('x1, x2... xn', x_min)