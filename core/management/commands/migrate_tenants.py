# ESTE PROCESO SE USA AL AGREGAR NUEVOS MODELOS EN UNA APP DEL TENANT
# SE EJECUTA EN EL HOST:
#
# 1) EN DEFAULT
# docker-compose exec web python manage.py makemigrations core  <- aqui se especifica la app
# docker-compose exec web python manage.py migrate --database=default
#
# 2) PARA MIGRAR EN TODOS LOS TENANT
# core/management/commands/migrate_tenants/Command
#
#3) Y SE CORRE:
# esto lo aplica en todas las bases de datos tenant:
#
# docker-compose exec web python manage.py migrate_tenants --apps core
#
#ESTO LO APLICA SOLO EN LA BASE DE DATOS CON ID=5 y 12 EN EMPRESADB
# docker-compose exec web python manage.py migrate_tenants --apps core --only 5 --plan
# docker-compose exec web python manage.py migrate_tenants --apps core --only 12
#
# EJEMPLO REAL DE EJECUCION Y RESULTADO ESPERADO:
#
#root@SWITCHH:~/admin# docker-compose exec web python manage.py migrate_tenants --apps core --only 2
#
#
# === Tenant 2 | e_test_0120250828 ===
# -> migrate core
# Operations to perform:
#   Apply all migrations: core
# Running migrations:
#   Applying core.0003_sitemessages_remove_empresa_num_usuarios_and_more... OK
# ✅ OK tenant e_test_0120250828 (changed=True)
#
# ============================================================
# 📊 RESUMEN MIGRACIÓN TENANTS
# ============================================================
# ✔ OK: 1
#   - e_test_0120250828
#
# 🎉 Ningún tenant falló
#
# ⏱ Tiempo total: 0.19 segundos
# ============================================================

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connections, close_old_connections

from core.models import EmpresaDB
from core.middleware import reconfigurar_conexion_tenant

import time


TENANT_ALIAS = "tenant"


class Command(BaseCommand):
    help = "Aplica migraciones a todas las bases de datos tenant (DB-per-tenant)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apps",
            nargs="*",
            default=[],
            help="Lista de apps a migrar (ej: crm autos tarifas cotizador). Si se omite, migra todo.",
        )
        parser.add_argument(
            "--fake-initial",
            action="store_true",
            help="Usa --fake-initial para evitar conflictos si ya existen tablas.",
        )
        parser.add_argument(
            "--plan",
            action="store_true",
            help="Solo muestra el plan de migración (no aplica cambios).",
        )
        parser.add_argument(
            "--database",
            default="default",
            help="Alias donde vive EmpresaDB (por defecto 'default').",
        )
        parser.add_argument(
            "--only",
            nargs="*",
            type=int,
            default=[],
            help="IDs de EmpresaDB a procesar (ej: --only 1 5 9).",
        )
        parser.add_argument(
            "--exclude",
            nargs="*",
            type=int,
            default=[],
            help="IDs de EmpresaDB a excluir (ej: --exclude 2 3).",
        )

    def handle(self, *args, **opts):
        inicio = time.time()

        apps = opts["apps"]
        fake_initial = opts["fake_initial"]
        plan_only = opts["plan"]
        global_alias = opts["database"]
        only_ids = set(opts["only"] or [])
        exclude_ids = set(opts["exclude"] or [])

        qs = EmpresaDB.objects.using(global_alias).all().order_by("id")
        if only_ids:
            qs = qs.filter(id__in=only_ids)
        if exclude_ids:
            qs = qs.exclude(id__in=exclude_ids)

        tenants = list(qs)
        if not tenants:
            self.stdout.write(self.style.WARNING("No hay EmpresaDB registrados (según filtros)."))
            return

        ok_tenants = []
        failed_tenants = []

        for t in tenants:
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n=== Tenant {t.id} | {t.db_name} ==="))

            close_old_connections()

            nueva_config = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": (t.db_name or "").strip(),
                "USER": (t.db_user or "").strip(),
                "PASSWORD": (t.db_password or "").strip(),
                "HOST": (t.db_host or "").strip(),
                "PORT": str(t.db_port).strip() if t.db_port is not None else "",
                "TIME_ZONE": "America/Mexico_City",
                "CONN_MAX_AGE": 600,
                "AUTOCOMMIT": True,
                "ATOMIC_REQUESTS": False,
                "CONN_HEALTH_CHECKS": False,
                "OPTIONS": {},
            }

            try:
                changed = reconfigurar_conexion_tenant(TENANT_ALIAS, nueva_config)
                settings.DATABASES[TENANT_ALIAS] = nueva_config

                try:
                    connections[TENANT_ALIAS].close()
                except Exception:
                    pass

                # Ping
                with connections[TENANT_ALIAS].cursor() as cursor:
                    cursor.execute("SELECT 1;")

                migrate_kwargs = {
                    "database": TENANT_ALIAS,
                    "fake_initial": fake_initial,
                    "interactive": False,
                    "verbosity": opts.get("verbosity", 1),
                }

                if plan_only:
                    call_command("migrate", plan=True, **migrate_kwargs)
                    ok_tenants.append(t.db_name)
                    continue

                if apps:
                    for app_label in apps:
                        self.stdout.write(self.style.HTTP_INFO(f"-> migrate {app_label}"))
                        call_command("migrate", app_label, **migrate_kwargs)
                else:
                    call_command("migrate", **migrate_kwargs)

                self.stdout.write(self.style.SUCCESS(f"✅ OK tenant {t.db_name} (changed={changed})"))
                ok_tenants.append(t.db_name)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error migrando {t.db_name}: {e}"))
                failed_tenants.append((t.db_name, str(e)))
                continue

        fin = time.time()
        duracion = round(fin - inicio, 2)

        # =========================
        # 📊 RESUMEN FINAL
        # =========================

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.MIGRATE_HEADING("📊 RESUMEN MIGRACIÓN TENANTS"))
        self.stdout.write("=" * 60)

        self.stdout.write(self.style.SUCCESS(f"✔ OK: {len(ok_tenants)}"))
        for db in ok_tenants:
            self.stdout.write(f"   - {db}")

        if failed_tenants:
            self.stdout.write(self.style.ERROR(f"\n✖ FALLIDOS: {len(failed_tenants)}"))
            for db, error in failed_tenants:
                self.stdout.write(f"   - {db}")
                self.stdout.write(f"     → {error}")
        else:
            self.stdout.write(self.style.SUCCESS("\n🎉 Ningún tenant falló"))

        self.stdout.write(f"\n⏱ Tiempo total: {duracion} segundos")
        self.stdout.write("=" * 60)
