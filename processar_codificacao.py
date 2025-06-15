# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    Lida com valores None para os campos de entrada.
    """
    output_final = []

    # Tabela de mapeamento para os códigos 319 e seus excedentes
    # Os nomes das chaves (PASSEIO, RUA, ASPHALTIC) devem estar em MAIÚSCULAS
    tabela_319 = {
        'PASSEIO': {
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3810',
                    (1.25, 2.00): '3811',
                    (2.00, 3.00): '3812',
                    (3.00, 5.00): '3813'
                },
                'codigo_excedente_mts': '3811'
            },
            'TROCA PARCIAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3830',
                    (1.25, 2.00): '3831',
                    (2.00, 3.00): '3832',
                    (3.00, 5.00): '3833'
                },
                'codigo_excedente_mts': '3831'
            },
            'TROCA TOTAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3850', # Adicionado 3850
                    (1.25, 2.00): '3851', # Adicionado 3851
                    (2.00, 3.00): '3852',
                    (3.00, 5.00): '3853'
                },
                'codigo_excedente_mts': '3851' # O código para o excedente de MTS (conforme discutido)
            }
        },
        'RUA': {
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3820',
                    (1.25, 2.00): '3821',
                    (2.00, 3.00): '3822',
                    (3.00, 5.00): '3823'
                },
                'codigo_excedente_mts': '3821'
            },
            'TROCA PARCIAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3840',
                    (1.25, 2.00): '3841',
                    (2.00, 3.00): '3842',
                    (3.00, 5.00): '3843'
                },
                'codigo_excedente_mts': '3841'
            },
            'TROCA TOTAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3860',
                    (1.25, 2.00): '3861',
                    (2.00, 3.00): '3862',
                    (3.00, 5.00): '3863'
                },
                'codigo_excedente_mts': '3861'
            }
        },
        'ASPHALTIC': { # Supondo que 'ASPHALTIC' também é um tipo de pavimento
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3870',
                    (1.25, 2.00): '3871',
                    (2.00, 3.00): '3872',
                    (3.00, 5.00): '3873'
                },
                'codigo_excedente_mts': '3871'
            },
            'TROCA PARCIAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3880',
                    (1.25, 2.00): '3881',
                    (2.00, 3.00): '3882',
                    (3.00, 5.00): '3883'
                },
                'codigo_excedente_mts': '3881'
            },
            'TROCA TOTAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3890',
                    (1.25, 2.00): '3891',
                    (2.00, 3.00): '3892',
                    (3.00, 5.00): '3893'
                },
                'codigo_excedente_mts': '3891'
            }
        }
    }

    # Código para outros tipos de trabalho que não o 319 e suas variantes
    outros_codigos = {
        '300': 'Código 300 Padrão',
        '301': 'Código 301 Padrão',
        '302': 'Código 302 Padrão',
        '303': 'Código 303 Padrão',
        '304': 'Código 304 Padrão',
        '305': 'Código 305 Padrão',
        '306': 'Código 306 Padrão',
        '307': 'Código 307 Padrão',
        '308': 'Código 308 Padrão',
        '309': 'Código 309 Padrão',
        '310': 'Código 310 Padrão',
        '311': 'Código 311 Padrão',
        '312': 'Código 312 Padrão',
        '313': 'Código 313 Padrão',
        '314': 'Código 314 Padrão',
        '315': 'Código 315 Padrão',
        '316': 'Código 316 Padrão',
        '317': 'Código 317 Padrão',
        '318': 'Código 318 Padrão',
        # ... e assim por diante
    }

    for item in lista_itens_adicionados:
        codigo_entrada = item.get('codigo')
        pavimento_entrada = item.get('pavimento')
        troca_entrada = item.get('troca')
        profundidade_entrada = item.get('profundidade')
        mts_tubo_batido_entrada = item.get('mts_tubo_batido')
        diametro_entrada = item.get('diametro')

        # Normaliza as strings para maiúsculas e remove acentos/espaços extras para correspondência
        # Usamos str() para garantir que None não cause erro ao chamar .strip() ou .upper()
        pavimento_normalizado = str(pavimento_entrada).strip().upper() if pavimento_entrada else None
        troca_normalizada = str(troca_entrada).strip().upper() if troca_entrada else None

        # Tratamento para o código '319' e suas variações
        if codigo_entrada and ('319' in codigo_entrada or '319 codigos' in codigo_entrada):
            if not all([pavimento_normalizado, troca_normalizada, profundidade_entrada]):
                output_final.append(f"ERRO: Dados incompletos para o código 319 (pavimento, troca ou profundidade ausentes). Item: {item}")
                continue

            # >>>>>>>>>>> INÍCIO DA CORREÇÃO <<<<<<<<<<<
            # Substitui vírgula por ponto para permitir a conversão para float
            if isinstance(profundidade_entrada, str):
                profundidade_entrada = profundidade_entrada.replace(',', '.')
            if isinstance(mts_tubo_batido_entrada, str):
                mts_tubo_batido_entrada = mts_tubo_batido_entrada.replace(',', '.')
            # >>>>>>>>>> FIM DA CORREÇÃO <<<<<<<<<<<

            try:
                profundidade = float(profundidade_entrada)
                # Garante que mts_tubo_batido_entrada seja um float ou 0.0 se for None/vazio/inválido
                mts_tubo_batido = float(mts_tubo_batido_entrada) if mts_tubo_batido_entrada else 0.0
            except (ValueError, TypeError):
                output_final.append(f"ERRO: Profundidade ou MTS Tubo Batido inválidos para o código 319. Item: {item}")
                continue

            if pavimento_normalizado in tabela_319 and troca_normalizada in tabela_319[pavimento_normalizado]:
                regras_atuais = tabela_319[pavimento_normalizado][troca_normalizada]
                codigo_base_encontrado = False
                codigo_base = None

                # Encontrar o código base pela profundidade
                for (min_p, max_p), codigo in regras_atuais['profundidades_base'].items():
                    if min_p <= profundidade <= max_p:
                        codigo_base = codigo
                        codigo_base_encontrado = True
                        break
                
                # Se a profundidade for maior que a última faixa, pega o último código base da tabela
                if not codigo_base_encontrado:
                    # Encontra a maior profundidade na tabela e usa seu código correspondente
                    maior_profundidade_faixa = max(regras_atuais['profundidades_base'].keys(), key=lambda x: x[1])
                    codigo_base = regras_atuais['profundidades_base'][maior_profundidade_faixa]
                    codigo_base_encontrado = True
                    output_final.append(f"ATENÇÃO: Profundidade {profundidade} excede as faixas definidas para o código 319 (pavimento: {pavimento_entrada}, troca: {troca_entrada}). Usando o código base para a maior profundidade ({codigo_base}).")

                if codigo_base_encontrado:
                    # Adiciona o código base
                    output_final.append(codigo_base)

                    # Lógica para excedente de MTS Tubo Batido
                    # O "excedente" é o valor de mts_tubo_batido menos a profundidade do furo.
                    excedente_mts = mts_tubo_batido - profundidade

                    if excedente_mts > 0:
                        codigo_excedente = regras_atuais.get('codigo_excedente_mts')
                        if codigo_excedente:
                            # Formata o excedente para duas casas decimais
                            output_final.append(f"{codigo_excedente} {excedente_mts:.2f} MTS")
                        else:
                            output_final.append(f"ATENÇÃO: Código de excedente MTS não definido para {pavimento_entrada} / {troca_entrada}.")
            else:
                output_final.append(f"ERRO: Combinação de Pavimento ('{pavimento_entrada}') e/ou Troca ('{troca_entrada}') inválida para o código 319. Item: {item}")
        
        # Tratamento para outros códigos
        elif codigo_entrada in outros_codigos:
            # Para códigos simples, adiciona o código e o diâmetro se existir
            # Remove espaços extras se o diâmetro não existir
            output_final.append(f"{codigo_entrada} {diametro_entrada or ''}".strip()) 
        
        # Caso o código não seja 319 nem esteja em 'outros_codigos'
        elif codigo_entrada:
            output_final.append(f"Código '{codigo_entrada}' não reconhecido ou sem lógica específica de processamento.")
        else:
            output_final.append("ERRO: Código não fornecido para um item.")
            
    return output_final

# Exemplo de uso para testes (será removido ou comentado na versão final para integração Flask)
if __name__ == '__main__':
    # Testes unitários para a função processar_codigos
    test_cases = [
        # Testes para o código 319 - PASSEIO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3810, 3811 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.5', 'mts_tubo_batido': '1.75', 'diametro': ''}, # Esperado: 3811, 3811 0.25 MTS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '2.5', 'mts_tubo_batido': '3.0', 'diametro': ''}, # Esperado: 3812, 3811 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '4.0', 'mts_tubo_batido': '5.0', 'diametro': ''}, # Esperado: 3813, 3811 1.00 MTS

        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3830, 3831 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '1.5', 'mts_tubo_batido': '2.0', 'diametro': ''}, # Esperado: 3831, 3831 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Total', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3850, 3851 0.50 MTS (NOVO)
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Total', 'profundidade': '1.5', 'mts_tubo_batido': '1.75', 'diametro': ''}, # Esperado: 3851, 3851 0.25 MTS (NOVO)

        # Testes para o código 319 - RUA
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3820, 3821 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': '1.5', 'mts_tubo_batido': '1.75', 'diametro': ''}, # Esperado: 3821, 3821 0.25 MTS
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Troca Parcial', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3840, 3841 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Troca Total', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3860, 3861 0.50 MTS (NOVO)

        # Testes para o código 319 - ASPHALTIC (Exemplo)
        {'codigo': '319 codigos', 'pavimento': 'Asphaltic', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3870, 3871 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Asphaltic', 'troca': 'Troca Parcial', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3880, 3881 0.50 MTS
        {'codigo': '319 codigos', 'pavimento': 'Asphaltic', 'troca': 'Troca Total', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 3890, 3891 0.50 MTS

        # Testes com excedente de MTS Tubo Batido
        {'codigo': '319', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': '1.5', 'mts_tubo_batido': '4.0', 'diametro': ''}, # Excedente de 2.50 MTS
        {'codigo': '319', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': '4.8', 'mts_tubo_batido': '5.25', 'diametro': ''}, # Excedente de 0.45 MTS
        {'codigo': '319', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '2.8', 'mts_tubo_batido': '2.1', 'diametro': ''}, # Sem excedente, mts_tubo_batido < profundidade. Output: 3832

        # Testes com valores inválidos/fora do esperado
        {'codigo': '319 codigos', 'pavimento': None, 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': None, 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': None, 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Invalida', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': 'abc', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO (profundidade inválida)
        
        # O seu caso específico de erro, agora deve funcionar:
        {'codigo': '319', 'diametro': None, 'mts_tubo_batido': '4', 'pavimento': 'PASSEIO', 'profundidade': '1,25', 'troca': 'SEM TROCA'},
        {'codigo': '319', 'diametro': None, 'mts_tubo_batido': '4,5', 'pavimento': 'PASSEIO', 'profundidade': '1.25', 'troca': 'SEM TROCA'}, # MTS Tubo Batido com vírgula

        # Testes para outros códigos (que não precisam de lógica específica)
        {'codigo': '300', 'pavimento': None, 'troca': None, 'profundidade': None, 'mts_tubo_batido': None, 'diametro': '100mm'}, # Esperado: 300 100mm
        {'codigo': '301', 'pavimento': None, 'troca': None, 'profundidade': None, 'mts_tubo_batido': None, 'diametro': ''}, # Esperado: 301
    ]

    print("--- Resultados dos Testes ---")
    for i, test_case in enumerate(test_cases):
        print(f"\nTeste {i+1}: Entrada: {test_case}")
        resultado = processar_codigos([test_case])
        print(f"Resultado: {resultado}")