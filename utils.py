import subprocess


def open_carla(carla_path="D://RL4RTA//env//CARLA_0.9.13"):
    command = carla_path + "//CarlaUE4.exe -fps=15 -quality-level=Low"
    subprocess.Popen(command, shell=True)


if __name__ == '__main__':
    open_carla()
