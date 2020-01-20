import os

CHARACTERISTICS = [ 'BR', 'AG', 'INT', 'CUN', 'WILL', 'PR']

def humanize(s):
    return s.replace("_", " ").title()

def batch_list(list, batch_size):
    return [ list[i:i + batch_size] for i in range(0, len(list), batch_size) ]

def load_data(yamlfile, filter=None):
    """Read YAML file and return list containing the data"""
    import yaml
    with open(yamlfile) as file:
        items = yaml.safe_load(file)
        if filter != None:
            items = [ item for item in yaml.safe_load(file) if filter(item) ]
        return items

def resource_path(filename):
    """Returns the full pathname of the specified file in the resource directory"""
    directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources'))
    return os.path.join(directory, filename)

def data_filename(args, default_filename='test.yaml', directories=[]):
    directories.append(os.path.dirname(__file__))
    directories.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data')))

    # if os.path.isfile(filename):
    #     return filename
    filename = args[1] if len(args) > 1 else default_filename
    if not filename.endswith(('.yaml', '.YAML')):
        filename = filename + '.yaml'
    for directory in directories:
        try_filename = os.path.join(directory, filename)
        if os.path.isfile(try_filename):
            return try_filename
    raise FileNotFoundError("data file not found:%s in %s" % (filename, str(directories)))

def register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("Arial", 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont("genesys", 'C:\\Users\\Semprebon\\Appdata\\local\\microsoft\\windows\\fonts\\GenesysGlyphsAndDice-2.2.ttf'))
