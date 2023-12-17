import carla
import cv2
import numpy as np

import time
import random


def main():
    world = None
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2000)
        world = client.get_world()

        # 车辆
        vehicle_spawn_point = random.choice(world.get_map().get_spawn_points())
        vehicle_bp = world.get_blueprint_library().find('vehicle.lincoln.mkz_2020')
        vehicle = world.spawn_actor(vehicle_bp, vehicle_spawn_point)
        vehicle.set_autopilot(True)

        # RGB相机
        camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(z=2))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)

        def show_image(image):
            img = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4))
            cv2.imwrite('./data/rgb/test' + str(time.time()) + '.jpg', img)

        camera.listen(lambda image: show_image(image))

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        # while True:
        #     world.get_spectator().set_transform(camera.get_transform())
        #     time.sleep(0.2)
        #     world.tick()

        world.get_spectator().set_transform(camera.get_transform())
        world.tick()

    finally:
        if world is not None:
            for actor in world.get_actors():
                actor.destroy()


if __name__ == '__main__':
    main()
