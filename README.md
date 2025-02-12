# create entorno virtual 
/virtualenv env

/env/Scripts/activate.bat

# dependencias
pip install poetry

pip install "gymnasium[classic-control]"

# run el test_gym
py .\test_gym.py

# Ejecutar agentes:
py agente_reactivo_simple.py 

py agente_con_obj.py

py agente_con_memoria.py   
