from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        exclude = ("stock",)

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True
    )
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=18, decimal_places=2)

    def validate_quantity(self, value):
        if not value:
            raise serializers.ValidationError("Не указано количество товаров.")
        if value < 1:
            raise serializers.ValidationError("Количество товаров не может быть меньше одного.")
        return value

    def validate_price(self, value):
        if not value:
            raise serializers.ValidationError("Не указана цена товара.")
        if value <= 0:
            raise serializers.ValidationError("Цена товара должна быть больше ноля.")
        return value

class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ("id", "address", "positions")

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for p in positions:
            sp = StockProduct(stock=stock, product=p["product"],
                              quantity=p["quantity"], price=p["price"])
            sp.save()

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        StockProduct.objects.filter(stock=stock).delete()
        for p in positions:
            sp = StockProduct(stock=stock, product=p["product"],
                              quantity=p["quantity"], price=p["price"])
            sp.save()

        return stock
