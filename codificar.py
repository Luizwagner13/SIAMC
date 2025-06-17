# tabela de códigos para o código 313
CODIGOS_313 = [
    {"codigo": 3078, "prof_min": 0.00, "prof_max": 1.25, "pavimento": "CIMENTO"},
    {"codigo": 3075, "prof_min": 0.00, "prof_max": 1.25, "pavimento": "TERRA"},
    {"codigo": 3412, "prof_min": 1.25, "prof_max": 2.00, "pavimento": "CIMENTO"},
    {"codigo": 3409, "prof_min": 1.25, "prof_max": 2.00, "pavimento": "TERRA"},
    {"codigo": 3413, "prof_min": 2.00, "prof_max": 3.00, "pavimento": "CIMENTO"},
    {"codigo": 3410, "prof_min": 2.00, "prof_max": 3.00, "pavimento": "TERRA"},
]

def codificar_313(pavimento: str, profundidade: float):
    pavimento = pavimento.strip().upper()
    for item in CODIGOS_313:
        if (item['pavimento'] == pavimento and
            item['prof_min'] <= profundidade < item['prof_max']):
            return item['codigo']
    return None

if __name__ == "__main__":
    pavimento = input("Informe o pavimento (CIMENTO ou TERRA): ")
    profundidade_str = input("Informe a profundidade (ex: 1.80): ")
    try:
        profundidade = float(profundidade_str.replace(',', '.'))
    except ValueError:
        print("Profundidade inválida.")
        exit(1)

    codigo = codificar_313(pavimento, profundidade)
    if codigo:
        print(f"Código OS: {codigo} - 1 unidade")
    else:
        print("Nenhum código encontrado para os parâmetros informados.")
