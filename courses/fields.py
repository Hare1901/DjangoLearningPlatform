from django.db import models

from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    """
    кастомное поле для определения очередности по существующим полям
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        """

        :param for_fields:  поле для ручного указания нумерации

        """
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # Проверяем: если значение поля не задано (None), назначим его автоматически
        if getattr(model_instance, self.attname) is None:
            try:
                # Получаем менеджер модели
                qs = self.model.objects.all()

                if self.for_fields:
                    # Фильтруем объекты по совпадающим значениям полей из for_fields
                    filter_kwargs = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**filter_kwargs)

                # Получаем объект с максимальным значением текущего поля (например, order)
                last_item = qs.latest(self.attname)

                # Новое значение — на 1 больше
                value = getattr(last_item, self.attname) + 1

            except ObjectDoesNotExist:
                # Если в этой группе ещё нет объектов — начнем с нуля
                value = 0

            # Устанавливаем рассчитанное значение в экземпляр
            setattr(model_instance, self.attname, value)
            return value

        else:
            # Если значение уже задано вручную — используем родительскую реализацию
            return super(OrderField, self).pre_save(model_instance, add)