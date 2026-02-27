from lxml import etree

def parse_xaml(content: bytes):
    """
    Parses UiPath XAML and extracts DisplayName activities
    """

    try:
        tree = etree.fromstring(content)
    except Exception as e:
        raise ValueError(f"Invalid XAML/XML: {str(e)}")

    activities = []

    for node in tree.xpath("//*[@DisplayName]"):
        activities.append(node.attrib.get("DisplayName"))

    return tree, activities