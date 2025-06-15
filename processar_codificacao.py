# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    Lida com valores None para os campos de entrada.
    """
    output_final = []

    # Tabela de mapeamento para os códigos 319 e seus excedentes
    # Gerada a partir da entrada do usuário.
    # A profundidade é mapeada como (min_val, max_val) ou (min_val, float('inf'))
    tabela_319 = {
        'PASSEIO': {
            'SEM TROCA': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3177,
                    (1.25, 2.00): 3443,
                    (2.00, 3.00): 3445,
                    (3.00, 5.00): 3816
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3178,
                    (1.25, 2.00): 3444,
                    (2.00, 3.00): 3446,
                    (3.00, 5.00): 3817
                }
            },
            'TROCA PARCIAL': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3159,
                    (1.25, 2.00): 3431,
                    (2.00, 3.00): 3433,
                    (3.00, 5.00): 3810
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3160,
                    (1.25, 2.00): 3432,
                    (2.00, 3.00): 3434,
                    (3.00, 5.00): 3811
                }
            },
            'TROCA TOTAL': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3141,
                    (1.25, 2.00): 3419,
                    (2.00, 3.00): 3421,
                    (3.00, 5.00): 3804
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3142,
                    (1.25, 2.00): 3420,
                    (2.00, 3.00): 3422,
                    (3.00, 5.00): 3805
                }
            }
        },
        'RUA': {
            'SEM TROCA': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3183,
                    (1.25, 2.00): 3447,
                    (2.00, 3.00): 3449,
                    (3.00, 5.00): 3818
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3184,
                    (1.25, 2.00): 3448,
                    (2.00, 3.00): 3450,
                    (3.00, 5.00): 3819
                }
            },
            'TROCA PARCIAL': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3165,
                    (1.25, 2.00): 3435,
                    (2.00, 3.00): 3437,
                    (3.00, 5.00): 3812
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3166,
                    (1.25, 2.00): 3436,
                    (2.00, 3.00): 3438,
                    (3.00, 5.00): 3813
                }
            },
            'TROCA TOTAL': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3147,
                    (1.25, 2.00): 3423,
                    (2.00, 3.00): 3425,
                    (3.00, 5.00): 3806
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3148,
                    (1.25, 2.00): 3424,
                    (2.00, 3.00): 3426,
                    (3.00, 5.00): 3807
                }
            }
        },
        'TERRA': {
            'SEM TROCA': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3171,
                    (1.25, 2.00): 3439,
                    (2.00, 3.00): 3441,
                    (3.00, 5.00): 3814
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3172,
                    (1.25, 2.00): 3440,
                    (2.00, 3.00): 3442,
                    (3.00, 5.00): 3815
                }
            },
            'TROCA PARCIAL': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3153,
                    (1.25, 2.00): 3427,
                    (2.00, 3.00): 3429,
                    (3.00, 5.00): 3808
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3154,
                    (1.25, 2.00): 3428,
                    (2.00, 3.00): 3430,
                    (3.00, 5.00): 3809
                }
            },
            'TROCA TOTAL': {
                'ATE 2 MTS DE TUBO BATIDO': {
                    (0.0, 1.25): 3135,
                    (1.25, 2.00): 3415,
                    (2.00, 3.00): 3417,
                    (3.00, 5.00): 3802
                },
                'EXEDENTE': {
                    (0.0, 1.25): 3136,
                    (1.25, 2.00): 3416,
                    (2.00, 3.00): 3418,
                    (3.00, 5.00): 3803
                }
            }
        }
    }


    # Helper function to find the correct depth range
    def find_depth_code(profundidade, depth_map):
        for (min_val, max_val), code in depth_map.items():
            if min_val <= profundidade <= max_val:
                return code
        return None

    for item in lista_itens_adicionados:
        codigo_selecionado = item.get('codigo')

        if codigo_selecionado == '319 codigos':
            pavimento = item.get('pavimento')
            troca = item.get('troca')
            profundidade_str = item.get('profundidade')
            mts_tubo_batido_str = item.get('mts_tubo_batido')

            # Validação e limpeza dos dados
            if not all([pavimento, troca, profundidade_str, mts_tubo_batido_str]):
                output_final.append(f"ERRO: Dados incompletos para o código {codigo_selecionado}. Verifique Pavimento, Troca, Profundidade e Metros de Tubo Batido.")
                continue

            # Converte vírgula para ponto e tenta converter para float
            try:
                profundidade = float(profundidade_str.replace(',', '.'))
                mts_tubo_batido = float(mts_tubo_batido_str.replace(',', '.'))
            except ValueError:
                output_final.append(f"ERRO: Valores de profundidade ou Metros de Tubo Batido inválidos para o código {codigo_selecionado}.")
                continue

            # Normaliza para maiúsculas para corresponder às chaves da tabela
            pavimento_upper = pavimento.upper().strip()
            troca_upper = troca.upper().strip()

            if pavimento_upper not in tabela_319:
                output_final.append(f"ERRO: Pavimento inválido '{pavimento}' para o código {codigo_selecionado}.")
                continue
            if troca_upper not in tabela_319[pavimento_upper]:
                output_final.append(f"ERRO: Tipo de troca inválido '{troca}' para o pavimento '{pavimento}' no código {codigo_selecionado}.")
                continue

            # Lógica para "ATE 2 MTS DE TUBO BATIDO" (Unidade Base)
            base_codes_map = tabela_319[pavimento_upper][troca_upper].get('ATE 2 MTS DE TUBO BATIDO', {})
            base_code = find_depth_code(profundidade, base_codes_map)

            if base_code:
                output_final.append(f"{base_code} - 1 UNIDADE")
            else:
                output_final.append(f"ERRO: Código base não encontrado para Pavimento: {pavimento}, Troca: {troca}, Profundidade: {profundidade}.")

            # Lógica para "EXEDENTE" de MTS de Tubo Batido
            excedente_mts_calc = mts_tubo_batido - 2.0 # Assume 2.0 é a base de MTS de Tubo Batido

            if excedente_mts_calc > 0:
                # O código do excedente está na seção 'EXEDENTE' para a mesma profundidade/pavimento/troca
                excedente_codes_map = tabela_319[pavimento_upper][troca_upper].get('EXEDENTE', {})
                excedente_code = find_depth_code(profundidade, excedente_codes_map)

                if excedente_code:
                    output_final.append(f"{excedente_code} - {int(excedente_mts_calc)} METROS") # Formatado como inteiro
                else:
                    output_final.append(f"ERRO: Código de excedente de MTS não encontrado para Pavimento: {pavimento}, Troca: {troca}, Profundidade: {profundidade}.")

        elif codigo_selecionado == '321 codigos':
            pavimento = item.get('pavimento')
            troca = item.get('troca')
            diametro = item.get('diametro')
            
            if not all([pavimento, troca, diametro]):
                output_final.append(f"ERRO: Dados incompletos para o código {codigo_selecionado}. Verifique Pavimento, Tipo de Troca e Diâmetro.")
                continue
            
            output_final.append(f"{codigo_selecionado} - {pavimento} {troca} {diametro}")

        elif codigo_selecionado == '313 codigos':
            diametro = item.get('diametro')
            if not diametro:
                output_final.append(f"ERRO: Diâmetro não fornecido para o código {codigo_selecionado}.")
                continue
            output_final.append(f"{codigo_selecionado} - {diametro}")

        elif codigo_selecionado == '320 (rec) codigos':
            diametro = item.get('diametro')
            pavimento = item.get('pavimento')
            if not all([diametro, pavimento]):
                output_final.append(f"ERRO: Dados incompletos para o código {codigo_selecionado}. Verifique Diâmetro e Pavimento.")
                continue
            output_final.append(f"{codigo_selecionado} - {diametro} {pavimento}")

        elif codigo_selecionado == '300 codigos':
            diametro = item.get('diametro')
            pavimento = item.get('pavimento')
            if not all([diametro, pavimento]):
                output_final.append(f"ERRO: Dados incompletos para o código {codigo_selecionado}. Verifique Diâmetro e Pavimento.")
                continue
            output_final.append(f"{codigo_selecionado} - {diametro} {pavimento}")

        elif codigo_selecionado == '343 codigos':
            diametro = item.get('diametro')
            pavimento = item.get('pavimento')
            troca = item.get('troca')
            if not all([diametro, pavimento, troca]):
                output_final.append(f"ERRO: Dados incompletos para o código {codigo_selecionado}. Verifique Diâmetro, Pavimento e Tipo de Troca.")
                continue
            output_final.append(f"{codigo_selecionado} - {diametro} {pavimento} {troca}")

        elif codigo_selecionado == '329 codigos':
            diametro = item.get('diametro')
            pavimento = item.get('pavimento')
            troca = item.get('troca')
            if not all([diametro, pavimento, troca]):
                output_final.append(f"ERRO: Dados incompletos para o código {codigo_selecionado}. Verifique Diâmetro, Pavimento e Tipo de Troca.")
                continue
            output_final.append(f"{codigo_selecionado} - {diametro} {pavimento} {troca}")

        else:
            # Lógica para outros códigos genéricos ou não mapeados especificamente
            detalhes = []
            if item.get('pavimento'): detalhes.append(item['pavimento'])
            if item.get('troca'): detalhes.append(item['troca'])
            if item.get('profundidade'): detalhes.append(item['profundidade'])
            if item.get('mts_tubo_batido'): detalhes.append(item['mts_tubo_batido'])
            if item.get('diametro'): detalhes.append(item['diametro'])

            if detalhes:
                output_final.append(f"{codigo_selecionado} - {' '.join(filter(None, detalhes))}") # filter(None, ...) remove vazios
            else:
                output_final.append(str(codigo_selecionado))

    return "\n".join(output_final)

# --- Exemplo de uso (para testes internos) ---
if __name__ == '__main__':
    print("--- Testes de processamento de códigos ---")

    # Seu exemplo: 3443 - 1 UNIDADE, 3444 - 7 METROS
    # (3443 é para DE 1,25 A 2,00 MTS DE PROFUNDIDADE. 1.55 está dentro)
    # (9 MTS de Tubo Batido - 2 MTS base = 7 MTS excedente)
    itens_para_testar = [
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.55', 'mts_tubo_batido': '9', 'diametro': ''},
        
        # Teste 1: Passeio, Sem Troca, Profundidade 1.0 (ATE 1,25), MTS Tubo Batido 1.0 (ATE 2) -> Esperado: 3177 - 1 UNIDADE
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.0', 'diametro': ''},
        
        # Teste 2: Passeio, Sem Troca, Profundidade 1.0 (ATE 1,25), MTS Tubo Batido 5.0 (ATE 2 + EXCEDENTE) -> Esperado: 3177 - 1 UNIDADE, 3178 - 3 METROS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '5.0', 'diametro': ''},
        
        # Teste 3: Passeio, Troca Parcial, Profundidade 1.0 (ATE 1,25), MTS Tubo Batido 1.0 (ATE 2) -> Esperado: 3159 - 1 UNIDADE
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '1.0', 'mts_tubo_batido': '1.0', 'diametro': ''},
        
        # Teste 4: Passeio, Troca Parcial, Profundidade 4.0 (DE 3,00 A 5,00), MTS Tubo Batido 1.0 (ATE 2) -> Esperado: 3810 - 1 UNIDADE
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '4.0', 'mts_tubo_batido': '1.0', 'diametro': ''},
        
        # Teste 5: Passeio, Troca Parcial, Profundidade 4.0 (DE 3,00 A 5,00), MTS Tubo Batido 5.0 (ATE 2 + EXCEDENTE) -> Esperado: 3810 - 1 UNIDADE, 3811 - 3 METROS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '4.0', 'mts_tubo_batido': '5.0', 'diametro': ''},

        # Testes com valores inválidos/fora do esperado (para verificar as mensagens de erro)
        {'codigo': '319 codigos', 'pavimento': None, 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # ERRO: Dados incompletos
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': None, 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # ERRO: Dados incompletos
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Invalida', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # ERRO: Tipo de troca inválido
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': 'abc', 'mts_tubo_batido': '1.5', 'diametro': ''}, # ERRO: Valores inválidos

        # Testes para outros códigos (que não precisam de lógica específica complexa)
        {'codigo': '300 codigos', 'diametro': '150', 'pavimento': 'Rua', 'troca': None, 'profundidade': None, 'mts_tubo_batido': None},
        {'codigo': '313 codigos', 'diametro': '200', 'pavimento': None, 'troca': None, 'profundidade': None, 'mts_tubo_batido': None},
        {'codigo': '500 OUTROS', 'diametro': '50', 'pavimento': 'Passeio', 'troca': 'Completa', 'profundidade': '2.5', 'mts_tubo_batido': '10'}
    ]

    for i, item in enumerate(itens_para_testar):
        print(f"\n--- Teste {i+1} ---")
        print(f"Entrada: {item}")
        resultado = processar_codigos([item])
        print(f"Saída:\n{resultado}")