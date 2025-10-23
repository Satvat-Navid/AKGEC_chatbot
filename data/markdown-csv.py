def filterLinks(md, csv, fileW, pattern):
    buffer = []
    data = []

    try:
        with open(md, "r", encoding="utf-8") as fmd:
            with open(csv, "r", encoding="utf-8") as fcsv:
                with open(fileW, "w", encoding="utf-8") as fw:
                    while True:
                        char = fmd.read(1)

                        if not char:
                            break

                        buffer.append(char)

                        if len(buffer) > len(pattern):
                            temp = buffer.pop(0)
                            data.append(temp)

                        if pattern == "".join(buffer):
                            buffer.clear()
                            link = fcsv.readline().strip()
                            newline = "\n"
                            nonewline = "\\n"
                            data = [nonewline if value == newline else value for value in data]
                            newline = '"'
                            nonewline = '""'
                            data = [nonewline if value == newline else value for value in data]
                            content = "".join(data)
                            fw.write(f'{link}, "{content}"\n')
                            data.clear()

    except Exception as e:
        print(f"error -------->> {e}")

filterLinks("fit_data.txt", "akg_links.txt", "akgec.csv", "\n\n---------------------------------------------------------------------------\n\n")
