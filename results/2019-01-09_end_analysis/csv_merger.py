def merge_csv(annotated_file, file_to_merge, merged_file, delimiter = ','):
    annotated_dict = dict()
    for line_index, line in enumerate(open(annotated_file, 'r')):
        line = line.split(',')  # Deliminated by ,
        line = [i.replace('"', '') for i in line]  # Remove "
        if line_index == 0:
            annotated_dict['titles'] = line
        else:
            annotated_dict[line[0]] = line  # First is protein name, others properties

    file_handle = open(merged_file, 'w')
    for line_index, line in enumerate(open(file_to_merge, 'r')):
        line = line.split(delimiter)  # Deliminated by \t
        line = [i.replace('"', '') for i in line]  # Remove "
        if line_index == 3:
            line.extend(annotated_dict['titles'])
        elif line[0] in annotated_dict.keys():  # The first 4 lines will not have it
            line.extend(annotated_dict[line[0]])
            
        line = [i.replace('\n', '') for i in line]  # Remove \n (some rows have hidden \n)
        line = ','.join(line)
        line += '\n'  # Add new line
        file_handle.write(line)
    file_handle.close()
    return 0
    
