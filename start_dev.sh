#!/bin/bash

# Inicia a API em background
cd backend
python api.py &
cd ..

# Inicia o simulador de sensores em background
cd backend
python simulador_sensores.py &
cd ..

# Abre o dashboard no navegador padrão
open frontend/dashboard.html
