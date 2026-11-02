# SPDX-License-Identifier: Apache-2.0
"""Generate employee bulk upload templates for Excel and Google Sheets."""

from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

COLUMNS = [
    # (header, description, example1, example2, is_required)
    ("codigo_empleado", "Código único (opcional, se autogenera si está vacío)", "EMP-001", "EMP-002", False),
    ("primer_nombre", "Primer nombre (*)", "Juan", "María", True),
    ("segundo_nombre", "Segundo nombre", "Carlos", "Fernanda", False),
    ("primer_apellido", "Primer apellido (*)", "Pérez", "González", True),
    ("segundo_apellido", "Segundo apellido", "López", "Martínez", False),
    ("tipo_identificacion", "Tipo doc: id_card, passport, residence_card, other", "id_card", "id_card", False),
    ("identificacion_personal", "Número de cédula / DNI / pasaporte (*)", "001-010190-0001A", "001-020292-0002B", True),
    ("fecha_nacimiento", "Fecha nacimiento (YYYY-MM-DD)", "1990-01-15", "1992-05-20", False),
    ("genero", "Género: male, female, other", "male", "female", False),
    ("nacionalidad", "Nacionalidad", "Nicaragüense", "Costarricense", False),
    ("tipo_sangre", "Tipo de sangre: A+, A-, B+, B-, AB+, AB-, O+, O-", "O+", "A+", False),
    ("estado_civil", "Estado civil: single, married, divorced, widowed, common_law", "single", "married", False),
    ("codigo_empresa", "Código de la empresa (*)", "MHE", "MHE", True),
    ("fecha_alta", "Fecha de ingreso YYYY-MM-DD (*)", "2024-01-15", "2024-03-01", True),
    ("fecha_baja", "Fecha de baja YYYY-MM-DD (dejar vacío si está activo)", "", "", False),
    ("tipo_contrato", "Contrato: permanent, temporary, project_based, internship", "permanent", "permanent", False),
    ("cargo", "Puesto o cargo", "Analista de Nómina", "Contador General", False),
    ("area", "Área o departamento", "Recursos Humanos", "Finanzas", False),
    ("centro_costos", "Centro de costos", "CC-101", "CC-201", False),
    ("salario_base", "Salario base mensual numérico (*)", "1200.00", "1500.00", True),
    ("codigo_moneda", "Código de moneda (*): USD, NIO, CRC, MXN, etc.", "USD", "USD", True),
    ("activo", "Estado: SI o NO (default SI)", "SI", "SI", False),
    ("correo", "Correo electrónico", "juan.perez@empresa.com", "maria.gonzalez@empresa.com", False),
    ("telefono", "Teléfono de contacto", "+505 8888-9999", "+506 8765-4321", False),
    ("direccion", "Dirección de domicilio", "Calle Central #123", "Av. Principal #456", False),
    ("banco", "Nombre del banco", "Banco BAC", "Banco Lafise", False),
    ("numero_cuenta_bancaria", "Número de cuenta bancaria", "987654321012", "123456789098", False),
    ("id_seguridad_social", "Número de Seguro Social (INSS / CCSS / IMSS)", "INSS-7890123", "INSS-4567890", False),
    ("id_fiscal", "ID Fiscal (RUC / RFC / NIT)", "001-010190-0001A", "001-020292-0002B", False),
    ("salario_acumulado", "Salario acumulado fiscal previo al sistema (opcional)", "0.00", "0.00", False),
    ("impuesto_acumulado", "Impuesto acumulado fiscal previo al sistema (opcional)", "0.00", "0.00", False),
    ("ultimo_salario_1", "Penúltimo salario mensual (opcional)", "", "", False),
    ("ultimo_salario_2", "Antepenúltimo salario mensual (opcional)", "", "", False),
    ("ultimo_salario_3", "Tercer salario anterior (opcional)", "", "", False),
]


