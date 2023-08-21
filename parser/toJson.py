def html_ticket_to_json (filepath: str) -> str:
    with open (filepath) as inputFile:
        html = inputFile.read().strip()
        questions = html.split("<ol class='hidden'>")[1].split("</ol>")[0].replace("</li>", "").split("<li>")[1:]
        for i, q in enumerate(questions):
            print (f"{i+1}. {q}")
        return ""

html_ticket_to_json ("tickets/1.html")
