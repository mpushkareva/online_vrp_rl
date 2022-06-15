import itertools
from order_courier import Courier


def check(env, courier, route):
    # TODO move courier from rout_idx to next depot pos
    time = env.time
    pos = courier.pos
    for order in route:
        t = ((pos[0] - order.pos[0]) ** 2 + (pos[1] - order.pos[1]) ** 2) ** 0.5 / courier.velocity
        if (t + time > order.deliver_time) or (t + time > env.end_time):  # ?
            return False
        else:
            time = t + time
            pos = order.pos
    return True


def greedy_action(env, order):
    for courier in env.couriers:
        current_route = courier.route[courier.route_idx:]
        if env.depot in current_route:
            depot_idx = current_route.index(env.depot)
            before_depot_idx = depot_idx
            route_after_depot = current_route[depot_idx + 1:]
            route_after_depot_ord = route_after_depot + [order]
        else:
            route_after_depot_ord = [order]
            before_depot_idx = len(current_route) - 1

        for route_var in itertools.permutations(route_after_depot_ord):
            if check(env, courier, route_var):
                courier.route = courier.route[:before_depot_idx] + \
                                [env.depot] + list(route_var)
                return courier, order

    courier = Courier(env.depot, velocity=100)
    if check(env, courier, [order]):
        return courier, order
    else:
        env.done = True
