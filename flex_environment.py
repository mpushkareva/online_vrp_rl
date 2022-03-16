import numpy as np
import random


class Orders:
    def __init__(self, start_time=9 * 60, end_time=20 * 60, prob_per_min=1/2.5, time2deliver=120, pos_distrib='normal'):
        self.time2deliver = time2deliver
        # self.orders = []
        self.order2deliver_time = {}
        self.order2pos = {}
        self.n_orders = 0
        self.prob_per_min = prob_per_min
        self.pos_distrib = pos_distrib
        self.time = start_time
        self.end_time = end_time
        self.end_game = (start_time == end_time)
        self.completed_orders2time = {}

    def complete_order(self, order, time):
        self.completed_orders2time[order] = time

    def order_pos_distribution(self, order):
        if self.pos_distrib == 'normal':
            self.order2pos[order] = np.random.normal(2000, 3000, size=2)

    def step(self):
        for t in range(self.end_time - self.time):
            is_new_order = np.random.choice([0, 1], size=1, p=[1 - self.prob_per_min, self.prob_per_min])
            if is_new_order:
                # self.orders = list(range(n_orders))
                self.order_pos_distribution(self.n_orders)
                self.order2deliver_time[self.n_orders] = self.time + t + self.time2deliver
                self.n_orders += 1
                self.time += t
                return
        self.time = self.end_time
        self.end_game = True


class Couriers:
    def __init__(self, n_couriers=150, depot_pos=(0, 0), velocity=100, start_time=9 * 60):
        self.depot_pos = depot_pos
        self.velocity = velocity
        self.n_couriers = n_couriers
        self.depot = 'd' # !!!
        self.courier2route = {k: [self.depot] for k in range(n_couriers)}
        self.courier2pos = {k: depot_pos for k in range(n_couriers)}
        self.courier2route_hist = {k: [] for k in range(n_couriers)}
        self.courier2pos_hist = {k: [depot_pos] for k in range(n_couriers)}
        self.courier_works = np.zeros(n_couriers)
        self.time_prev = start_time

    def appoint_order(self, order, courier):
        if self.depot in self.courier2route[courier]:
            self.courier2route[courier].append(order)
        else:
            self.courier2route[courier].extend([self.depot, order])
        self.courier_works[courier] = True


class Environment:
    def __init__(self, courier_pay=1500, penalty_by_hour=300, reward_by_order=300, gamma=1):
        self.reward = 0
        self.courier_pay = courier_pay
        self.penalty_by_hour = penalty_by_hour
        self.reward_by_order = reward_by_order
        self.gamma = gamma # кажется, что не имеет смысла в данной постановке задачи

    def update_env(self, couriers, orders):
        for courier in range(couriers.n_couriers):
            last_pos = couriers.courier2pos[courier]
            period = orders.time - couriers.time_prev
            print('b')
            for route_point in couriers.courier2route[courier]:
                print('a', last_pos, couriers.depot_pos, couriers.velocity)
                next_pos = [couriers.depot_pos if route_point == couriers.depot else orders.order2pos[route_point]]
                print(last_pos, next_pos, last_pos, next_pos, couriers.velocity)
                t = ((last_pos[0] - next_pos[0]) ** 2 + (last_pos[1] - next_pos[1]) ** 2) ** 0.5 / couriers.velocity
                if t >= period:
                    couriers.courier2pos[0] = last_pos[0] + (next_pos[0] - last_pos[0]) / t * couriers.velocity
                    couriers.courier2pos[1] = last_pos[1] + (next_pos[1] - last_pos[1]) / t * couriers.velocity
                    break
                else:
                    period = orders.time - couriers.time_prev - t
                    couriers.courier2route_hist[courier].append(couriers.courier2route[courier].pop(route_point))
                    couriers.courier2pos = next_pos
                    if route_point != couriers.depot:
                        orders.complete_order(route_point, orders.time)
        couriers.time_prev = orders.time

    def total_reward(self, couriers, orders):
        order2best_deliver_time = {o: (orders.completed_orders2time[o] if o in orders.completed_orders2time.keys()
                                       else orders.time) for o in range(orders.n_orders)}
        # Стоимость работы дня курьера + награда за выполненный заказ + штраф за заказ не выполненный вовремя.
        self.reward = couriers.courier_works.sum() * self.courier_pay + \
                      self.reward_by_order * len(orders.completed_orders2time) + \
                      sum([max(order2best_deliver_time[o] - t, 0) * self.penalty_by_hour
                       for o, t in orders.order2deliver_time.items()])

    def action(self, couriers, orders):
        return orders.n_orders, random.choice(range(couriers.n_couriers))

    def step(self, couriers, orders):
        if not orders.end_game:
            orders.step()
            self.update_env(couriers, orders)
            order, courier = self.action(couriers, orders)
            couriers.appoint_order(order, courier)
            self.total_reward(couriers, orders)

