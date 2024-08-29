import os, subprocess, time


class Interface:
    def __init__(self):
        self.columns = os.get_terminal_size().columns
        self.lines = os.get_terminal_size().lines
    
    def clearScreenShowTitle(self, character, text):
        os.system('clear')
        print(character*self.columns + "\n" + f"{character*2}{text: ^{self.columns-4}}{character*2}" + "\n" + character*self.columns)
    
    def clearScreen(self):
        os.system('clear')


isoFiles = []

def listar_pastas(diretorio, fileformat):
    try:
        itens = os.listdir(diretorio)
        for item in itens:
            caminho_completo = os.path.join(diretorio, item)
            if os.path.isdir(caminho_completo):
                listar_pastas(caminho_completo, fileformat)
            else:
                extensao = os.path.splitext(caminho_completo)[-1][1:]

                if extensao == fileformat:
                    isoFiles.append(caminho_completo)
    except Exception:
        pass

interface = Interface()




interface.clearScreenShowTitle('#', "EASY DD BURNER")
time.sleep(0.5)
print('\nShowing your iso files:\n')

listar_pastas(f'/home/{os.getlogin()}', 'iso')


for x in range(len(isoFiles)):
    print(f'[{x+1}]  {isoFiles[x]}')


file = isoFiles[int(input('\nSelect the iso file to use: '))-1]

print(f'\n{file} selected')
time.sleep(2)




interface.clearScreenShowTitle('#', "EASY DD BURNER")
print('\nShowing your disks:\n')


getDisks = "lsblk -dn -o NAME,SIZE | awk '{print $1 \":\" $2}' | tr '\\n' ' ' | sed 's/ $/\\n/'"
result = subprocess.run(getDisks, shell=True, capture_output=True, text=True).stdout.strip().split()
listOfDisks = [(f'/dev/{disk.split(':')[0]}', disk.split(':')[1]) for disk in result]


for x in range(len(listOfDisks)):
    print(f'[{x+1}]   Disk: {listOfDisks[x][0]:<15} Size: {listOfDisks[x][1]:>7}')
   
disk = listOfDisks[int(input('\nSelect the disk to burn: '))-1][0]

print(f'\n{disk} selected')
time.sleep(2)



interface.clearScreenShowTitle('#', "EASY DD BURNER")
confirmation = input(('\nThe selected disk will be formated. Proceed?\n(y,n) > ')).lower()

if confirmation == 'y':
    print()
    os.system(f'sudo umount {disk}')
    os.system(f'sudo mkfs.ext4 {disk}')

else:
    print('\nOperation canceled.')
    exit()



interface.clearScreenShowTitle('#', "EASY DD BURNER")
print('\nBurning process started.\n')
os.system(f'sudo dd if={file} of={disk} bs=4M')

interface.clearScreenShowTitle('#', "EASY DD BURNER")
print('\nDone!')

