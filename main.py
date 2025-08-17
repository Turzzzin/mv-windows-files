import os
import shutil
import logging
import time
from pathlib import Path
from typing import Set, List, Tuple
import sys

class FileOrganizer:
    """Classe principal para organização de arquivos."""
    
    def __init__(self):
        # Configuração das extensões e destinos
        self.image_extensions = {'.png', '.jpg', '.jpeg'}
        self.excel_extensions = {'.xlsx'}
        self.video_extensions = {'.mp4'ß}
        
        # Pastas de destino
        self.photos_dest = Path(r'C:\Compartilhamento\Fotos')
        self.files_dest = Path(r'C:\Compartilhamento\Arquivos')
        self.videos_dest = Path(r'C:\Compartilahmento\Videos')
        
        self.excluded_dirs = {
            'windows', 'program files', 'program files (x86)',
            'programdata', '$recycle.bin', 'system volume information',
            'recovery', 'boot', 'msocache', 'intel', 'perflogs',
            'windows.old', 'temp', 'tmp', 'appdata', 'arquivos de programas'
            'arquivos de programas x86'
        }
        
        # Contadores
        self.files_moved = 0
        self.files_skipped = 0
        self.errors_count = 0
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Configura o sistema de logging."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('file_organizer.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_destination_folders(self):
        """Cria as pastas de destino caso não existam."""
        try:
            self.photos_dest.mkdir(parents=True, exist_ok=True)
            self.files_dest.mkdir(parents=True, exist_ok=True)
            self.videos_dest.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Pastas de destino verificadas/criadas:")
            self.logger.info(f"  - Fotos: {self.photos_dest}")
            self.logger.info(f"  - Arquivos: {self.files_dest}")
            self.logger.info(f"  - Videos: {self.videos_dest}")
        except Exception as e:
            self.logger.error(f"Erro ao criar pastas de destino: {e}")
            raise
    
    def should_skip_directory(self, dir_path: Path) -> bool:
        """
        Verifica se um diretório deve ser ignorado.
        
        Args:
            dir_path: Caminho do diretório
            
        Returns:
            True se deve ser ignorado, False caso contrário
        """
        dir_name = dir_path.name.lower()
        
        # Ignorar pastas de sistema
        if dir_name in self.excluded_dirs:
            return True
        
        # Ignorar pastas que começam com $ ou .
        if dir_name.startswith(('$', '.')):
            return True
        
        # Ignorar pastas de destino para evitar loops
        if dir_path == self.photos_dest or dir_path == self.files_dest or dir_path == self.videos_dest:
            return True
        
        return False
    
    def get_destination_folder(self, file_path: Path) -> Path:
        """
        Determina a pasta de destino baseada na extensão do arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Pasta de destino ou None se não deve ser movido
        """
        extension = file_path.suffix.lower()
        
        if extension in self.image_extensions:
            return self.photos_dest
        elif extension in self.excel_extensions:
            return self.files_dest
        elif extension in self.video_extensions:
            return self.videos_dest
        
        return None
    
    def move_file_safely(self, source_path: Path, dest_folder: Path) -> bool:
        """
        Move um arquivo de forma segura para a pasta de destino.
        
        Args:
            source_path: Caminho do arquivo origem
            dest_folder: Pasta de destino
            
        Returns:
            True se movido com sucesso, False caso contrário
        """
        try:
            dest_path = dest_folder / source_path.name
            
            # Verificar se o arquivo já existe no destino
            if dest_path.exists():
                self.logger.warning(f"Arquivo já existe no destino, ignorando: {source_path.name}")
                self.files_skipped += 1
                return False
            
            # Mover o arquivo
            shutil.move(str(source_path), str(dest_path))
            self.logger.info(f"Movido: {source_path} -> {dest_path}")
            self.files_moved += 1
            return True
            
        except PermissionError:
            self.logger.error(f"Sem permissão para mover: {source_path}")
            self.errors_count += 1
            return False
        except FileNotFoundError:
            self.logger.error(f"Arquivo não encontrado: {source_path}")
            self.errors_count += 1
            return False
        except Exception as e:
            self.logger.error(f"Erro ao mover {source_path}: {e}")
            self.errors_count += 1
            return False
    
    def scan_directory(self, directory: Path) -> List[Path]:
        """
        Escaneia um diretório em busca de arquivos alvo.
        
        Args:
            directory: Diretório para escanear
            
        Returns:
            Lista de arquivos encontrados
        """
        found_files = []
        
        try:
            # Verificar se temos permissão para listar o diretório
            items = list(directory.iterdir())
        except PermissionError:
            self.logger.warning(f"Sem permissão para acessar: {directory}")
            return found_files
        except Exception as e:
            self.logger.warning(f"Erro ao acessar {directory}: {e}")
            return found_files
        
        for item in items:
            try:
                if item.is_file():
                    # Verificar se é um arquivo que queremos
                    if self.get_destination_folder(item):
                        found_files.append(item)
                
                elif item.is_dir() and not self.should_skip_directory(item):
                    # Recursão para subdiretórios
                    found_files.extend(self.scan_directory(item))
                    
            except (PermissionError, OSError) as e:
                self.logger.warning(f"Erro ao processar {item}: {e}")
                continue
        
        return found_files
    
    def get_drives(self) -> List[str]:
        """
        Obtém todas as unidades disponíveis no Windows.
        
        Returns:
            Lista de letras de unidades
        """
        drives = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive = f'{letter}:\\'
            if os.path.exists(drive):
                drives.append(drive)
        return drives
    
    def organize_files(self):
        """Executa o processo completo de organização de arquivos."""
        start_time = time.time()
        
        self.logger.info("="*60)
        self.logger.info("INICIANDO ORGANIZADOR DE ARQUIVOS")
        self.logger.info("="*60)
        
        try:
            # Criar pastas de destino
            self.create_destination_folders()
            
            # Obter todas as unidades
            drives = self.get_drives()
            self.logger.info(f"Unidades detectadas: {', '.join(drives)}")
            
            all_files = []
            
            # Escanear cada unidade
            for drive in drives:
                self.logger.info(f"Escaneando unidade: {drive}")
                drive_path = Path(drive)
                
                try:
                    # Escanear diretórios na raiz da unidade
                    for item in drive_path.iterdir():
                        if item.is_dir() and not self.should_skip_directory(item):
                            self.logger.info(f"Escaneando pasta: {item}")
                            files_found = self.scan_directory(item)
                            all_files.extend(files_found)
                            
                except PermissionError:
                    self.logger.warning(f"Sem permissão para acessar unidade: {drive}")
                    continue
                except Exception as e:
                    self.logger.error(f"Erro ao escanear unidade {drive}: {e}")
                    continue
            
            self.logger.info(f"Total de arquivos encontrados: {len(all_files)}")
            
            # Mover arquivos encontrados
            if all_files:
                self.logger.info("Iniciando movimentação de arquivos...")
                
                for file_path in all_files:
                    dest_folder = self.get_destination_folder(file_path)
                    if dest_folder:
                        self.move_file_safely(file_path, dest_folder)
            
            # Estatísticas finais
            end_time = time.time()
            duration = end_time - start_time
            
            self.logger.info("="*60)
            self.logger.info("RELATÓRIO FINAL")
            self.logger.info("="*60)
            self.logger.info(f"Tempo de execução: {duration:.2f} segundos")
            self.logger.info(f"Arquivos movidos: {self.files_moved}")
            self.logger.info(f"Arquivos ignorados (já existem): {self.files_skipped}")
            self.logger.info(f"Erros encontrados: {self.errors_count}")
            self.logger.info("Processo concluído!")
            
        except KeyboardInterrupt:
            self.logger.info("Processo interrompido pelo usuário.")
        except Exception as e:
            self.logger.error(f"Erro crítico: {e}")
            raise


def main():
    print("Organizador de Arquivos - Versão 1.0")
    print("Pressione Ctrl+C para interromper a qualquer momento.")
    print()
    
    try:
        # Solicitar confirmação do usuário
        resposta = input("Deseja iniciar a organização de arquivos? (s/N): ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            organizer = FileOrganizer()
            organizer.organize_files()
        else:
            print("Operação cancelada pelo usuário.")
            
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        logging.error(f"Erro inesperado na função main: {e}")


if __name__ == "__main__":
    main()