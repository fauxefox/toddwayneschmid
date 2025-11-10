from sys import argv
import time
from os import listdir, fsdecode

# Graphics
from colorama import Fore

def create_page(header, footer, body, filename, course_folder = None, next_page_name = None, prev_page_name = None) :
    file = open(filename, "w")

    current_date = time.strftime("%Y-%m-%d", time.localtime())
    
    filename:str
    is_notes_page = "notes" in filename

    if is_notes_page :
        backforwardlinks = "<div style=\"border: none; margin-bottom: -20px; padding: 0px; text-align: center;\">"

        if prev_page_name and ("notes" in prev_page_name) :
            cleaned_up_name = prev_page_name.replace("_", " ").replace(".html", "")[11:].title()
            prev_page_link = f"<a href=\"../compiled/{course_folder}_{prev_page_name}\"><span class=\"link\"> &larr; {cleaned_up_name}</span></a>"
            # prev_page_link = f"<a href=\"../compiled/{course_folder}_{prev_page_name}\"><span class=\"link\"> \(\looparrowleft\) {cleaned_up_name}</span></a>"
        else : 
            prev_page_link = None

        if next_page_name and ("notes" in next_page_name) :
            cleaned_up_name = next_page_name.replace("_", " ").replace(".html", "")[11:].title()
            next_page_link = f"<a href=\"../compiled/{course_folder}_{next_page_name}\"><span class=\"link\">{cleaned_up_name} &rarr;</span></a>"
            # next_page_link = f"<a href=\"../compiled/{course_folder}_{next_page_name}\"><span class=\"link\">{cleaned_up_name} \(\leadsto\)</span></a>"
        else : 
            next_page_link = None

        backforwardblock = backforwardlinks \
            + (prev_page_link if prev_page_link else "") \
            + (next_page_link if next_page_link else "") \
            + "</div>"
    else : 
        backforwardblock = ""

    page_string = f"<!-- THIS IS A COMPILED FILE \n Compiled on {current_date} -->" \
        + "\n"*100 \
        + header \
        + backforwardblock\
        + body \
        + backforwardblock\
        + footer\
        # + backforwardblock\
    
    file.write(page_string)
    file.close()

if __name__ == "__main__" :
    # Collect course name
    try :
        course_folder = argv[1]
    except :
        course_folder = input("Enter course folder name: ")

    print("Building pages for", course_folder)

    # Collect html header
    print("Collecting html header file.")
    header_file = open(f'{course_folder}/header.html')
    header = header_file.read()
    header_file.close()

    # Collect html footer
    print("Collecting html footer file.")
    footer_file = open(f'{course_folder}/footer.html')
    footer = footer_file.read()
    footer_file.close()

    # Get pages directory
    pages_folder = fsdecode(f'{course_folder}/pageconstruction/')
    print("Searching pages folder at", pages_folder)

    # Create pages and spit them into local directory
    print("Creating pages:")
    page_list = listdir(pages_folder)

    page_name_list = sorted([fsdecode(page_file).lower() for page_file in page_list])


    for page_index in range(len(page_name_list)) :

        page_name = page_name_list[page_index]
        
        print("\t- Creating", Fore.BLUE, page_name)

        file = open(f"{course_folder}/pageconstruction/{page_name}", "r")
        page = file.read()
        file.close()

        out_file = f"{course_folder}/compiled/{course_folder}_{page_name}"

        if page_index > 0 :
            prev_page_name = page_name_list[page_index - 1]
        else :
            prev_page_name = None
        
        if page_index < len(page_name_list) - 1 :
            next_page_name = page_name_list[page_index + 1]
        else :
            next_page_name = None

        create_page(header, footer, page, out_file, course_folder = course_folder, prev_page_name = prev_page_name, next_page_name = next_page_name)
        
        print(Fore.RESET, "\t\twritten to", Fore.RED, out_file, Fore.RESET)


    