## ver.py - Шифр Вермана
Шифрует сообщение. `ver.py --help` для справки.
Использование:
```bash 
$ ver.py encrypt -i data [-o data.dec] [-k data.dec.key]
```
Шифрование файла `data`. Ключ `data.dec.key` сохраняется в той же директории, выходной файл - `data.dec`

```bash
$ ver.py decrypt -i data.dec [-k data.dec.key] [-o data]
```
Расшифровка файла `data.dec` ключом `data.dec.key` и вывод в файл `data`.

```bash
$ ver.py encrypt foo/ -k keys/ -o outs/
```
Шифровка всех файлов в папке `foo`. Ключи сохраняются в `keys` в формате `file.dec.key`, а вывод в `out/file.dec`.

requirements: `click`.

> Windows and Linux 
