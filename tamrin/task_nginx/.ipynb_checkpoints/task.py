with open('docker-compose.yml', encoding="utf-8") as docer_file:
    deta = docer_file.readlines()
    for line in deta:
        count = 0
        # count space
        for item in line[:5]:
            if item == ' ':
                count += 1
            else:
                break
        #         if 'END_POINT' in line.strip().strip(':').strip('-'):
        #             End_point = line.strip('- END_POINT=/')
        # Find based on distance
        if count == 2:
            #             if 'END_POINT' in line.strip().strip(':').strip('-'):
            #                 print(line)
            line_ = line.strip().strip(':').strip('# ')
            # Does not consider the items listed
            if 'END_POINT' == line_:
                print(line_)


