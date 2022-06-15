import numpy as np
import random

from order_courier import Order, Depot, Courier
from greedy import greedy_action


class Environment:
    def __init__(self, courier_pay=1500, depot_pos=(0, 0), penalty_by_hour=300, reward_by_order=300, gamma=1,
                 pos_distrib='normal', start_time=9*60, end_time=21*60, prob_per_min=0.5, time2deliver=2*60,
                 action_type='greedy'):
        self.depot = Depot(depot_pos)
        self.courier_pay = courier_pay
        self.penalty_by_hour = penalty_by_hour
        self.reward_by_order = reward_by_order
        self.gamma = gamma  # кажется, что не имеет смысла в данной постановке задачи
        self.pos_distrib = pos_distrib
        self.start_time = start_time
        self.end_time = end_time
        self.prob_per_min = prob_per_min
        self.time2deliver = time2deliver
        self.action_type = action_type

    def update_env(self, period, time):
        for courier in self.couriers:
            courier.update_position(period, time)

    def order_pos_distribution(self):
        if self.pos_distrib == 'normal':
            return np.random.normal(0, 3000, size=2)

    def reset(self):
        self.couriers = [Courier(self.depot, velocity=100)]
        self.orders = []
        self.rewards = []
        self.done = False
        self.time = self.start_time

        for period in range(1, self.end_time - self.time):
            is_new_order = np.random.choice([0, 1], size=1, p=[1 - self.prob_per_min, self.prob_per_min])
            if is_new_order:
                self.orders.append(Order(len(self.orders), self.time + period + self.time2deliver,
                                         self.order_pos_distribution()))
                self.update_env(period, self.time)
                self.time += period
                return self.total_reward(), self.done  # reward, done
        self.done = True
        return self.total_reward(), self.done

    def step(self, action):
        # action = (courier_id, order_id)
        if not self.done: # probable should be removed
            action[0].appoint_order(action[1])
            for t in range(1, self.end_time - self.time):
                is_new_order = np.random.choice([0, 1], size=1, p=[1 - self.prob_per_min, self.prob_per_min])
                if is_new_order:
                    self.orders.append(Order(len(self.orders), self.time + t + self.time2deliver,
                                             self.order_pos_distribution()))
                    self.update_env(t, self.time)
                    self.time += t

                    return self.total_reward(), False  # reward, done
            self.time = self.end_time
            return self.total_reward(), True
        else:
            self.total_reward(), True

    def total_reward(self):
        overtimes = (order.completed_order2time - order.deliver_time if order.is_completed
                     else self.time - order.deliver_time for order in self.orders)
        # Стоимость работы дня курьера + награда за выполненный заказ + штраф за заказ не выполненный вовремя.
        reward = - sum((courier.is_working for courier in self.couriers)) * self.courier_pay + \
                      self.reward_by_order * sum((order.is_completed for order in self.orders)) + \
                      sum((max(overtime, 0) * self.penalty_by_hour for overtime in overtimes))
        self.rewards.append(reward)
        return reward

    def action(self):
        if self.action_type == 'greedy':
            return greedy_action(self, self.orders[-1])
        else:
            return random.choice(self.couriers), self.orders[-1]
