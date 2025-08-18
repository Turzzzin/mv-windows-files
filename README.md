# Organizador de Arquivos para Windows

Este projeto contém um script Python que automatiza a organização de arquivos em computadores Windows. O programa busca arquivos de imagens, vídeos e planilhas Excel em todas as unidades do sistema, exceto pastas de sistema e outras pastas protegidas, e os move para pastas de destino específicas.

# Motivo do desenvolvimento
Meus pais têm um computador antigo que gostaria de transformar em um homelab. Eles concordaram, com a condição de salvar todas as fotos armazenadas nele para transferir ao computador mais recente. Eram cerca de 8 mil fotos espalhadas em diretórios diversos e bastante desorganizados. Por isso, decidi criar um script Python para automatizar essa varredura e organização dos arquivos.

## Funcionalidades

- **Busca automática:** Escaneia todas as unidades disponíveis no computador.
- **Filtragem inteligente:** Ignora pastas de sistema e arquivos já existentes nas pastas de destino.
- **Movimentação segura:** Move arquivos de imagens, vídeos e planilhas para pastas organizadas.
- **Registro de atividades:** Gera logs detalhados do processo, incluindo arquivos movidos, ignorados e erros encontrados.
- **Interface simples:** Solicita confirmação do usuário antes de iniciar o processo.

## Como usar

1. Certifique-se de estar em um ambiente Windows.
2. Execute o script `main.py` com Python 3.
3. Siga as instruções no terminal para iniciar a organização dos arquivos.

## Observações

- As pastas de destino são configuradas diretamente no código.
- O script pode exigir permissões administrativas para acessar todas as unidades e pastas.
- O processo pode ser interrompido a qualquer momento pressionando `Ctrl+C`.

---

**Atenção:** Antes de executar, revise as pastas de destino configuradas no código para garantir que atendem às suas necessidades
