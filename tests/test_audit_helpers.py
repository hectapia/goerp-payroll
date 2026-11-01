from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from goerp_payroll import audit_helpers
from goerp_payroll.enums import EstadoAprobacion, NominaEstado, TipoUsuario


class DummyActivo:
    def is_(self, _value):
        return "activo_expr"


class DummyQuery:
    def __init__(self, result):
        self.result = result
        self.filters = None

    def join(self, *_args, **_kwargs):
        return self

    def filter(self, *args):
        self.filters = args
        return self

    def all(self):
        return self.result


class DummySession:
    def __init__(self, query_results=None):
        self.added = []
        self._query_results = list(query_results or [])

    def add(self, item):
        self.added.append(item)

    def query(self, _model):
        return DummyQuery(self._query_results.pop(0))


@dataclass
class BaseConcept:
    id: str = "id-1"
    nombre: str = "Concepto"
    codigo: str = "C-001"
    estado_aprobacion: str = EstadoAprobacion.BORRADOR
    aprobado_por: str | None = None
    aprobado_en: object | None = None
    creado_por_plugin: bool = False


class DummyPercepcion(BaseConcept):
    activo = DummyActivo()


class DummyDeduccion(BaseConcept):
    activo = DummyActivo()


class DummyPrestacion(BaseConcept):
    activo = DummyActivo()


@dataclass
class DummyPlanilla:
    id: str = "pl-1"
    nombre: str = "Planilla 1"
    estado_aprobacion: str = EstadoAprobacion.BORRADOR
    aprobado_por: str | None = None
    aprobado_en: object | None = None
    creado_por_plugin: bool = False


@dataclass
class DummyNomina:
    id: str = "nom-1"
    estado: str = NominaEstado.GENERADO
    aprobado_por: str | None = None
    aprobado_en: object | None = None
    aplicado_por: str | None = None
    aplicado_en: object | None = None
    anulado_por: str | None = None
    anulado_en: object | None = None
    razon_anulacion: str | None = None
    periodo_inicio: str = "2025-01-01"
    periodo_fin: str = "2025-01-31"


@dataclass
class DummyRegla:
    id: str = "reg-1"
    nombre: str = "Regla"
    codigo: str = "RC-001"
    version: int = 1
    estado_aprobacion: str = EstadoAprobacion.BORRADOR
    aprobado_por: str | None = None
    aprobado_en: object | None = None
    creado_por_plugin: bool = False
    activo = DummyActivo()


@pytest.fixture
def patched_models(monkeypatch):
    monkeypatch.setattr(audit_helpers, "Percepcion", DummyPercepcion)
    monkeypatch.setattr(audit_helpers, "Deduccion", DummyDeduccion)
    monkeypatch.setattr(audit_helpers, "Prestacion", DummyPrestacion)


@pytest.fixture
def patched_logs_db(monkeypatch):
    session = DummySession()
    monkeypatch.setattr(audit_helpers, "db", SimpleNamespace(session=session))
    monkeypatch.setattr(audit_helpers, "utc_now", lambda: "NOW")

    monkeypatch.setattr(audit_helpers, "ConceptoAuditLog", lambda **kw: SimpleNamespace(**kw))
    monkeypatch.setattr(audit_helpers, "PlanillaAuditLog", lambda **kw: SimpleNamespace(**kw))
    monkeypatch.setattr(audit_helpers, "NominaAuditLog", lambda **kw: SimpleNamespace(**kw))
    monkeypatch.setattr(audit_helpers, "ReglaCalculoAuditLog", lambda **kw: SimpleNamespace(**kw))
    return session


def test_puede_aprobar_concepto_roles():
    assert audit_helpers.puede_aprobar_concepto(TipoUsuario.ADMIN)
    assert audit_helpers.puede_aprobar_concepto(TipoUsuario.HHRR)
    assert not audit_helpers.puede_aprobar_concepto(TipoUsuario.AUDIT)


