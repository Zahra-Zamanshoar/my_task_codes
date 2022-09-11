for i in os.listdir():
    b = i.strip('.')
    try:
        with open(f'{i}/readme.md') as file:
            data = file.readlines
            for line in data:
                if '##' in line:
                    c = line.strip("#")

                    with open('untitled.txt', mode="r") as f:
                        first_line = f.readlines()
                        for k in first_line:
                            with open('untitled.txt', mode="w") as file_2:
                                file_2.write(print(
                                    f'##[{i}],https://github.com/pooya-mohammadi/today-i-learned/blob/main/{i}/Readme.'))
    #                             b = print(f'##[{i}],https://github.com/pooya-mohammadi/today-i-learned/blob/main/{i}/Readme.')
    #                     with open('untitled.txt',mode ="w" ) as file_2:
    #                         file_2.write(b)

    #                     print(f'https://github.com/pooya-mohammadi/today-i-learned/blob/main/toefl/writing.md/{i}/)
    #         for j in os.listdir(b):
    #             if j == 'Readme.md':
    #                 for line in open(j):
    #                     if '##' in line:
    #                         print(line.strip("#"))

    except:
        pass

#             with open(f'{i}/readme.md') as file:
#                 dataa = file.readlines
#                 for line in data:
#                      if '##' in line:
#                         print(line.strip("#"))
#         except:
#             break
