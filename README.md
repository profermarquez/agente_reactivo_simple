# create entorno virtual 
virtualenv env

/env/Scripts activate

# dependencias
pip install poetry

pip install "gymnasium[classic-control]"

# run el test_gym
py .\test_gym.py

# Run Ejemplo de Agente reactivo simple
py .\agente_reactivo_simple.py 