def test_crear_log_auditoria_para_cada_tipo_y_error(patched_models, patched_logs_db):
    per = DummyPercepcion(id="p1")
    ded = DummyDeduccion(id="d1")
    pre = DummyPrestacion(id="b1")

    per_log = audit_helpers.crear_log_auditoria(per, "created", "u")
    ded_log = audit_helpers.crear_log_auditoria(ded, "created", "u")
    pre_log = audit_helpers.crear_log_auditoria(pre, "created", "u", cambios=None)

    assert per_log.tipo_concepto == "percepcion"
    assert per_log.percepcion_id == "p1"
    assert ded_log.tipo_concepto == "deduction"
    assert ded_log.deduccion_id == "d1"
    assert pre_log.tipo_concepto == "benefit"
    assert pre_log.prestacion_id == "b1"
    assert pre_log.cambios == {}
    assert len(patched_logs_db.added) == 3

    with pytest.raises(ValueError):
        audit_helpers.crear_log_auditoria(SimpleNamespace(id="x"), "x", "u")


def test_generar_descripcion_cambios_cubre_variantes():
    assert audit_helpers.generar_descripcion_cambios({}) == ""
    cambios = {
        "campo_nuevo": {"old": "", "new": "A"},
        "campo_eliminado": {"old": "B", "new": None},
        "campo_cambio": {"old": "X", "new": "Y"},
    }
    texto = audit_helpers.generar_descripcion_cambios(cambios)
    assert "Campo Nuevo establecido a A" in texto
    assert "Campo Eliminado eliminado (era B)" in texto
    assert "Campo Cambio cambió de X a Y" in texto


def test_aprobar_y_rechazar_concepto(monkeypatch, patched_models):
    calls = []
    monkeypatch.setattr(audit_helpers, "crear_log_auditoria", lambda **kw: calls.append(kw))
    monkeypatch.setattr(audit_helpers, "utc_now", lambda: "NOW")

    concepto = DummyPercepcion(nombre="Ingreso", codigo="I01")
    assert audit_helpers.aprobar_concepto(concepto, "admin")
    assert concepto.estado_aprobacion == EstadoAprobacion.APROBADO
    assert concepto.aprobado_por == "admin"
    assert concepto.aprobado_en == "NOW"
    assert calls[-1]["accion"] == "approved"

    assert not audit_helpers.aprobar_concepto(concepto, "admin")

    assert audit_helpers.rechazar_concepto(concepto, "hr", "dato inválido")
    assert concepto.estado_aprobacion == EstadoAprobacion.BORRADOR
    assert concepto.aprobado_por is None
    assert "Razón: dato inválido" in calls[-1]["descripcion"]

    assert audit_helpers.rechazar_concepto(concepto, "hr")
    assert "Razón" not in calls[-1]["descripcion"]


def test_marcar_como_borrador_si_editado(monkeypatch, patched_models):
    calls = []
    monkeypatch.setattr(audit_helpers, "crear_log_auditoria", lambda **kw: calls.append(kw))
    monkeypatch.setattr(audit_helpers, "generar_descripcion_cambios", lambda _c: "desc")

    concepto_plugin = DummyPercepcion(creado_por_plugin=True, estado_aprobacion=EstadoAprobacion.APROBADO)
    audit_helpers.marcar_como_borrador_si_editado(concepto_plugin, "u", {"nombre": {"old": "A", "new": "B"}})
    assert calls == []

    concepto_borrador = DummyPercepcion(estado_aprobacion=EstadoAprobacion.BORRADOR)
    audit_helpers.marcar_como_borrador_si_editado(concepto_borrador, "u", {})
    assert calls == []

    concepto = DummyPercepcion(estado_aprobacion=EstadoAprobacion.APROBADO)
    audit_helpers.marcar_como_borrador_si_editado(concepto, "u", {"nombre": {"old": "A", "new": "B"}})
    assert concepto.estado_aprobacion == EstadoAprobacion.BORRADOR
    assert "Estado cambiado a borrador." in calls[-1]["descripcion"]


def test_detectar_cambios_campos_importantes_y_equivalencias():
    original = {
        "nombre": "A",
        "descripcion": None,
        "codigo": "X",
        "monto_default": 10,
        "tipo": "t1",
    }
    nuevo = {
        "nombre": "B",
        "descripcion": "",
        "codigo": "X",
        "monto_default": 11,
        "tipo": "t2",
        "extra": "ignorado",
    }
    cambios = audit_helpers.detectar_cambios(original, nuevo)
    assert cambios == {
        "nombre": {"old": "A", "new": "B"},
        "monto_default": {"old": 10, "new": 11},
        "tipo": {"old": "t1", "new": "t2"},
    }


