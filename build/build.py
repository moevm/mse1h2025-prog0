from pathlib import Path
import shutil
import tempfile
import zipfile
import base64
import os
import lxml.etree as xml
import ast
import astor


ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = ROOT / 'src'
OUTPUT_PATH = ROOT / 'dist'
XML_TEMPLATE_PATH = ROOT / 'build' / 'template.xml'


if OUTPUT_PATH.exists():
    for file in OUTPUT_PATH.iterdir():
        if file.is_dir():
            shutil.rmtree(file)
        else:
            file.unlink()
else:
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


# Получение base64 от zip-архива всех файлов проекта
sources = [*SOURCE_PATH.glob('**/*.py')]

bundle_tempfile = tempfile.NamedTemporaryFile(delete=False)

with zipfile.ZipFile(bundle_tempfile.name, 'w', zipfile.ZIP_DEFLATED) as bundle_file:
    for file in sources:
        bundle_file.write(file, file.relative_to(SOURCE_PATH))

with open(bundle_tempfile.name, 'rb') as f:
    bundle_base64 = base64.b64encode(f.read()).decode('ascii')

bundle_tempfile.close()
os.unlink(bundle_tempfile.name)


# Загрузка xml-шаблона вопроса и создание записи об zip-архиве
with XML_TEMPLATE_PATH.open('r', encoding='utf-8') as xml_file:
    xml_parser = xml.XMLParser(strip_cdata=False)
    xml_template = xml.parse(xml_file, xml_parser)

xml_template.xpath('//file')[0].text = bundle_base64


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
for file in sources:
    # Получение информации о классе вопроса из файла
    question_class, question_arguments = QuestionDataExtractor().extract(ast.parse(file.read_text(encoding='utf-8')))

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

    # Запись в файл и вывод в консоль
    xml_output_path = OUTPUT_PATH / f'{question_class}.xml'
    xml_template.write(xml_output_path, xml_declaration=True, encoding='utf-8')
    print(xml_output_path)
