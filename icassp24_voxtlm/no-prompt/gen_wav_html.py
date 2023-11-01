import os

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Demo non-prompted speech generation</title>
</head>
<body>
    <h1>Audio Files</h1>
    <table>
        <thead>
            <tr>
                <th>Audio File</th>
                <th>Text</th>
                {subfolder_headers}
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>
"""

table_row_template = """
<tr>
    <td>{audio_name}</td>
    <td>{text_content}</td>
    {audio_cells}
</tr>
"""

audio_cell_template = """
<td>
    <audio controls>
        <source src="{audio_path}" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
</td>
"""

def read_text_file(text_file_path):
    try:
        text_dict={}
        with open(text_file_path, 'r') as f:
            #return f.read().splitlines()
        
            for line in f:
                id=line.strip().split()[0]
                text=" ".join(line.strip().split()[1:])
                text_dict[id]=text
            return text_dict
    except:
        return {}

def read_audio_file_names(subfolder_path):
    audio_files = [f for f in os.listdir(subfolder_path) if f.endswith('.mp3') or f.endswith('.wav')]
    audio_files_2 = [f for f in audio_files if f.startswith('1089')]
    return audio_files_2

def generate_html(root_folder, text_file_path):
    #subfolders = [name for name in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, name))]
    #subfolders.sort(reverse=True)
    #print(subfolders, subfolders.sort(reverse=True))
    #print(subfolders)
    subfolders = ["Ground-Truth", "VoxtLM-3M-50", "VoxtLM200_LS+M", "VoxtLM-Bal-1000"]
    subfolder_headers = "\n".join(f"<th>{subfolder}</th>" for subfolder in subfolders)
    
    text_content_lines = read_text_file(text_file_path)
    audio_file_names = read_audio_file_names(os.path.join(root_folder, subfolders[0]))
    
    table_rows = []

    # TODO: how many files
    count=20
    for audio_name in audio_file_names:
        count-=1

        if count==0:
            break
        audio_name_without_extension = os.path.splitext(audio_name)[0]
        if audio_name_without_extension in text_content_lines:
            text_content=text_content_lines[audio_name_without_extension]
        else:
            text_content=""
        audio_cells = [audio_cell_template.format(audio_path=os.path.join(root_folder, subfolder, audio_name))
                       if audio_name in os.listdir(os.path.join(root_folder, subfolder))
                       else ""
                       for subfolder in subfolders]
        table_row_html = table_row_template.format(audio_name=audio_name_without_extension, text_content=text_content, audio_cells="\n".join(audio_cells))
        table_rows.append(table_row_html)
    
    table_rows_html = "\n".join(table_rows)
    final_html = html_content.format(subfolder_headers=subfolder_headers, table_rows=table_rows_html)
    
    return final_html

root_folder = "."      # Replace with your root folder path
text_file_path = "textfile_norm.txt"  # Replace with the path to your text file
output_file = "demo.html"        # Name of the HTML output file

html_content = generate_html(root_folder, text_file_path)

with open(output_file, 'w') as f:
    f.write(html_content)

print(f"HTML file '{output_file}' generated.")
