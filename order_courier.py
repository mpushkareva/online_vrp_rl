# TODO import fresh libraries
class Order:
    def __init__(self, order_id, deliver_time, pos):
        self.order_id = order_id
        self.deliver_time = deliver_time
        self.pos = pos
        self.is_completed = False
        self.completed_order2time = None

    def complete_order(self, time):
        self.is_completed = True
        self.completed_order2time = time


class Depot:
    def __init__(self, depot_pos):
        self.pos = depot_pos


class Courier:
    def __init__(self, depot, velocity=100):
        self.velocity = velocity
        self.depot = depot
        self.route = [depot]
        self.pos = depot.pos
        self.route_idx = 0
        self.is_working = False

    def appoint_order(self, order):
        if self.depot in self.route[self.route_idx:]:
            self.route.append(order)
        else:
            self.route.extend([self.depot, order])
        self.is_working = True

    def update_position(self, period, time):
        while self.route_idx != len(self.route) - 1:
            route_point = self.route[self.route_idx]
            next_pos = self.depot.pos if route_point == self.depot else route_point.pos
            t = ((self.pos[0] - next_pos[0]) ** 2 + (self.pos[1] - next_pos[1]) ** 2) ** 0.5 / self.velocity
            if t >= period:
                self.pos = (self.pos[0] + (next_pos[0] - self.pos[0]) * period / t,
                            self.pos[1] + (next_pos[1] - self.pos[1]) * period / t)
                break
            else:
                period = period - t
                self.route_idx += 1
                self.pos = next_pos
                time += t
                if route_point != self.depot:
                    route_point.complete_order(time)

