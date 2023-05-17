import os

## setup Libri-Light
import os

for k in os.listdir('librispeech_finetuning/9h/clean'):
    for j in os.listdir('librispeech_finetuning/9h/'+'clean'):
        for z in os.listdir('librispeech_finetuning/9h/clean/'+j):
            for i in os.listdir('librispeech_finetuning/9h/clean/'+j+'/'+z):
                os.rename('librispeech_finetuning/9h/clean/'+j+'/'+z+'/'+i, f'vall-e/data/libri/{i}')
        
    break
lst = []
for i in os.listdir('vall-e/data/libri'):
    try:
        if 'trans' in i:
            with open(f'vall-e/data/libri/{i}') as text_file:
                for row in text_file:
                    z = row.split('-')
                    name = z[0]+'-'+z[1]+ '-' + z[2].split(' ')[0]
                    text = " ".join(z[2].split(' ')[1:])
                    # print(name, text)
                    lst.append([name, text])

                        
    except:
        None      

for i in lst:
    try:
        with open('vall-e/data/libri/'+i[0]+'.txt', 'x') as file:
            # print(i[1])
            file.write(i[1])
    except:
        with open('vall-e/data/libri/'+i[0]+'.txt', 'w+') as file:
            # print(i[1])
            file.write(i[1])

for i in sorted(os.listdir('vall-e/data/libri')):
    if i.split('.')[1] == 'txt':
        # print(i)
        print('.'.join([i.split('.')[0],'normalized',i.split('.')[1]]))
        os.rename('vall-e/data/libri/'+i, 'vall-e/data/libri/'+'.'.join([i.split('.')[0],'normalized',i.split('.')[1]]))