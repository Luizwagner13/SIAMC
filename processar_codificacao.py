# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    Lida com valores None para os campos de entrada.
    """
    output_final = []

    # Tabela de mapeamento para os códigos 319 e seus excedentes
    # Gerada a partir da entrada do usuário em formato de texto.
    # As chaves são tuplas (min_profundidade, max_profundidade) para facilitar a busca por faixa.
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


    # Helper function to find the correct depth code
    def find_depth_code(profundidade, depth_map):
        for (min_val, max_val), code in depth_map.items():
            if min_val <= profundidade <= max_val:
                return code
        return None

    for item in lista_itens_adicionados:
        codigo = item.get('codigo')

        if codigo == '319 codigos':
            pavimento = item.get('pavimento')
            troca = item.get('troca')
            profundidade_str = item.get('profundidade')
            mts_tubo_batido_str = item.get('mts_tubo_batido')

            # Validação e limpeza dos dados
            if not all([pavimento, troca, profundidade_str, mts_tubo_batido_str]):
                output_final.append(f"ERRO: Dados incompletos para o código {codigo}.")
                continue

            # Converte vírgula para ponto e tenta converter para float
            try:
                profundidade = float(profundidade_str.replace(',', '.'))
                mts_tubo_batido = float(mts_tubo_batido_str.replace(',', '.'))
            except ValueError:
                output_final.append(f"ERRO: Valores de profundidade ou MTS de Tubo Batido inválidos para o código {codigo}.")
                continue

            # Normaliza para maiúsculas para corresponder às chaves da tabela
            pavimento = pavimento.upper().strip()
            troca = troca.upper().strip()

            if pavimento not in tabela_319:
                output_final.append(f"ERRO: Pavimento inválido '{pavimento}' para o código {codigo}.")
                continue
            if troca not in tabela_319[pavimento]:
                output_final.append(f"ERRO: Tipo de troca inválido '{troca}' para o pavimento '{pavimento}' no código {codigo}.")
                continue

            # Lógica para "ATE 2 MTS DE TUBO BATIDO" (código base - 1 UNIDADE)
            base_codes_map = tabela_319[pavimento][troca].get('ATE 2 MTS DE TUBO BATIDO', {})
            base_code = find_depth_code(profundidade, base_codes_map)

            if base_code:
                output_final.append(f"{base_code} - 1 UNIDADE")
            else:
                output_final.append(f"ERRO: Código base 'ATE 2 MTS DE TUBO BATIDO' não encontrado para Pavimento: {pavimento}, Troca: {troca}, Profundidade: {profundidade}.")

            # Lógica para "EXEDENTE" de MTS de Tubo Batido
            excedente_mts_calc = mts_tubo_batido - 2.0 # Assume 2.0 é a base de MTS de Tubo Batido

            if excedente_mts_calc > 0:
                # O código do excedente está na linha 'EXEDENTE' para a mesma combinação
                # de pavimento, troca e FAIXA DE PROFUNDIDADE.
                excedente_codes_map = tabela_319[pavimento][troca].get('EXEDENTE', {})
                excedente_code = find_depth_code(profundidade, excedente_codes_map)

                if excedente_code:
                    output_final.append(f"{excedente_code} - {int(excedente_mts_calc)} METROS") # Formatado como inteiro
                else:
                    output_final.append(f"ERRO: Código de excedente de MTS não encontrado para Pavimento: {pavimento}, Troca: {troca}, Profundidade: {profundidade}.")

        else:
            # Lógica para outros códigos (manter como estava ou ajustar se necessário)
            # Para outros códigos, simplesmente adiciona o código e os detalhes disponíveis
            detalhes = []
            if item.get('pavimento'): detalhes.append(item['pavimento'])
            if item.get('troca'): detalhes.append(item['troca'])
            if item.get('profundidade'): detalhes.append(item['profundidade'])
            if item.get('mts_tubo_batido'): detalhes.append(item['mts_tubo_batido'])
            if item.get('diametro'): detalhes.append(item['diametro'])

            if detalhes:
                output_final.append(f"{codigo} - {' '.join(detalhes)}")
            else:
                output_final.append(str(codigo))

    return "\n".join(output_final)

# --- Exemplo de uso (para testes internos) ---
if __name__ == '__main__':
    print("--- Testes de processamento de códigos ---")

    itens_para_testar = [
        # SEU EXEMPLO QUE DEVE GERAR: 3443 - 1 UNIDADE, 3444 - 7 METROS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.55', 'mts_tubo_batido': '9', 'diametro': ''},

        # Teste 1: Passeio, Sem Troca, Profundidade 1.0 (ATE 1,25), MTS Tubo Batido 1.0 (ATE 2) -> Esperado: 3177 - 1 UNIDADE
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.0', 'diametro': ''},
        # Teste 2: Passeio, Sem Troca, Profundidade 1.0 (ATE 1,25), MTS Tubo Batido 5.0 (ATE 2 + EXCEDENTE) -> Esperado: 3177 - 1 UNIDADE, 3178 - 3 METROS (5-2=3)
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '5.0', 'diametro': ''},

        # Teste 3: Passeio, Sem Troca, Profundidade 2.50 (DE 2,00 A 3,00), MTS Tubo Batido 1.0 (ATE 2) -> Esperado: 3445 - 1 UNIDADE
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '2.50', 'mts_tubo_batido': '1.0', 'diametro': ''},
        # Teste 4: Passeio, Sem Troca, Profundidade 2.50 (DE 2,00 A 3,00), MTS Tubo Batido 7.0 (ATE 2 + EXCEDENTE) -> Esperado: 3445 - 1 UNIDADE, 3446 - 5 METROS (7-2=5)
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '2.50', 'mts_tubo_batido': '7.0', 'diametro': ''},

        # Teste 5: Passeio, Troca Parcial, Profundidade 1.0 (ATE 1,25), MTS Tubo Batido 1.0 (ATE 2) -> Esperado: 3159 - 1 UNIDADE
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '1.0', 'mts_tubo_batido': '1.0', 'diametro': ''},
        # Teste 6: Passeio, Troca Parcial, Profundidade 4.0 (DE 3,00 A 5,00), MTS Tubo Batido 1.0 (ATE 2) -> Esperado: 3810 - 1 UNIDADE
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '4.0', 'mts_tubo_batido': '1.0', 'diametro': ''},
        # Teste 7: Passeio, Troca Parcial, Profundidade 4.0 (DE 3,00 A 5,00), MTS Tubo Batido 5.0 (ATE 2 + EXCEDENTE) -> Esperado: 3810 - 1 UNIDADE, 3811 - 3 METROS
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '4.0', 'mts_tubo_batido': '5.0', 'diametro': ''},

        # Testes com valores inválidos/fora do esperado
        {'codigo': '319 codigos', 'pavimento': None, 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': None, 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Invalida', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': 'abc', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO (profundidade inválida)

        # Testes para outros códigos (que não precisam de lógica específica)
        {'codigo': '300', 'pavimento': None, 'troca': None, 'profundidade': None, 'mts_tubo_batido': None, 'diametro': None},
        {'codigo': '500', 'pavimento': 'Teste', 'troca': 'Outra', 'profundidade': '10', 'mts_tubo_batido': '20', 'diametro': '30'}
    ]

    for i, item in enumerate(itens_para_testar):
        print(f"\n--- Teste {i+1} ---")
        print(f"Entrada: {item}")
        resultado = processar_codigos([item])
        print(f"Saída: \n{resultado}")