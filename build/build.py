import glob
import tempfile
import zipfile
import base64
import os
import lxml.etree as xml
import ast
import astor
import pathlib

SOURCE_DIR = 'src'
OUTPUT_DIR = 'dist'
XML_TEMPLATE_PATH = 'build/template.xml'

# Получение base64 от zip-архива всех файлов проекта
target_files = glob.glob('**/*.py', root_dir=SOURCE_DIR, recursive=True)

tempfile = tempfile.NamedTemporaryFile(delete=False)

with zipfile.ZipFile(tempfile.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    for file in target_files:
        zip_file.write(os.path.join(SOURCE_DIR, file), file)

with open(tempfile.name, 'rb') as f:
    zip_base64 = base64.b64encode(f.read()).decode('ascii')

tempfile.close()
os.unlink(tempfile.name)


# Загрузка xml-шаблона вопроса и создание записи об zip-архиве
with open(XML_TEMPLATE_PATH, 'r', encoding='utf-8') as xml_file:
    xml_parser = xml.XMLParser(strip_cdata=False)
    xml_template = xml.parse(xml_file, xml_parser)

xml_template.xpath('//file')[0].text = zip_base64


# Класс извлечения узла аргументов из конструктора класса
class InitArgumentsExtractor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        if node.name != '__init__':
            return

        self.arguments_node = node.args

    def extract(self, node: ast.AST) -> ast.arguments | None:
        self.arguments_node = None
        self.visit(node)
        return self.arguments_node

# Класс извлечения названия класса и узла аргументов конструктора класса для потомков QuestionBase
class QuestionDataExtractor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        if self.class_name or not any(base.id == 'QuestionBase' for base in node.bases):
            return

        self.class_name = node.name

        arguments_extractor = InitArgumentsExtractor()
        self.arguments_node = arguments_extractor.extract(node)

    def extract(self, node: ast.AST) -> tuple[str | None, ast.arguments | None]:
        self.class_name = None
        self.arguments_node = None
        self.visit(node)
        return self.class_name, self.arguments_node


# Шаблоны кода, внедряемого в xml-файл
parameters_code_template = r'''import sys
sys.path.insert(0, 'bundle.zip')
from prog_questions import {class_name}

question = {constructor_code}
print(question.getTemplateParameters())
'''

code_template = r'''import sys
sys.path.insert(0, 'bundle.zip')
from prog_questions import {class_name}

question = {class_name}.initWithParameters("""{{{{ PARAMETERS | e('py') }}}}""")
print(question.test("""{{{{ STUDENT_ANSWER | e('py') }}}}"""))
'''

# Проверка для всех файлов проекта
for file in target_files:
    # Получение информации о классе вопроса из файла
    with open(os.path.join(SOURCE_DIR, file), 'r', encoding='utf-8') as code_file:
        question_class, question_arguments = QuestionDataExtractor().extract(ast.parse(code_file.read()))

    # Если в файле нет класса вопроса - пропускаем
    if question_class is None:
        continue

    # Конвертация узла arguments в массив keyword
    if question_arguments is not None:
        keywords = [ast.keyword(arg=kw_name, value=kw_value) for kw_name, kw_value in zip(question_arguments.kwonlyargs, question_arguments.kw_defaults) if kw_name.arg != 'seed']
    else:
        keywords = []

    # Создание куска кода с вызовом initTemplate со стандартными параметрами (полученными из кода конструктора)
    call_node = ast.Call(func=ast.Attribute(value=ast.Name(id=question_class), attr='initTemplate'), args=[], keywords=keywords)
    constructor_code = astor.to_source(call_node).rstrip()

    # Подстановка в шаблоны кода
    parameters_code = parameters_code_template.format(class_name=question_class, constructor_code=constructor_code).lstrip()
    code = code_template.format(class_name=question_class).lstrip()

    # Модификация xml-шаблона
    xml_template.xpath('//question/name/text')[0].text = question_class
    xml_template.xpath('//templateparams')[0].text = xml.CDATA(parameters_code)
    xml_template.xpath('//template')[0].text = xml.CDATA(code)

    # Создание директорий для выходного файла, если их нет
    xml_filename = os.path.join(OUTPUT_DIR, f'{question_class}.xml')
    pathlib.Path(os.path.dirname(xml_filename)).mkdir(parents=True, exist_ok=True)

    # Запись в файл и вывод в консоль
    xml_template.write(xml_filename, xml_declaration=True, encoding='utf-8')
    print(xml_filename)
