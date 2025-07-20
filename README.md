# Clearwave Agente Interativo

Este projeto contém o agente de monitoramento de relatórios Clearwave.

## Como gerar o executável

1. Certifique-se de ter Python 3.10+ instalado.
2. Execute o script `installer/build_exe.bat` para gerar os arquivos `.exe` na
   pasta `dist`.

## Estrutura do projeto

- `app/ui/main_interactive.py`: Interface principal (Tkinter)
- `app/core/monitor.py`: Lógica de monitoramento
- `installer/build_exe.bat`: Script para gerar executáveis

## Dependências

- Python 3.10+
- watchdog
- tkinter
- pyinstaller

## Observações

- O executável gerado é standalone (não requer Python instalado para uso final).
- Manual do usuário disponível em PDF para clientes finais.