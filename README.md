Para executar a prova a seguir, deve-se fazer o seguinte:

1. Abrir o terminal de seu Linux Ubuntu versão 22.04

2. Entrar no diretório desta prova
```bash
cd prova
```

3. Buildar utilizando o colcon 
```bash
colcon build
```

4. Dar source no seu local_setup.bash
```bash
source install/local_setup.bash
```

5. Rodar o nó do turtlesim
```bash
ros2 run turtlesim turtlesim_node
```

6. Rodar a tartaruga 
```bash
ros2 run prova prova
```

7. Rodar a CLI
```bash
ros2 run cli cli VALORX, VALORY, TEMPO
```