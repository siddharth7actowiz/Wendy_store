from lxml import html

# Sample HTML with various link types
html_data = """
<div>
    <a href="https://example.com">Home Page</a>
    <img src="/assets/logo.png" alt="Logo">
    <link rel="stylesheet" href="styles.css">
    <script src="app.js"></script>
    <form action="/login" method="post">
        <input type="submit" value="Log In">
    </form>
</div>
"""

# 1. Parse the string using html.fromstring()
tree = html.fromstring(html_data)

# 2. Iterate through all links
print("--- Extracted Links ---")
for element, attribute, link, pos in tree.iterlinks():
    # element: the HTML object (e.g., <Element a>)
    # attribute: the specific attribute containing the link (e.g., 'href' or 'src')
    # link: the raw URL/path string
    print(f"Found <{element.tag}> link: {link} (in attribute: {attribute})")

# 3. Pro tip: Make all relative links absolute in one go
    
    print(link)
    
