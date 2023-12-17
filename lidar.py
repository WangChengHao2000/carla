import carla
import numpy as np

import time
import random

from utils import open_carla


def main():
    world = None
    lidar_data = []
    try:
        open_carla()

        client = carla.Client('localhost', 2000)
        client.set_timeout(60000)
        world = client.get_world()

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        # 车辆
        vehicle_spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle_bp = world.get_blueprint_library().find('vehicle.lincoln.mkz_2020')
        vehicle = world.spawn_actor(vehicle_bp, vehicle_spawn_point)
        vehicle.set_autopilot(True)

        # lidar
        lidar_blueprint = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar_blueprint.set_attribute('range', '100')  # 设置感知范围（单位：米）
        lidar_blueprint.set_attribute('rotation_frequency', '10')  # 设置旋转频率（单位：Hz）
        lidar_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        lidar_sensor = world.spawn_actor(lidar_blueprint, lidar_transform, attach_to=vehicle)

        def process_lidar_data(lidar_measurement):
            print(location for location in lidar_measurement)

        lidar_sensor.listen(process_lidar_data)

        for i in range(20):
            world.get_spectator().set_transform(lidar_sensor.get_transform())
            time.sleep(0.2)
            world.tick()

        lidar_sensor.stop()

    finally:
        if world is not None:
            for actor in world.get_actors():
                actor.destroy()
        np.save('./data/lidar_data.npy', np.array(lidar_data, dtype=object))


if __name__ == '__main__':
    main()
