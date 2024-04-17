import os
import csv
from datetime import datetime
from pathlib import Path

pendentes_dir = Path("/PENDENTES")
validado_dir = Path("/VALIDADO")
invalidado_dir = Path("/INVALIDADO")

[dir.mkdir(parents=True, exist_ok=True) for dir in (validado_dir, invalidado_dir)]

for csv_file in pendentes_dir.glob("*.csv"):
    try:
    
        valid_file = True
        num_columns = 4
        seen_numero_da_venda = set()

    
        with open(csv_file, newline="") as file:
            reader = csv.reader(file, delimiter=";")

        
            next(reader)
            for i, row in enumerate(reader, start=2):
                if not row:
                    print(f"Errolinha {i}: Arquivo possui linhas em branco.")
                    valid_file = False
                    continue

                if len(row) != num_columns:
                    print(f"Errolinha {i}: Número inválido de colunas.")
                    valid_file = False
                    continue

                numero_da_venda, nome_do_cliente, data_da_venda, valor_da_venda = row

                if not all((numero_da_venda, nome_do_cliente, data_da_venda, valor_da_venda)):
                    print(f"Errolinha {i}: Campos obrigatórios faltando.")
                    valid_file = False
                    continue

                try:
                    data_da_venda = datetime.strptime(data_da_venda, "%d/%m/%Y")
                except ValueError:
                    print(f"Errolinha {i}: Formato de data inválido.")
                    valid_file = False
                    continue

                if data_da_venda > datetime.now():
                    print(f"Errolinha {i}: Data futura.")
                    valid_file = False
                    continue

                try:
                    valor_da_venda = float(valor_da_venda)
                except ValueError:
                    print(f"Errolinha {i}: Valor da venda inválido.")
                    valid_file = False
                    continue

                if valor_da_venda <= 0:
                    print(f"Errolinha {i}: Valor da venda deve ser maior que zero.")
                    valid_file = False
                    continue

                if numero_da_venda in seen_numero_da_venda:
                    print(f"Errolinha {i}: Número da venda duplicado.")
                    valid_file = False
                    continue

                seen_numero_da_venda.add(numero_da_venda)

    except Exception as e:
        print(f"Erro na leitura do arquivo {csv_file}: {e}")
        valid_file = False


    if valid_file:
        csv_file.rename(validado_dir / csv_file.name)
    else:
        csv_file.rename(invalidado_dir / csv_file.name)