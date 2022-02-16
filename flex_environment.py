import numpy as np


class Orders:
    def __init__(self, start_time, end_time, prob_per_min, time2deliver, pos_distrib):
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

    def order_pos_distribution(self, order):
        if self.pos_distrib == 'normal':
            self.order2pos[order] = np.random.normal(50, 100, size=2)

    def step(self):
        for t in range(self.end_time - self.time):
            is_new_order = np.random.choice([0, 1], size=1, p=[1 - self.prob_per_min, self.prob_per_min])
            if is_new_order:
                # self.orders = list(range(n_orders))
                self.order_pos_distribution(self.n_orders)
                self.order2deliver_time[self.n_orders] = self.time + t + self.time2deliver
                self.n_orders += 1
                self.time += t
        self.time = self.end_time
        self.end_game = True


class Couriers:
    def __init__(self, n_couriers, depot_pos, velocity, start_time):
        self.depot_pos = depot_pos
        self.velocity = velocity
        self.n_couriers = n_couriers
        self.courier2orders = {k: [] for k in range(n_couriers)}
        self.courier2pos = {k: depot_pos for k in range(n_couriers)}
        self.courier2orders_hist = {k: [] for k in range(n_couriers)}
        self.courier2pos_hist = {k: [depot_pos] for k in range(n_couriers)}
        self.courier_works = {k: False for k in range(n_couriers)}
        self.time_prev = start_time
        self.depot = 'd' # !!!

    def get_pos(self, time, orders):
        for courier in range(self.n_couriers):
            last_pos = self.courier2orders_hist[courier]
            period = time -self.time_prev
            for order_id in self.courier2orders[courier]:
                t = np.sqrt()

        self.time_prev = time

    def appoint_order(self, orders, courier_id):
        last_order = orders.n_orders
        if self.depot in self.courier2orders[courier_id]:
            self.courier2orders[courier_id].append(last_order)
            self.courier2orders_hist[courier_id].append(last_order)
        else:
            self.courier2orders[courier_id].extend([self.depot, last_order])