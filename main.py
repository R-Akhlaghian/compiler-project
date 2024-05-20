from Scanner.scanner import Scanner

scanner = Scanner()
while True:
    next_token = scanner.get_next_token()
    print(scanner.line_number, next_token)
    if next_token is None:
        break
