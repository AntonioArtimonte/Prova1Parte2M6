Para executar a prova a seguir, deve-se fazer o seguinte:

1. Abrir o terminal de seu Linux Ubuntu versão 22.04

```bash
cd prova
```

```bash
colcon build
```

```bash
source install/local_setup.bash
```

```bash
ros2 run turtlesim turtlesim_node
```

```bash
ros2 run prova prova
```

```bash
ros2 run cli cli
```