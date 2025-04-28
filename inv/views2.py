
#ANTES DE AGREGAR CEROS A LA REFERENCIA
class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inv/movimiento_form.html'

    def get_initial(self):
        initial = super().get_initial()
        empresa = getattr(self.request.user, 'empresa', None)
        
        if empresa:
            #print(f"Empresa: ", empresa)
            #print(f"almacen_actual: ", empresa.almacen_actual)

            # Verificar que el almacen_actual está asignado
            if empresa.almacen_actual:
                try:
                    # Buscar el Almacen usando el ID almacen_actual
                    almacen = Almacen.objects.get(id=empresa.almacen_actual)
                    # Asignar solo el id del almacen
                    initial['almacen'] = almacen.id
                except Almacen.DoesNotExist:
                    print("No se encontró el almacén", empresa.almacen_actual)
                    
            else:
                print("No se asignó almacen_actual")
            
        # Asignar la fecha de hoy
        initial['fecha_movimiento'] = date.today()

        print('Initial en get_initial:', initial)
               
        return initial
    
    def get(self, request, *args, **kwargs):
        print("Entrando a MovimientoCreateView GET")  # Esto debería aparecer en la consola cuando entras al formulario
        form = self.form_class()
        formset = DetalleMovimientoFormSet(queryset=DetalleMovimiento.objects.none())  # Inicializa el formset vacío

        # Asignar el valor inicial de 'almacen'
        initial = self.get_initial()  # Llamamos a get_initial() para obtener los valores iniciales del formulario
        form.initial = initial  # Asignamos esos valores iniciales al formulario
        print('Formulario en GET:', form['almacen'].value())
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = DetalleMovimientoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Guardar el movimiento
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.move_s = movimiento.clave_movimiento.tipo
            movimiento.save()

            # Asociar los detalles con el movimiento y guardarlos
            formset.instance = movimiento
            formset.save()

            return redirect('inv:movimiento_list')  # Redirige a la lista de movimientos
        
        return render(request, self.template_name, {'form': form, 'formset': formset})
    
    def form_valid(self, form):
        # Antes de guardar, formateamos la referencia
        referencia = form.cleaned_data.get('referencia')
        if referencia:
            referencia_formateada = str(referencia).zfill(8)
            print("referencia: ",referencia_formateada)
            form.instance.referencia = referencia_formateada

        return super().form_valid(form)
