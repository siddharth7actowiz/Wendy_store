
def read_html(Path):
    try:
        with open(Path,"r",encoding="utf-8") as f:
            data=f.read()
            return data
    except Exception as e:
        print("Error",read_html.__name__,e)    