def generate_template(output_path: Path):
    wb = openpyxl.Workbook()

    # -------------------------------------------------------------
    # Sheet 1: Empleados (Data sheet)
    # -------------------------------------------------------------
    ws = wb.active
    ws.title = "Empleados"
    ws.views.sheetView[0].showGridLines = True

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    req_fill = PatternFill(start_color="0284C7", end_color="0284C7", fill_type="solid")  # GoERP Blue
    opt_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")  # Slate

    thin_border = Border(
        left=Side(style="thin", color="CCCCCC"),
        right=Side(style="thin", color="CCCCCC"),
        top=Side(style="thin", color="CCCCCC"),
        bottom=Side(style="thin", color="CCCCCC"),
    )

    # Row 1: Header names
    for col_idx, (name, _, _, _, is_req) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=name)
        cell.font = header_font
        cell.fill = req_fill if is_req else opt_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border

    # Row 2 & 3: Sample data
    sample_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    for row_num, ex_idx in [(2, 2), (3, 3)]:
        for col_idx, (_, _, ex1, ex2, _) in enumerate(COLUMNS, start=1):
            val = ex1 if ex_idx == 2 else ex2
            cell = ws.cell(row=row_num, column=col_idx, value=val)
            cell.font = Font(name="Calibri", size=10, italic=True)
            cell.fill = sample_fill
            cell.alignment = Alignment(horizontal="left", vertical="center")
            cell.border = thin_border

    # Adjust column widths
    for col_idx, (name, _, _, _, _) in enumerate(COLUMNS, start=1):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = max(len(name) + 5, 16)

    # -------------------------------------------------------------
    # Sheet 2: Catalogos_Referencia
    # -------------------------------------------------------------
    ws_cat = wb.create_sheet(title="Catalogos_Referencia")
    ws_cat.views.sheetView[0].showGridLines = True

    cat_header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    cat_fill = PatternFill(start_color="15803D", end_color="15803D", fill_type="solid")  # Emerald Green

    catalogs = [
        ("tipo_identificacion", [
            ("id_card", "Cédula de Identidad / DNI"),
            ("passport", "Pasaporte"),
            ("residence_card", "Carnet de Residente"),
            ("other", "Otro documento"),
        ]),
        ("genero", [
            ("male", "Masculino"),
            ("female", "Femenino"),
            ("other", "Otro"),
        ]),
        ("tipo_contrato", [
            ("permanent", "Contrato Indefinido"),
            ("temporary", "Contrato Temporal"),
            ("project_based", "Por Obra / Proyecto"),
            ("internship", "Prácticas / Pasantía"),
        ]),
        ("estado_civil", [
            ("single", "Soltero/a"),
            ("married", "Casado/a"),
            ("divorced", "Divorciado/a"),
            ("widowed", "Viudo/a"),
            ("common_law", "Unión Libre"),
        ]),
        ("tipo_sangre", [
            ("O+", "O Positivo"),
            ("O-", "O Negativo"),
            ("A+", "A Positivo"),
            ("A-", "A Negativo"),
            ("B+", "B Positivo"),
            ("B-", "B Negativo"),
            ("AB+", "AB Positivo"),
            ("AB-", "AB Negativo"),
        ]),
        ("codigo_moneda", [
            ("USD", "Dólar Estadounidense"),
            ("NIO", "Córdoba Nicaragüense"),
            ("CRC", "Colón Costarricense"),
            ("MXN", "Peso Mexicano"),
            ("GTQ", "Quetzal Guatemalteco"),
            ("HNL", "Lempira Hondureña"),
            ("PAB", "Balboa Panameña"),
            ("EUR", "Euro"),
        ]),
    ]

    col_pos = 1
    for cat_name, items in catalogs:
        # Header
        ws_cat.cell(row=1, column=col_pos, value=cat_name).fill = cat_fill
        ws_cat.cell(row=1, column=col_pos).font = cat_header_font
        ws_cat.cell(row=1, column=col_pos + 1, value="Descripción").fill = cat_fill
        ws_cat.cell(row=1, column=col_pos + 1).font = cat_header_font

        for row_idx, (code, desc) in enumerate(items, start=2):
            c1 = ws_cat.cell(row=row_idx, column=col_pos, value=code)
            c2 = ws_cat.cell(row=row_idx, column=col_pos + 1, value=desc)
            c1.border = thin_border
            c2.border = thin_border

        ws_cat.column_dimensions[get_column_letter(col_pos)].width = 20
        ws_cat.column_dimensions[get_column_letter(col_pos + 1)].width = 28
        col_pos += 3

    # -------------------------------------------------------------
    # Sheet 3: Instrucciones_GoogleSheets
    # -------------------------------------------------------------
    ws_inst = wb.create_sheet(title="Instrucciones")
    ws_inst.views.sheetView[0].showGridLines = True

    instructions = [
        ("INSTRUCCIONES PARA GOOGLE SHEETS Y EXCEL", True),
        ("", False),
        ("1. ¿Cómo usar esta plantilla en Google Sheets?", True),
        ("   a) Abre tu navegador y ve a https://sheets.new o Google Drive.", False),
        ("   b) En el menú principal de Google Sheets, selecciona: Archivo > Importar > Subir.", False),
        ("   c) Arrastra o selecciona este archivo (.xlsx).", False),
        ("   d) Selecciona 'Reemplazar hoja de cálculo' o 'Crear una nueva hoja de cálculo'.", False),
        ("", False),
        ("2. Llenado de información:", True),
        ("   - Los campos con fondo azul y (*) en la cabecera son OBLIGATORIOS.", False),
        ("   - Los campos con fondo gris son opcionales.", False),
        ("   - Para campos con opciones predefinidas (tipo_contrato, tipo_identificacion, genero, etc.), consulta la pestaña 'Catalogos_Referencia'.", False),
        ("   - Las fechas deben ingresarse en formato YYYY-MM-DD (ejemplo: 2024-01-15).", False),
        ("   - El salario_base debe ser un número decimal sin símbolos de moneda (ejemplo: 1200.00).", False),
        ("   - Elimina las filas de ejemplo (filas 2 y 3) antes de guardar tu archivo final.", False),
        ("", False),
        ("3. ¿Cómo exportar y subir a GoERP Payroll?", True),
        ("   a) En Google Sheets, haz clic en: Archivo > Descargar > Microsoft Excel (.xlsx) o Valores separados por comas (.csv).", False),
        ("   b) Entra a GoERP Payroll con tu usuario Administrador.", False),
        ("   c) Ve al menú Empleados > Carga Masiva (Solo Administrador).", False),
        ("   d) Selecciona tu archivo y pulsa 'Procesar Carga Masiva'.", False),
    ]

    for row_idx, (text, is_bold) in enumerate(instructions, start=1):
        cell = ws_inst.cell(row=row_idx, column=1, value=text)
        cell.font = Font(name="Calibri", size=11, bold=is_bold, color="0F172A" if is_bold else "334155")

    ws_inst.column_dimensions["A"].width = 110

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"Template successfully created at: {output_path}")


def generate_csv(output_path: Path):
    import csv

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name for name, _, _, _, _ in COLUMNS])
        writer.writerow([ex1 for _, _, ex1, _, _ in COLUMNS])
        writer.writerow([ex2 for _, _, _, ex2, _ in COLUMNS])
    print(f"CSV template successfully created at: {output_path}")


if __name__ == "__main__":
    xlsx_dest = Path("goerp_payroll/static/templates/plantilla_empleados_googlesheets.xlsx")
    csv_dest = Path("goerp_payroll/static/templates/plantilla_empleados_googlesheets.csv")
    generate_template(xlsx_dest)
    generate_csv(csv_dest)