def test_obtener_conceptos_y_tiene_conceptos(monkeypatch, patched_models):
    session = DummySession(
        query_results=[
            [SimpleNamespace(nombre="Ingreso")],
            [SimpleNamespace(nombre="Renta")],
            [],
        ]
    )
    monkeypatch.setattr(audit_helpers, "db", SimpleNamespace(session=session))
    monkeypatch.setattr(audit_helpers, "true", lambda: "TRUE")

    class PI:
        planilla_id = "planilla_id_expr"

    class PD:
        planilla_id = "planilla_id_expr"

    class PP:
        planilla_id = "planilla_id_expr"

    import goerp_payroll.model as model

    monkeypatch.setattr(model, "PlanillaIngreso", PI)
    monkeypatch.setattr(model, "PlanillaDeduccion", PD)
    monkeypatch.setattr(model, "PlanillaPrestacion", PP)

    conceptos = audit_helpers.obtener_conceptos_en_borrador("pl-1")
    assert len(conceptos["percepciones"]) == 1
    assert len(conceptos["deducciones"]) == 1
    assert conceptos["prestaciones"] == []

    monkeypatch.setattr(
        audit_helpers,
        "obtener_conceptos_en_borrador",
        lambda _id: {"percepciones": [1], "deducciones": [], "prestaciones": []},
    )
    assert audit_helpers.tiene_conceptos_en_borrador("pl-1")

    monkeypatch.setattr(
        audit_helpers,
        "obtener_conceptos_en_borrador",
        lambda _id: {"percepciones": [], "deducciones": [], "prestaciones": []},
    )
    assert not audit_helpers.tiene_conceptos_en_borrador("pl-1")


def test_planilla_flujos(monkeypatch, patched_logs_db):
    original_creator = audit_helpers.crear_log_auditoria_planilla
    calls = []
    monkeypatch.setattr(audit_helpers, "crear_log_auditoria_planilla", lambda **kw: calls.append(kw))
    monkeypatch.setattr(audit_helpers, "utc_now", lambda: "NOW")

    planilla = DummyPlanilla()
    assert audit_helpers.aprobar_planilla(planilla, "admin")
    assert planilla.estado_aprobacion == EstadoAprobacion.APROBADO
    assert not audit_helpers.aprobar_planilla(planilla, "admin")

    assert audit_helpers.rechazar_planilla(planilla, "admin", "motivo")
    assert "Razón: motivo" in calls[-1]["descripcion"]
    assert audit_helpers.rechazar_planilla(planilla, "admin")

    monkeypatch.setattr(audit_helpers, "generar_descripcion_cambios", lambda _c: "detalle")
    plugin = DummyPlanilla(creado_por_plugin=True, estado_aprobacion=EstadoAprobacion.APROBADO)
    audit_helpers.marcar_planilla_como_borrador_si_editada(plugin, "u", {})

    draft = DummyPlanilla(estado_aprobacion=EstadoAprobacion.BORRADOR)
    audit_helpers.marcar_planilla_como_borrador_si_editada(draft, "u", {})

    approved = DummyPlanilla(estado_aprobacion=EstadoAprobacion.APROBADO)
    audit_helpers.marcar_planilla_como_borrador_si_editada(approved, "u", {"a": {"old": 1, "new": 2}})
    assert approved.estado_aprobacion == EstadoAprobacion.BORRADOR

    # also cover raw log creator
    monkeypatch.setattr(audit_helpers, "crear_log_auditoria_planilla", original_creator)
    log = audit_helpers.crear_log_auditoria_planilla(DummyPlanilla(id="plx"), "x", "u", cambios=None)
    assert log.planilla_id == "plx"


def test_nomina_flujos(monkeypatch, patched_logs_db):
    original_creator = audit_helpers.crear_log_auditoria_nomina
    calls = []
    monkeypatch.setattr(audit_helpers, "crear_log_auditoria_nomina", lambda **kw: calls.append(kw))
    monkeypatch.setattr(audit_helpers, "utc_now", lambda: "NOW")

    n = DummyNomina(estado=NominaEstado.GENERADO)
    assert audit_helpers.aprobar_nomina(n, "admin")
    assert n.estado == NominaEstado.APROBADO

    n2 = DummyNomina(estado=NominaEstado.ERROR)
    assert not audit_helpers.aprobar_nomina(n2, "admin")

    assert audit_helpers.aplicar_nomina(n, "admin")
    assert n.estado == NominaEstado.APLICADO

    n3 = DummyNomina(estado=NominaEstado.GENERADO)
    assert not audit_helpers.aplicar_nomina(n3, "admin")

    assert audit_helpers.anular_nomina(n, "admin", "error")
    assert n.estado == NominaEstado.ANULADO
    assert not audit_helpers.anular_nomina(n, "admin", "error")

    monkeypatch.setattr(audit_helpers, "crear_log_auditoria_nomina", original_creator)
    log = audit_helpers.crear_log_auditoria_nomina(DummyNomina(id="nx"), "x", "u", cambios=None)
    assert log.nomina_id == "nx"


def test_regla_calculo_flujos(monkeypatch, patched_logs_db):
    original_creator = audit_helpers.crear_log_auditoria_regla_calculo
    calls = []
    monkeypatch.setattr(audit_helpers, "crear_log_auditoria_regla_calculo", lambda **kw: calls.append(kw))
    monkeypatch.setattr(audit_helpers, "utc_now", lambda: "NOW")

    regla = DummyRegla()
    assert audit_helpers.aprobar_regla_calculo(regla, "u")
    assert regla.estado_aprobacion == EstadoAprobacion.APROBADO
    assert not audit_helpers.aprobar_regla_calculo(regla, "u")

    assert audit_helpers.rechazar_regla_calculo(regla, "u", "x")
    assert "Razón: x" in calls[-1]["descripcion"]
    assert audit_helpers.rechazar_regla_calculo(regla, "u")

    monkeypatch.setattr(audit_helpers, "generar_descripcion_cambios", lambda _c: "detalle")
    plugin = DummyRegla(creado_por_plugin=True, estado_aprobacion=EstadoAprobacion.APROBADO)
    audit_helpers.marcar_regla_calculo_como_borrador_si_editada(plugin, "u", {})

    draft = DummyRegla(estado_aprobacion=EstadoAprobacion.BORRADOR)
    audit_helpers.marcar_regla_calculo_como_borrador_si_editada(draft, "u", {})

    approved = DummyRegla(estado_aprobacion=EstadoAprobacion.APROBADO)
    audit_helpers.marcar_regla_calculo_como_borrador_si_editada(approved, "u", {"x": {"old": 1, "new": 2}})
    assert approved.estado_aprobacion == EstadoAprobacion.BORRADOR

    monkeypatch.setattr(audit_helpers, "crear_log_auditoria_regla_calculo", original_creator)
    log = audit_helpers.crear_log_auditoria_regla_calculo(DummyRegla(id="rx"), "x", "u", cambios=None)
    assert log.regla_calculo_id == "rx"


def test_obtener_reglas_en_borrador_y_validacion(monkeypatch):
    session = DummySession(query_results=[[SimpleNamespace(nombre="R1", version=2)]])
    monkeypatch.setattr(audit_helpers, "db", SimpleNamespace(session=session))
    monkeypatch.setattr(audit_helpers, "ReglaCalculo", DummyRegla)
    monkeypatch.setattr(audit_helpers, "true", lambda: "TRUE")

    class PRC:
        planilla_id = "planilla_id_expr"

    import goerp_payroll.model as model

    monkeypatch.setattr(model, "PlanillaReglaCalculo", PRC)

    reglas = audit_helpers.obtener_reglas_calculo_en_borrador("pl-1")
    assert len(reglas) == 1

    monkeypatch.setattr(
        audit_helpers,
        "obtener_conceptos_en_borrador",
        lambda _id: {
            "percepciones": [SimpleNamespace(nombre="Ingreso")],
            "deducciones": [SimpleNamespace(nombre="Renta")],
            "prestaciones": [SimpleNamespace(nombre="INSS")],
        },
    )
    monkeypatch.setattr(
        audit_helpers, "obtener_reglas_calculo_en_borrador", lambda _id: [SimpleNamespace(nombre="ReglaX", version=3)]
    )

    resultado = audit_helpers.validar_configuracion_nomina("pl-1")
    assert resultado["tiene_advertencias"] is True
    assert len(resultado["advertencias"]) == 4

    monkeypatch.setattr(
        audit_helpers,
        "obtener_conceptos_en_borrador",
        lambda _id: {"percepciones": [], "deducciones": [], "prestaciones": []},
    )
    monkeypatch.setattr(audit_helpers, "obtener_reglas_calculo_en_borrador", lambda _id: [])
    limpio = audit_helpers.validar_configuracion_nomina("pl-1")
    assert limpio["tiene_advertencias"] is False
    assert limpio["advertencias"] == []
